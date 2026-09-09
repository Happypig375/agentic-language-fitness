using System.Text.Json;

namespace OrderFlow;

public static class Program
{
    private static readonly JsonSerializerOptions Options = new()
    {
        PropertyNameCaseInsensitive = true,
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase
    };

    public static void Main()
    {
        string? line;
        while ((line = Console.ReadLine()) is not null)
        {
            try
            {
                var request = JsonSerializer.Deserialize<Request>(line, Options)
                    ?? throw new InvalidOperationException("Request was null");
                var response = OrderFlowEngine.Handle(request);
                Console.WriteLine(JsonSerializer.Serialize(response, Options));
            }
            catch (Exception ex)
            {
                Console.WriteLine(JsonSerializer.Serialize(new { error = ex.Message }, Options));
            }
        }
    }
}
