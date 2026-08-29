using System.Text.Json;

namespace OrderFlow;

public sealed class Order
{
    public string Id { get; init; } = "";
    public DateTimeOffset CreatedAt { get; init; }
    public string Status { get; init; } = "";
    public int? Priority { get; init; }
    public DateTimeOffset? DueAt { get; init; }
}

public sealed class Request
{
    public string Operation { get; init; } = "";
    public Order[] Orders { get; init; } = [];
    public DateTimeOffset? AsOf { get; init; }
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
        IEnumerable<Order> selected;
        if (string.Equals(request.Operation, "ready", StringComparison.OrdinalIgnoreCase))
        {
            selected = request.Orders
                .Where(order => string.Equals(order.Status, "pending", StringComparison.OrdinalIgnoreCase))
                .OrderByDescending(order => order.Priority ?? 0)
                .ThenBy(order => order.CreatedAt)
                .ThenBy(order => order.Id, StringComparer.Ordinal);
        }
        else if (string.Equals(request.Operation, "overdue", StringComparison.OrdinalIgnoreCase))
        {
            var asOf = request.AsOf
                ?? throw new ArgumentException("asOf is required for overdue", nameof(request.AsOf));
            selected = request.Orders
                .Where(order =>
                    (string.Equals(order.Status, "pending", StringComparison.OrdinalIgnoreCase)
                     || string.Equals(order.Status, "processing", StringComparison.OrdinalIgnoreCase))
                    && order.DueAt.HasValue
                    && order.DueAt.Value < asOf)
                .OrderBy(order => order.DueAt!.Value)
                .ThenByDescending(order => order.Priority ?? 0)
                .ThenBy(order => order.Id, StringComparer.Ordinal);
        }
        else
        {
            throw new ArgumentException($"Unknown operation: {request.Operation}", nameof(request.Operation));
        }

        return new Response(selected.Select(order => order.Id).ToArray());
    }
}
