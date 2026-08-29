# Add an at-risk order query

Add an `atRisk` operation with these rules:

1. `asOf` is required; missing or null returns the exact error `asOf is required for atRisk`;
2. include only `pending` or `processing` orders, compared case-insensitively;
3. include only orders whose `dueAt` instant is in the half-open interval `[asOf, asOf + 24 hours)`;
4. exclude orders with no `dueAt`;
5. sort by `dueAt` ascending, then priority descending (missing means `0`), then `id` in ordinal ascending order;
6. return exactly `{ "ids": [...] }`.

Compare `DateTimeOffset` values as instants, including when different offsets spell the same instant. Unknown operations must return the exact error `Unknown operation: <value>` without an appended parameter name.

Retain the existing priority-aware `ready` and `overdue` operations, the line-delimited JSON protocol, and the .NET standard-library-only constraint.
