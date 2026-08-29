open System
open System.Text.Json

[<CLIMutable>]
type Order =
    { id: string
      createdAt: DateTimeOffset
      status: string
      priority: Nullable<int> }

[<CLIMutable>]
type Request =
    { operation: string
      orders: Order array }

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

let handle (request: Request) =
    match request.operation with
    | operation when isStatus "ready" operation ->
        request.orders
        |> Array.filter (fun order -> isStatus "pending" order.status)
        |> Array.sortBy (fun order -> -(priorityOf order), order.createdAt, order.id)
        |> Array.map (fun order -> order.id)
        |> fun ids -> { ids = ids }
    | operation -> invalidArg "operation" $"Unknown operation: {operation}"

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
