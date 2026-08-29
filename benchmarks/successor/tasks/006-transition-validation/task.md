# Add validated stateless transitions

Add a `transition` operation with request fields `id` and `toStatus`. Apply validation in this exact order:

1. a missing, null, or empty `id` returns `id is required for transition`;
2. a missing, null, or empty `toStatus` returns `toStatus is required for transition`;
3. find orders whose `id` is an ordinal, case-sensitive match; no match returns `order not found for transition`, and more than one match returns `duplicate order id for transition`;
4. compare statuses case-insensitively and allow only `pending` to `processing` or `cancelled`, and `processing` to `completed` or `cancelled`; every other pair returns `invalid transition`.

On success, return exactly `{ "id": <matched id>, "status": <canonical lowercase target> }`. The operation is stateless: do not modify input data or retain changes across input lines.

Missing or null orders and null array elements follow the behavior introduced by the previous task. Preserve all earlier operations, errors, response shapes, and the line-delimited JSON protocol.
