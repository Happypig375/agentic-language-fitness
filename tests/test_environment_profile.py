import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from alf.environment_profile import (
    EnvironmentProfileError,
    environment_profile_sha256,
    load_environment_profile,
    validate_container_route,
)
from alf.runner import route_profile_identity


ROOT = Path(__file__).parents[1]
PROFILE = ROOT / "infra" / "remote-runner" / "environment-profile.json"


class EnvironmentProfileTests(unittest.TestCase):
    def test_tracked_profile_hashes_and_matches_container_route(self):
        profile = load_environment_profile(PROFILE, repository_root=ROOT)
        self.assertRegex(environment_profile_sha256(profile), r"^[0-9a-f]{64}$")
        validate_container_route(
            profile,
            docker_network="alf-internal",
            https_proxy="http://172.30.0.1:43128",
            http_proxy="http://172.30.0.1:43128",
            no_proxy="127.0.0.1,localhost",
        )

    def test_route_drift_and_outside_profile_fail_closed(self):
        profile = load_environment_profile(PROFILE, repository_root=ROOT)
        with self.assertRaisesRegex(EnvironmentProfileError, "proxy"):
            validate_container_route(
                profile,
                docker_network="alf-internal",
                https_proxy="http://172.30.0.1:43129",
                http_proxy="http://172.30.0.1:43128",
                no_proxy="127.0.0.1,localhost",
            )
        with tempfile.TemporaryDirectory() as directory:
            outside = Path(directory) / "profile.json"
            outside.write_text(json.dumps(profile), encoding="utf-8")
            with self.assertRaisesRegex(EnvironmentProfileError, "escapes"):
                load_environment_profile(outside, repository_root=ROOT)

    def test_v3_provenance_rejects_an_environment_override(self):
        with patch.dict(
            "os.environ",
            {"ALF_ENVIRONMENT_PROFILE_PATH": "docs/protocol.md"},
        ):
            with self.assertRaisesRegex(ValueError, "tracked remote-runner profile"):
                route_profile_identity(ROOT, {"schema_version": 3, "definition": {}})


if __name__ == "__main__":
    unittest.main()
