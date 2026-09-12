# Shared task guidance

Implement the current public contract in the supplied repository and language.
Use .NET SDK 10.0.302 and no added dependency. Choose natural private
boundaries and idioms; keep the public wire behavior exact and do not assume a
particular private file layout.

Keep validation, state ownership and transition/effect ordering behind clear
private boundaries. Separate JSON I/O from the state-transition rules where
useful. Owned mutable collections and immutable values are both acceptable;
choose them for the operation's semantics rather than an assumed style rule.

The public seed contract and every earlier episode remain binding unless a
later public requirement explicitly supersedes one. Later tasks may require
repairing an earlier missing feature; no private interface name is a prerequisite.

Each episode provides the current repository, this guidance, all prior public
obligations, and its current episode document in a fresh no-tools conversation.
Submit a JSON object containing `files`, a mapping of changed safe full-file
paths to complete UTF-8 contents, and a short string `architecture_notes`.
Malformed submission envelopes or unsafe path changes do not replace the current
safe state. Validly submitted code may be incomplete or wrong; do not assume
earlier required features work. Fix inherited defects within the same submission
when needed to satisfy the cumulative public contract.

Keep existing public obligations working while implementing the current delta.
The `architecture_notes` string is an archived impact explanation, not an
automatically persisted repository file. Put any notes needed by a later
maintainer in a changed Markdown file in `files`; those bytes are then ordinary
repository state and count in later supplied context. Tests are also ordinary
repository artifacts, not replacements for the external contract. Do not add
tools, network calls, clocks, randomness, graphics, or external services.
Use checked 64-bit arithmetic and deterministic ordinal ordering. Keep effects
and errors observable exactly as specified. Public examples are executable
examples, not implementation prescriptions.
