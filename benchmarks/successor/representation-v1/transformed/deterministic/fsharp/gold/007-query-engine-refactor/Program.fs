open System
open System.Text.Json

let options =
    JsonSerializerOptions(
        PropertyNameCaseInsensitive = true,
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase
    )

let mutable running = true

while running do
    match Console.ReadLine() with
    | null -> running <- false
    | loc_ey5euhrnbl ->
        try
            let loc_zk64hdzcrs =
                JsonSerializer.Deserialize<OrderFlowEngine.Request>(loc_ey5euhrnbl, options)

            match loc_zk64hdzcrs with
            | null -> raise (InvalidOperationException("Request was null"))
            | loc_zk64hdzcrs ->
                let loc_r43bavyf4z = OrderFlowEngine.handle loc_zk64hdzcrs
                Console.WriteLine(JsonSerializer.Serialize(loc_r43bavyf4z, options))
        with loc_fnvfrnyz4a ->
            Console.WriteLine(JsonSerializer.Serialize({| error = loc_fnvfrnyz4a.Message |}, options))
