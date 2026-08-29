module OrderFlowEngine

open System

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
      asOf: Nullable<DateTimeOffset>
      id: string
      toStatus: string }

[<CLIMutable>]
type Response = { ids: string array }

[<CLIMutable>]
type TransitionResponse =
    { id: string
      status: string }

let private isStatus actual expected =
    String.Equals(actual, expected, StringComparison.OrdinalIgnoreCase)

let private isActive status =
    isStatus status "pending" || isStatus status "processing"

let private priorityOf (order: Order) =
    if order.priority.HasValue then order.priority.Value else 0

let private normalizeOrders (orders: Order array) =
    if Object.ReferenceEquals(orders, null) then
        [||]
    else
        orders
        |> Array.choose (fun order ->
            if isNull (box order) then None else Some order)

let private compareReady (left: Order) (right: Order) =
    let byPriority = compare (priorityOf right) (priorityOf left)

    if byPriority <> 0 then
        byPriority
    else
        let byCreatedAt = DateTimeOffset.Compare(left.createdAt, right.createdAt)

        if byCreatedAt <> 0 then
            byCreatedAt
        else
            StringComparer.Ordinal.Compare(left.id, right.id)

let private compareDuePriorityId (left: Order) (right: Order) =
    let byDueAt = DateTimeOffset.Compare(left.dueAt.Value, right.dueAt.Value)

    if byDueAt <> 0 then
        byDueAt
    else
        let byPriority = compare (priorityOf right) (priorityOf left)

        if byPriority <> 0 then
            byPriority
        else
            StringComparer.Ordinal.Compare(left.id, right.id)

let private ready (orders: Order array) =
    orders
    |> Array.filter (fun order -> isStatus order.status "pending")
    |> Array.sortWith compareReady

let private overdue asOf (orders: Order array) =
    orders
    |> Array.filter (fun order ->
        isActive order.status
        && order.dueAt.HasValue
        && order.dueAt.Value < asOf)
    |> Array.sortWith compareDuePriorityId

let private atRisk (asOf: DateTimeOffset) (orders: Order array) =
    let upperBound = asOf.AddHours(24.0)

    orders
    |> Array.filter (fun order ->
        isActive order.status
        && order.dueAt.HasValue
        && order.dueAt.Value >= asOf
        && order.dueAt.Value < upperBound)
    |> Array.sortWith compareDuePriorityId

let private isVip (order: Order) =
    not (isNull (box order.customer))
    && (isStatus order.customer.tier "gold"
        || isStatus order.customer.tier "platinum")

let private canonicalTarget source target =
    if isStatus source "pending" then
        if isStatus target "processing" then
            "processing"
        elif isStatus target "cancelled" then
            "cancelled"
        else
            raise (InvalidOperationException("invalid transition"))
    elif isStatus source "processing" then
        if isStatus target "completed" then
            "completed"
        elif isStatus target "cancelled" then
            "cancelled"
        else
            raise (InvalidOperationException("invalid transition"))
    else
        raise (InvalidOperationException("invalid transition"))

let private transition (request: Request) : TransitionResponse =
    if String.IsNullOrEmpty(request.id) then
        raise (InvalidOperationException("id is required for transition"))

    if String.IsNullOrEmpty(request.toStatus) then
        raise (InvalidOperationException("toStatus is required for transition"))

    let matches =
        request.orders
        |> normalizeOrders
        |> Array.filter (fun order ->
            String.Equals(order.id, request.id, StringComparison.Ordinal))

    if matches.Length = 0 then
        raise (InvalidOperationException("order not found for transition"))

    if matches.Length > 1 then
        raise (InvalidOperationException("duplicate order id for transition"))

    { id = matches[0].id
      status = canonicalTarget matches[0].status request.toStatus }

let private query (request: Request) : Response =
    let orders = normalizeOrders request.orders

    let selected =
        match request.operation with
        | operation when isStatus operation "ready" ->
            ready orders
        | operation when isStatus operation "overdue" ->
            if not request.asOf.HasValue then
                raise (InvalidOperationException("asOf is required for overdue"))

            overdue request.asOf.Value orders
        | operation when isStatus operation "atRisk" ->
            if not request.asOf.HasValue then
                raise (InvalidOperationException("asOf is required for atRisk"))

            atRisk request.asOf.Value orders
        | operation when isStatus operation "vipReady" ->
            orders
            |> ready
            |> Array.filter isVip
        | operation ->
            raise (InvalidOperationException($"Unknown operation: {operation}"))

    selected
    |> Array.map (fun order -> order.id)
    |> fun ids -> { ids = ids }

let handle (request: Request) : obj | null =
    if isStatus request.operation "transition" then
        box (transition request)
    else
        box (query request)
