Implement the current task in the supplied source snapshot. Preserve earlier
contracts included in the request. Source entries are UTF-8 text with LF
newlines. Their paths are relative to the project root.

Submit exactly one JSON object, without Markdown fences or commentary:

```json
{"files": {"Program.cs": "complete replacement file contents\n"}}
```

Include complete contents of every added or changed file. Omitted files stay
unchanged; `{"files": {}}` submits the current state. Deletion and renaming are
not supported. Use root-level ASCII names beginning with a letter and containing
only letters, digits, or underscores, with the assigned `.cs` or `.fs` extension.
At most eight source files are allowed. A submission may use at most 49,152 UTF-8
bytes; the resulting source/project snapshot may use at most 65,536 bytes.

Keep the project framework, dependencies, compiler settings, and build targets
unchanged. F# may change only the ordered `<Compile Include="..." />` entries to
include its source files; `Program.fs` must remain last. For engine extraction,
`OrderFlowEngine.fs` must precede `Program.fs`. C# uses the existing implicit
source inclusion. The engine filename and division of responsibilities stated
in the extraction task are required; other internal names and implementations
may differ from the starting code.

There are no shell, build, test, network, language-server, or external tools.
Reason over the supplied files and return a submission. No execution feedback
is available before the first submission. If development checks fail, up to two
repair submissions may follow in this conversation. Each repair applies to the
current accepted source snapshot supplied with the feedback. Invalid JSON or
file replacement leaves that snapshot unchanged and consumes the submission.
A forbidden project change ends the trajectory as a protocol violation.

Development examples and compiler/development feedback are the only execution
information available. Keep the line-delimited JSON program protocol and
stateless behavior. Do not add external dependencies, generated build scripts,
or attempts to access the host environment.
