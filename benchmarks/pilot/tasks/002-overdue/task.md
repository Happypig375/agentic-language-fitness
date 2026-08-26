# Add overdue-order query

Extend an order with an optional timestamp field `dueAt`. Extend a request with an optional timestamp field `asOf`.

Add an `overdue` operation with these rules:

1. `asOf` is required for this operation;
2. include only `pending` or `processing` orders (case-insensitive);
3. include only orders with `dueAt` strictly earlier than `asOf`;
4. exclude orders with no `dueAt`;
5. sort by `dueAt` ascending, then priority descending (missing means `0`), then `id` in ordinal ascending order.

Retain the priority-aware `ready` operation and the line-delimited JSON protocol. Use only the .NET standard library.
