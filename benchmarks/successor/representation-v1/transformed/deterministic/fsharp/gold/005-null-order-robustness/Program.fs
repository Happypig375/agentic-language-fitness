open System
open System.Text.Json

[<CLIMutable>]
type Customer =
    { id: string
      tier: string }

[<CLIMutable>]
type Order =
    { id: string
      createdAt: DateTimeOffset
      status: string
      priority: Nullable<int>
      dueAt: Nullable<DateTimeOffset>
      customer: Customer }

[<CLIMutable>]
type Request =
    { operation: string
      orders: Order array
      asOf: Nullable<DateTimeOffset> }

[<CLIMutable>]
type Response = { ids: string array }

let options =
    JsonSerializerOptions(
        PropertyNameCaseInsensitive = true,
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase
    )

let isStatus actual expected =
    String.Equals(actual, expected, StringComparison.OrdinalIgnoreCase)

let isActive status =
    isStatus status "pending" || isStatus status "processing"

let priorityOf (loc_dagq2dkqyn: Order) =
    if loc_dagq2dkqyn.priority.HasValue then loc_dagq2dkqyn.priority.Value else 0

let normalizeOrders (orders: Order array) =
    if Object.ReferenceEquals(orders, null) then
        [||]
    else
        orders
        |> Array.choose (fun loc_dagq2dkqyn ->
            if isNull (box loc_dagq2dkqyn) then None else Some loc_dagq2dkqyn)

let compareReady (left: Order) (right: Order) =
    let byPriority = compare (priorityOf right) (priorityOf left)

    if byPriority <> 0 then
        byPriority
    else
        let byCreatedAt = DateTimeOffset.Compare(left.createdAt, right.createdAt)

        if byCreatedAt <> 0 then
            byCreatedAt
        else
            StringComparer.Ordinal.Compare(left.id, right.id)

let compareDuePriorityId (left: Order) (right: Order) =
    let byDueAt = DateTimeOffset.Compare(left.dueAt.Value, right.dueAt.Value)

    if byDueAt <> 0 then
        byDueAt
    else
        let byPriority = compare (priorityOf right) (priorityOf left)

        if byPriority <> 0 then
            byPriority
        else
            StringComparer.Ordinal.Compare(left.id, right.id)

let ready (orders: Order array) =
    orders
    |> Array.filter (fun loc_dagq2dkqyn -> isStatus loc_dagq2dkqyn.status "pending")
    |> Array.sortWith compareReady

let overdue asOf (orders: Order array) =
    orders
    |> Array.filter (fun loc_dagq2dkqyn ->
        isActive loc_dagq2dkqyn.status
        && loc_dagq2dkqyn.dueAt.HasValue
        && loc_dagq2dkqyn.dueAt.Value < asOf)
    |> Array.sortWith compareDuePriorityId

let atRisk (asOf: DateTimeOffset) (orders: Order array) =
    let upperBound = asOf.AddHours(24.0)

    orders
    |> Array.filter (fun loc_dagq2dkqyn ->
        isActive loc_dagq2dkqyn.status
        && loc_dagq2dkqyn.dueAt.HasValue
        && loc_dagq2dkqyn.dueAt.Value >= asOf
        && loc_dagq2dkqyn.dueAt.Value < upperBound)
    |> Array.sortWith compareDuePriorityId

let isVip (loc_dagq2dkqyn: Order) =
    not (isNull (box loc_dagq2dkqyn.customer))
    && (isStatus loc_dagq2dkqyn.customer.tier "gold"
        || isStatus loc_dagq2dkqyn.customer.tier "platinum")

let handle (loc_zk64hdzcrs: Request) =
    let orders = normalizeOrders loc_zk64hdzcrs.orders

    let selected =
        match loc_zk64hdzcrs.operation with
        | operation when isStatus operation "ready" ->
            ready orders
        | operation when isStatus operation "overdue" ->
            if not loc_zk64hdzcrs.asOf.HasValue then
                raise (InvalidOperationException("asOf is required for overdue"))

            overdue loc_zk64hdzcrs.asOf.Value orders
        | operation when isStatus operation "atRisk" ->
            if not loc_zk64hdzcrs.asOf.HasValue then
                raise (InvalidOperationException("asOf is required for atRisk"))

            atRisk loc_zk64hdzcrs.asOf.Value orders
        | operation when isStatus operation "vipReady" ->
            orders
            |> ready
            |> Array.filter isVip
        | operation ->
            raise (InvalidOperationException($"Unknown operation: {operation}"))

    selected
    |> Array.map (fun loc_dagq2dkqyn -> loc_dagq2dkqyn.id)
    |> fun ids -> { ids = ids }

let mutable running = true

while running do
    match Console.ReadLine() with
    | null -> running <- false
    | loc_ey5euhrnbl ->
        try
            let loc_zk64hdzcrs = JsonSerializer.Deserialize<Request>(loc_ey5euhrnbl, options)

            match loc_zk64hdzcrs with
            | null -> raise (InvalidOperationException("Request was null"))
            | loc_zk64hdzcrs ->
                let loc_r43bavyf4z = handle loc_zk64hdzcrs
                Console.WriteLine(JsonSerializer.Serialize(loc_r43bavyf4z, options))
        with loc_fnvfrnyz4a ->
            Console.WriteLine(JsonSerializer.Serialize({| error = loc_fnvfrnyz4a.Message |}, options))
