open System
open System.Text.Json

[<CLIMutable>]
type Order =
    { id: string
      createdAt: DateTimeOffset
      status: string
      priority: Nullable<int>
      dueAt: Nullable<DateTimeOffset> }

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

let isStatus expected actual =
    String.Equals(expected, actual, StringComparison.OrdinalIgnoreCase)

let priorityOf (loc_dagq2dkqyn: Order) =
    if loc_dagq2dkqyn.priority.HasValue then loc_dagq2dkqyn.priority.Value else 0

let ready (orders: Order array) =
    orders
    |> Array.filter (fun loc_dagq2dkqyn -> isStatus "pending" loc_dagq2dkqyn.status)
    |> Array.sortBy (fun loc_dagq2dkqyn -> -(priorityOf loc_dagq2dkqyn), loc_dagq2dkqyn.createdAt, loc_dagq2dkqyn.id)

let overdue asOf (orders: Order array) =
    orders
    |> Array.filter (fun loc_dagq2dkqyn ->
        (isStatus "pending" loc_dagq2dkqyn.status || isStatus "processing" loc_dagq2dkqyn.status)
        && loc_dagq2dkqyn.dueAt.HasValue
        && loc_dagq2dkqyn.dueAt.Value < asOf)
    |> Array.sortBy (fun loc_dagq2dkqyn -> loc_dagq2dkqyn.dueAt.Value, -(priorityOf loc_dagq2dkqyn), loc_dagq2dkqyn.id)

let handle (loc_zk64hdzcrs: Request) =
    let selected =
        match loc_zk64hdzcrs.operation with
        | operation when isStatus "ready" operation -> ready loc_zk64hdzcrs.orders
        | operation when isStatus "overdue" operation ->
            if not loc_zk64hdzcrs.asOf.HasValue then
                invalidArg "asOf" "asOf is required for overdue"
            overdue loc_zk64hdzcrs.asOf.Value loc_zk64hdzcrs.orders
        | operation -> invalidArg "operation" $"Unknown operation: {operation}"

    selected |> Array.map (fun loc_dagq2dkqyn -> loc_dagq2dkqyn.id) |> fun ids -> { ids = ids }

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
