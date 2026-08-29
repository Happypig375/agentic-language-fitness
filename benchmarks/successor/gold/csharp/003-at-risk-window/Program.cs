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

        if (IsStatus(request.Operation, "ready"))
        {
            selected = Ready(request.Orders);
        }
        else if (IsStatus(request.Operation, "overdue"))
        {
            var asOf = request.AsOf
                ?? throw new ArgumentException(
                    "asOf is required for overdue",
                    nameof(request.AsOf));
            selected = Overdue(request.Orders, asOf);
        }
        else if (IsStatus(request.Operation, "atRisk"))
        {
            var asOf = request.AsOf
                ?? throw new InvalidOperationException("asOf is required for atRisk");
            selected = AtRisk(request.Orders, asOf);
        }
        else
        {
            throw new InvalidOperationException($"Unknown operation: {request.Operation}");
        }

        return new Response(selected.Select(order => order.Id).ToArray());
    }

    private static IEnumerable<Order> Ready(IEnumerable<Order> orders) =>
        orders
            .Where(order => IsStatus(order.Status, "pending"))
            .OrderByDescending(order => order.Priority ?? 0)
            .ThenBy(order => order.CreatedAt)
            .ThenBy(order => order.Id, StringComparer.Ordinal);

    private static IEnumerable<Order> Overdue(
        IEnumerable<Order> orders,
        DateTimeOffset asOf) =>
        orders
            .Where(order =>
                IsActive(order.Status)
                && order.DueAt.HasValue
                && order.DueAt.Value < asOf)
            .OrderBy(order => order.DueAt!.Value)
            .ThenByDescending(order => order.Priority ?? 0)
            .ThenBy(order => order.Id, StringComparer.Ordinal);

    private static IEnumerable<Order> AtRisk(
        IEnumerable<Order> orders,
        DateTimeOffset asOf)
    {
        var upperBound = asOf.AddHours(24);

        return orders
            .Where(order =>
                IsActive(order.Status)
                && order.DueAt.HasValue
                && order.DueAt.Value >= asOf
                && order.DueAt.Value < upperBound)
            .OrderBy(order => order.DueAt!.Value)
            .ThenByDescending(order => order.Priority ?? 0)
            .ThenBy(order => order.Id, StringComparer.Ordinal);
    }

    private static bool IsActive(string? status) =>
        IsStatus(status, "pending") || IsStatus(status, "processing");

    private static bool IsStatus(string? actual, string expected) =>
        string.Equals(actual, expected, StringComparison.OrdinalIgnoreCase);
}
