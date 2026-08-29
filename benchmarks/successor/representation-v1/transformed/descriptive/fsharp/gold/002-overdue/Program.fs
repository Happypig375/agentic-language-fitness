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

let priorityOf (order: Order) =
    if order.priority.HasValue then order.priority.Value else 0

let ready (orders: Order array) =
    orders
    |> Array.filter (fun order -> isStatus "pending" order.status)
    |> Array.sortBy (fun order -> -(priorityOf order), order.createdAt, order.id)

let overdue asOf (orders: Order array) =
    orders
    |> Array.filter (fun order ->
        (isStatus "pending" order.status || isStatus "processing" order.status)
        && order.dueAt.HasValue
        && order.dueAt.Value < asOf)
    |> Array.sortBy (fun order -> order.dueAt.Value, -(priorityOf order), order.id)

let handle (request: Request) =
    let selected =
        match request.operation with
        | operation when isStatus "ready" operation -> ready request.orders
        | operation when isStatus "overdue" operation ->
            if not request.asOf.HasValue then
                invalidArg "asOf" "asOf is required for overdue"
            overdue request.asOf.Value request.orders
        | operation -> invalidArg "operation" $"Unknown operation: {operation}"

    selected |> Array.map (fun order -> order.id) |> fun ids -> { ids = ids }

let mutable running = true

while running do
    match Console.ReadLine() with
    | null -> running <- false
    | input ->
      try
        let request = JsonSerializer.Deserialize<Request>(input, options)
        match request with
        | null -> raise (InvalidOperationException("Request was null"))
        | request ->
          let response = handle request
          Console.WriteLine(JsonSerializer.Serialize(response, options))
      with ex ->
        Console.WriteLine(JsonSerializer.Serialize({| error = ex.Message |}, options))
