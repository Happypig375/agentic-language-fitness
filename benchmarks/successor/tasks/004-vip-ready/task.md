# Add VIP-ready eligibility

Extend an order with an optional nested `customer` object whose `id` and `tier` fields are optional.

Add a `vipReady` operation that:

1. applies the existing `ready` eligibility rules;
2. additionally requires a customer tier equal to `gold` or `platinum`, compared case-insensitively;
3. excludes orders with a missing or null customer, or a missing or null tier;
4. uses the existing ready ordering: priority descending, `createdAt` ascending, then ordinal `id` ascending;
5. returns exactly `{ "ids": [...] }` without echoing customer data.

Keep customer data input-only. Preserve every existing operation, old payloads that omit `customer`, the line-delimited JSON protocol, and the .NET standard-library-only constraint.
