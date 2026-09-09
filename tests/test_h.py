import json
import tempfile
import unittest
from pathlib import Path

from alf.h import HBoundaryError, HController, TrajectoryDispatcher, parse_action
from alf.e3a_runner import Journal

SPEC = {"authority": {"max_submission_bytes": 49_152, "max_source_files": 8,
                       "max_total_files": 8,
                       "max_workspace_bytes": 65_536}}
SOURCE = {"OrderFlow.csproj": "<Project><PropertyGroup><OutputType>Exe</OutputType>"
          "<TargetFramework>net8.0</TargetFramework><ImplicitUsings>enable</ImplicitUsings>"
          "<Nullable>enable</Nullable></PropertyGroup></Project>", "Engine.cs": "class Engine {}"}


def cli(text, usage=None):
    usage = {"input_tokens": 3, "output_tokens": 4} if usage is None else usage
    return "\n".join((json.dumps({"type": "thread.started"}), json.dumps({"type": "turn.started"}),
        json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": text}}),
        json.dumps({"type": "turn.completed", "id": "r", "model": "mock", "usage": usage}), ""))


class Offline:
    is_live = False
    def __init__(self, outputs, **changes):
        self.outputs, self.calls, self.changes = iter(outputs), [], changes
    def launch(self, replay, timeout):
        self.calls.append((replay, timeout))
        result = {"stdout": next(self.outputs), "stderr": b"", "returncode": 0,
                  "timed_out": False, "output_overflow": False, "cleanup_confirmed": True}
        result.update(self.changes)
        return result


class HTests(unittest.TestCase):
    def controller(self, source=SOURCE, order=None, **kwargs):
        return HController(source, order or list(source), submission_spec=SPEC, **kwargs)

    def test_h1_is_pure_ordered_and_contains_all_source(self):
        source = dict(SOURCE)
        controller = self.controller(source, ["Engine.cs", "OrderFlow.csproj"], access="H1")
        source["Engine.cs"] = "changed"
        self.assertEqual(controller.request(), controller.request())
        body = json.loads(controller.request())["transcript"][0]["data"]
        self.assertEqual([x["filename"] for x in body["source"]], ["Engine.cs", "OrderFlow.csproj"])
        self.assertEqual(body["source"][0]["text"], "class Engine {}")

    def test_h2_map_only_then_resident_text_and_counted_history_persist(self):
        controller = self.controller(access="H2")
        self.assertTrue(all("text" not in x for x in json.loads(controller.request())["transcript"][0]["data"]["source"]))
        raw = '{"action":"read","paths":["Engine.cs"]}'
        first = controller.apply(raw)
        body = json.loads(first["request"])["transcript"][0]["data"]
        self.assertEqual(body["source"][1]["text"], "class Engine {}")
        self.assertEqual(body["history"][0]["raw"], raw)
        second = controller.apply(raw)
        self.assertEqual(second["results"][0]["returned"], "reference")
        self.assertEqual(json.loads(second["request"])["transcript"][0]["data"]["source"][1]["text"], "class Engine {}")

    def test_assigned_result_order_and_atomic_overflow(self):
        controller = self.controller(order=["Engine.cs", "OrderFlow.csproj"], access="H2")
        result = controller.apply('{"action":"read","paths":["OrderFlow.csproj","Engine.cs"]}')
        self.assertEqual([x["path"] for x in result["results"]], ["Engine.cs", "OrderFlow.csproj"])
        cap = len(self.controller(access="H2").request()) + 30
        failing = self.controller(access="H2", byte_cap=cap)
        with self.assertRaisesRegex(HBoundaryError, "authored-budget-exhausted"):
            failing.apply('{"action":"read","paths":["Engine.cs"]}')
        self.assertEqual((failing.reads, failing.events, failing.done), (0, [], True))

    def test_two_read_final_boundary_and_h1_read_rejection(self):
        controller = self.controller(access="H2")
        controller.apply('{"action":"read","paths":["Engine.cs"]}')
        controller.apply('{"action":"read","paths":["Engine.cs"]}')
        with self.assertRaisesRegex(HBoundaryError, "read-quota"):
            controller.apply('{"action":"read","paths":["Engine.cs"]}')
        with self.assertRaisesRegex(HBoundaryError, "read-quota"):
            self.controller(access="H1").apply('{"action":"read","paths":["Engine.cs"]}')

    def test_whole_json_duplicate_extra_nonfinite_path_and_surrogate_rejected(self):
        invalid = ('{}', '{"action":"read","paths":["Engine.cs"],"x":1}',
          '{"action":"read","paths":["Engine.cs","Engine.cs"]}', '{"action":"read","paths":["../x.cs"]}',
          '{"action":"read","paths":["Engine.cs"],"action":"read"}',
          '{"action":"submit","files":{},"n":NaN}', '{"action":"submit","files":{"Engine.cs":"\\ud800"}}',
          '{"action":"submit","files":{}} trailing')
        for raw in invalid:
            with self.subTest(raw=raw), self.assertRaises(HBoundaryError):
                parse_action(raw)
        for paths in ((["Engine.cs"],), [{"Engine.cs": 1}]):
            with self.assertRaises(HBoundaryError):
                parse_action(json.dumps({"action": "read", "paths": paths}))

    def test_submission_authority_project_validation_and_raw_retention(self):
        with self.assertRaisesRegex(HBoundaryError, "authority"):
            HController(SOURCE, list(SOURCE), submission_spec={})
        controller = self.controller(access="H1")
        result = controller.apply('{"action":"submit","files":{"OrderFlow.csproj":"<Project>"}}')
        self.assertFalse(result["project_development"]["passed"])
        unsafe = self.controller(access="H1")
        raw = '{"action":"submit","files":{"Bad.fs":"x"}}'
        with self.assertRaises(HBoundaryError): unsafe.apply(raw)
        self.assertEqual(unsafe.raw_actions, [raw])

    def test_submission_enforces_total_file_ceiling_atomically(self):
        source = {"OrderFlow.csproj": SOURCE["OrderFlow.csproj"],
                  **{f"S{i}.cs": "class S{}" for i in range(1, 8)}}
        controller = self.controller(source=source, order=list(source), access="H1")
        raw = '{"action":"submit","files":{"S8.cs":"class S8{}"}}'
        with self.assertRaisesRegex(HBoundaryError, "workspace file ceiling exceeded"):
            controller.apply(raw)
        self.assertEqual(controller.source, source)
        self.assertEqual(controller.raw_actions, [raw])

    def test_fresh_evaluator_once_no_feedback_and_shared_dispatcher(self):
        actions = ['{"action":"read","paths":["Engine.cs"]}',
                   '{"action":"submit","files":{"Engine.cs":"class Engine { int X; }"}}']
        transport, seen = Offline([cli(x) for x in actions]), []
        shared = TrajectoryDispatcher(transport, ceiling=2)
        result = self.controller(access="H2", evaluator=lambda x, _deadline: seen.append(x) or {"passed": True}).run_trajectory(dispatcher=shared)
        self.assertEqual((len(transport.calls), len(seen), shared.guard.dispatched), (2, 1, 2))
        self.assertNotIn("evaluation", transport.calls[1][0].decode())
        self.assertTrue(result["evaluation"]["passed"])

    def test_h1_infeasible_is_zero_dispatch(self):
        transport = Offline([])
        result = self.controller(access="H1", byte_cap=1, evaluator=lambda _x, _deadline: None).run_trajectory(transport)
        self.assertEqual(result["failure"], "authored-budget-exhausted")
        self.assertEqual(transport.calls, [])
        missing = self.controller(access="H1").run_trajectory(Offline([]))
        self.assertEqual(missing["failure"], "isolated-evaluator-required")

    def test_predebit_exact_retention_usage_and_live_refusal(self):
        records = []
        dispatcher = TrajectoryDispatcher(Offline([cli("{}")]), ceiling=1, record=records.append)
        self.assertEqual(dispatcher.dispatch(b"exact", 10**12)["status"], "completed")
        self.assertEqual(dispatcher.requests[0]["replay_utf8"], "exact")
        self.assertEqual([x["event"] for x in records], ["dispatch-debited", "dispatch-finished"])
        self.assertEqual(dispatcher.dispatch(b"again", 10**12)["failure"], "CodexBoundaryError")
        with self.assertRaisesRegex(HBoundaryError, "live transport refused"):
            TrajectoryDispatcher(object())

    def test_real_journal_persists_json_safe_prelaunch_replay(self):
        with tempfile.TemporaryDirectory() as temporary:
            journal = Journal(Path(temporary) / "attempt")
            dispatcher = TrajectoryDispatcher(Offline([cli("{}")]), ceiling=1, record=journal.record)
            dispatcher.dispatch("π".encode(), 10**12)
            rows = [json.loads(line) for line in journal.path.read_text().splitlines()]
            self.assertEqual(rows[0]["replay_utf8"], "π")
            self.assertEqual(rows[0]["bytes"], 2)

    def test_capture_failure_matrix_and_unknown_usd(self):
        cases = (({"cleanup_confirmed": False}, "cleanup-unconfirmed"), ({"timed_out": True}, "transport-timeout"),
                 ({"output_overflow": True}, "raw-capture-overflow"), ({"returncode": 7}, "transport-nonzero-exit"),
                 ({"stderr": None}, "invalid-transport-metadata"))
        for changes, expected in cases:
            result = TrajectoryDispatcher(Offline([cli("{}")], **changes)).dispatch(b"x", 10**12)
            self.assertEqual((result["failure"], result["usd"]), (expected, None))

    def test_usage_alarm_for_missing_invalid_or_over_threshold(self):
        for usage in ({}, {"input_tokens": 32769, "output_tokens": 1},
                      {"input_tokens": 1, "output_tokens": 8193},
                      {"input_tokens": 1, "output_tokens": 1, "cached_input_tokens": 2}):
            result = TrajectoryDispatcher(Offline([cli("{}", usage)])).dispatch(b"x", 10**12)
            self.assertEqual(result["failure"], "usage-alarm")

    def test_dispatch_and_trajectory_deadlines(self):
        clock = iter((0.0, 121.0))
        result = TrajectoryDispatcher(Offline([cli("{}")]), clock=lambda: next(clock)).dispatch(b"x", 120.0)
        self.assertEqual(result["failure"], "trajectory-deadline")
        times = []
        transport = Offline([cli('{"action":"submit","files":{}}')])
        shared = TrajectoryDispatcher(transport, clock=lambda: 0.0)
        self.controller(access="H1", evaluator=lambda _x, _deadline: None).run_trajectory(deadline=9999.0, dispatcher=shared)
        times.append(transport.calls[0][1])
        self.assertEqual(times, [120.0])

    def test_canonical_instructions_and_shared_evaluator_deadline(self):
        replay = json.loads(self.controller(access="H2").request())
        self.assertIn("exactly one read or submit envelope", replay["instructions"])
        seen = []
        controller = self.controller(access="H1", evaluator=lambda _source, deadline: seen.append(deadline) or {"passed": True})
        transport = Offline([cli('{"action":"submit","files":{}}')])
        controller.run_trajectory(deadline=77.0, dispatcher=TrajectoryDispatcher(transport, clock=lambda: 0.0))
        self.assertEqual(seen, [77.0])


if __name__ == "__main__":
    unittest.main()
