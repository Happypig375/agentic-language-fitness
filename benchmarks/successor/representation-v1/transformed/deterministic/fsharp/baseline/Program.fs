open System
open System.Text.Json

[<CLIMutable>]
type Order =
    { id: string
      createdAt: DateTimeOffset
      status: string }

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

let handle (loc_zk64hdzcrs: Request) =
    match loc_zk64hdzcrs.operation with
    | operation when isStatus "ready" operation ->
        loc_zk64hdzcrs.orders
        |> Array.filter (fun loc_dagq2dkqyn -> isStatus "pending" loc_dagq2dkqyn.status)
        |> Array.sortBy (fun loc_dagq2dkqyn -> loc_dagq2dkqyn.createdAt, loc_dagq2dkqyn.id)
        |> Array.map (fun loc_dagq2dkqyn -> loc_dagq2dkqyn.id)
        |> fun ids -> { ids = ids }
    | operation -> invalidArg "operation" $"Unknown operation: {operation}"

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
