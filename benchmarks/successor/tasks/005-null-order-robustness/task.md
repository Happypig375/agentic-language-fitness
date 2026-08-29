# Fix null-order failures

Requests to the existing `ready`, `overdue`, `atRisk`, and `vipReady` operations can fail or return inconsistent responses in these reproductions:

- the `orders` field is omitted;
- `orders` is null;
- an orders array contains null elements before, between, or after valid orders;
- an orders array contains only null elements.

Fix the defect across all four operations while preserving every result for valid orders. Requests with no usable orders must produce an empty `ids` array, and null array elements must not affect results or ordering.

Required fields remain required. Missing or null `asOf` must return exactly `asOf is required for overdue` for `overdue` and `asOf is required for atRisk` for `atRisk`, including when order data is also absent or null. Preserve the exact unknown-operation error and every earlier response shape.
