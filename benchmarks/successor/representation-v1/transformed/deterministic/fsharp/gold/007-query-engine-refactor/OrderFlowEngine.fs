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

let private fun_qbwdskpmpf actual expected =
    String.Equals(actual, expected, StringComparison.OrdinalIgnoreCase)

let private fun_7hdzz5dlwr status =
    fun_qbwdskpmpf status "pending" || fun_qbwdskpmpf status "processing"

let private priorityOf (loc_dagq2dkqyn: Order) =
    if loc_dagq2dkqyn.priority.HasValue then loc_dagq2dkqyn.priority.Value else 0

let private fun_svzzyc72ua (orders: Order array) =
    if Object.ReferenceEquals(orders, null) then
        [||]
    else
        orders
        |> Array.choose (fun loc_dagq2dkqyn ->
            if isNull (box loc_dagq2dkqyn) then None else Some loc_dagq2dkqyn)

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

let private fun_rtvkjd7gi7 (orders: Order array) =
    orders
    |> Array.filter (fun loc_dagq2dkqyn -> fun_qbwdskpmpf loc_dagq2dkqyn.status "pending")
    |> Array.sortWith compareReady

let private fun_jjxhcduzec asOf (orders: Order array) =
    orders
    |> Array.filter (fun loc_dagq2dkqyn ->
        fun_7hdzz5dlwr loc_dagq2dkqyn.status
        && loc_dagq2dkqyn.dueAt.HasValue
        && loc_dagq2dkqyn.dueAt.Value < asOf)
    |> Array.sortWith compareDuePriorityId

let private fun_6q4qho5po5 (asOf: DateTimeOffset) (orders: Order array) =
    let upperBound = asOf.AddHours(24.0)

    orders
    |> Array.filter (fun loc_dagq2dkqyn ->
        fun_7hdzz5dlwr loc_dagq2dkqyn.status
        && loc_dagq2dkqyn.dueAt.HasValue
        && loc_dagq2dkqyn.dueAt.Value >= asOf
        && loc_dagq2dkqyn.dueAt.Value < upperBound)
    |> Array.sortWith compareDuePriorityId

let private fun_7j64sig4qk (loc_dagq2dkqyn: Order) =
    not (isNull (box loc_dagq2dkqyn.customer))
    && (fun_qbwdskpmpf loc_dagq2dkqyn.customer.tier "gold"
        || fun_qbwdskpmpf loc_dagq2dkqyn.customer.tier "platinum")

let private fun_53ppru7gia source target =
    if fun_qbwdskpmpf source "pending" then
        if fun_qbwdskpmpf target "processing" then
            "processing"
        elif fun_qbwdskpmpf target "cancelled" then
            "cancelled"
        else
            raise (InvalidOperationException("invalid transition"))
    elif fun_qbwdskpmpf source "processing" then
        if fun_qbwdskpmpf target "completed" then
            "completed"
        elif fun_qbwdskpmpf target "cancelled" then
            "cancelled"
        else
            raise (InvalidOperationException("invalid transition"))
    else
        raise (InvalidOperationException("invalid transition"))

let private fun_2eafckheko (loc_zk64hdzcrs: Request) : TransitionResponse =
    if String.IsNullOrEmpty(loc_zk64hdzcrs.id) then
        raise (InvalidOperationException("id is required for transition"))

    if String.IsNullOrEmpty(loc_zk64hdzcrs.toStatus) then
        raise (InvalidOperationException("toStatus is required for transition"))

    let matches =
        loc_zk64hdzcrs.orders
        |> fun_svzzyc72ua
        |> Array.filter (fun loc_dagq2dkqyn ->
            String.Equals(loc_dagq2dkqyn.id, loc_zk64hdzcrs.id, StringComparison.Ordinal))

    if matches.Length = 0 then
        raise (InvalidOperationException("order not found for transition"))

    if matches.Length > 1 then
        raise (InvalidOperationException("duplicate order id for transition"))

    { id = matches[0].id
      status = fun_53ppru7gia matches[0].status loc_zk64hdzcrs.toStatus }

let private query (loc_zk64hdzcrs: Request) : Response =
    let orders = fun_svzzyc72ua loc_zk64hdzcrs.orders

    let selected =
        match loc_zk64hdzcrs.operation with
        | operation when fun_qbwdskpmpf operation "ready" ->
            fun_rtvkjd7gi7 orders
        | operation when fun_qbwdskpmpf operation "overdue" ->
            if not loc_zk64hdzcrs.asOf.HasValue then
                raise (InvalidOperationException("asOf is required for overdue"))

            fun_jjxhcduzec loc_zk64hdzcrs.asOf.Value orders
        | operation when fun_qbwdskpmpf operation "atRisk" ->
            if not loc_zk64hdzcrs.asOf.HasValue then
                raise (InvalidOperationException("asOf is required for atRisk"))

            fun_6q4qho5po5 loc_zk64hdzcrs.asOf.Value orders
        | operation when fun_qbwdskpmpf operation "vipReady" ->
            orders
            |> fun_rtvkjd7gi7
            |> Array.filter fun_7j64sig4qk
        | operation ->
            raise (InvalidOperationException($"Unknown operation: {operation}"))

    selected
    |> Array.map (fun loc_dagq2dkqyn -> loc_dagq2dkqyn.id)
    |> fun ids -> { ids = ids }

let handle (loc_zk64hdzcrs: Request) : obj | null =
    if fun_qbwdskpmpf loc_zk64hdzcrs.operation "transition" then
        box (fun_2eafckheko loc_zk64hdzcrs)
    else
        box (query loc_zk64hdzcrs)
