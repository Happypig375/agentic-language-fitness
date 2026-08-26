# Add priority ordering

Extend the existing order model with an optional integer `priority` field.

For the existing `ready` operation:

1. include only orders whose status is `pending` (case-insensitive);
2. treat a missing priority as `0`;
3. sort by priority descending;
4. break ties by `createdAt` ascending;
5. break remaining ties by `id` in ordinal ascending order.

Preserve the line-delimited JSON input/output protocol, all baseline behavior not changed above, and the existing .NET standard-library-only constraint.
