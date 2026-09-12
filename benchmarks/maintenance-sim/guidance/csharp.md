# C# guidance

Use modern C# features such as records, pattern matching, and collection
initializers where they make the implementation clear. Encapsulated state,
owned generic collections and small private transition helpers are natural
options; immutable and mutable representations are both permitted.
`System.Text.Json` is
available from the framework; no packages are needed. Read one JSON request per
line from standard input and write one response per line to standard output.
