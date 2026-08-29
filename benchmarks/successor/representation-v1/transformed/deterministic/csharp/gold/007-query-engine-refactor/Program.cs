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
        string? loc_ey5euhrnbl;
        while ((loc_ey5euhrnbl = Console.ReadLine()) is not null)
        {
            try
            {
                var loc_zk64hdzcrs = JsonSerializer.Deserialize<Request>(loc_ey5euhrnbl, Options)
                    ?? throw new InvalidOperationException("Request was null");
                var loc_r43bavyf4z = OrderFlowEngine.Handle(loc_zk64hdzcrs);
                Console.WriteLine(JsonSerializer.Serialize(loc_r43bavyf4z, Options));
            }
            catch (Exception loc_fnvfrnyz4a)
            {
                Console.WriteLine(JsonSerializer.Serialize(new { error = loc_fnvfrnyz4a.Message }, Options));
            }
        }
    }
}
