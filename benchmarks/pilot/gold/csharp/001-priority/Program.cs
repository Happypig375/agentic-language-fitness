using System.Text.Json;

namespace OrderFlow;

public sealed class Order
{
    public string Id { get; init; } = "";
    public DateTimeOffset CreatedAt { get; init; }
    public string Status { get; init; } = "";
    public int? Priority { get; init; }
}

public sealed class Request
{
    public string Operation { get; init; } = "";
    public Order[] Orders { get; init; } = [];
}

public sealed record Response(string[] Ids);

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
                var response = Handle(request);
                Console.WriteLine(JsonSerializer.Serialize(response, Options));
            }
            catch (Exception ex)
            {
                Console.WriteLine(JsonSerializer.Serialize(new { error = ex.Message }, Options));
            }
        }
    }

    private static Response Handle(Request request)
    {
        if (!string.Equals(request.Operation, "ready", StringComparison.OrdinalIgnoreCase))
            throw new ArgumentException($"Unknown operation: {request.Operation}", nameof(request.Operation));

        var ids = request.Orders
            .Where(order => string.Equals(order.Status, "pending", StringComparison.OrdinalIgnoreCase))
            .OrderByDescending(order => order.Priority ?? 0)
            .ThenBy(order => order.CreatedAt)
            .ThenBy(order => order.Id, StringComparer.Ordinal)
            .Select(order => order.Id)
            .ToArray();
        return new Response(ids);
    }
}
