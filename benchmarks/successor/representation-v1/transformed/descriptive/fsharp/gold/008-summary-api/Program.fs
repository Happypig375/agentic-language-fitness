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
    | input ->
        try
            let request =
                JsonSerializer.Deserialize<OrderFlowEngine.Request>(input, options)

            match request with
            | null -> raise (InvalidOperationException("Request was null"))
            | request ->
                let response = OrderFlowEngine.handle request
                Console.WriteLine(JsonSerializer.Serialize(response, options))
        with ex ->
            Console.WriteLine(JsonSerializer.Serialize({| error = ex.Message |}, options))
