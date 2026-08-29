# Add an order summary API

Add a `summary` operation in the extracted engine. Return exactly one object with these five integer keys: `pending`, `processing`, `completed`, `cancelled`, and `overdue`.

Count the four recognized statuses case-insensitively and ignore unknown statuses. If `asOf` is present and non-null, `overdue` counts pending or processing orders whose dated `dueAt` instant is strictly earlier than `asOf`. The overdue count overlaps the status counts and is not subtracted from them. If `asOf` is omitted or null, return `overdue: 0`.

Missing or null orders and null array elements retain the established behavior. Preserve the extracted architecture, every earlier operation and error, all previous response shapes, stateless processing, the line-delimited JSON protocol, and the .NET standard-library-only constraint.
