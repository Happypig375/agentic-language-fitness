The program reads one JSON request per input line and writes exactly one JSON
response per input line. For `ready`, return exactly `{"ids": [...]}` containing
pending orders (case-insensitive status), initially ordered by creation instant
ascending and then ordinal ID ascending. Empty orders yield an empty ID array.
A JSON null request yields exactly `{"error": "Request was null"}`. Requests
are independent; there is no retained application state between lines.

Apply the included earlier contracts chronologically, then the current task;
later contracts override only the behavior they explicitly change. Preserve
the supplied JSON adaptation and .NET standard-library-only project. Do not
infer new requirements for inputs outside these declared contracts. Compilation
warnings do not fail a build. Development checks exercise these contracts and,
for extraction, engine-file presence and the declared F# compilation order.
