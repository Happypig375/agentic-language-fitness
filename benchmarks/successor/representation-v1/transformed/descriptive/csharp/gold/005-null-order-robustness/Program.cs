using System.Text.Json;

namespace OrderFlow;

public sealed class Customer
{
    public string? Id { get; init; }
    public string? Tier { get; init; }
}

public sealed class Order
{
    public string Id { get; init; } = "";
    public DateTimeOffset CreatedAt { get; init; }
    public string Status { get; init; } = "";
    public int? Priority { get; init; }
    public DateTimeOffset? DueAt { get; init; }
    public Customer? Customer { get; init; }
}

public sealed class Request
{
    public string Operation { get; init; } = "";
    public Order?[]? Orders { get; init; }
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
        var orders = NormalizeOrders(request.Orders);
        IEnumerable<Order> selected;

        if (IsStatus(request.Operation, "ready"))
        {
            selected = Ready(orders);
        }
        else if (IsStatus(request.Operation, "overdue"))
        {
            var asOf = request.AsOf
                ?? throw new InvalidOperationException("asOf is required for overdue");
            selected = Overdue(orders, asOf);
        }
        else if (IsStatus(request.Operation, "atRisk"))
        {
            var asOf = request.AsOf
                ?? throw new InvalidOperationException("asOf is required for atRisk");
            selected = AtRisk(orders, asOf);
        }
        else if (IsStatus(request.Operation, "vipReady"))
        {
            selected = Ready(orders).Where(IsVip);
        }
        else
        {
            throw new InvalidOperationException($"Unknown operation: {request.Operation}");
        }

        return new Response(selected.Select(order => order.Id).ToArray());
    }

    private static Order[] NormalizeOrders(Order?[]? orders) =>
        orders?.OfType<Order>().ToArray() ?? [];

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

    private static bool IsVip(Order order) =>
        order.Customer is not null
        && (IsStatus(order.Customer.Tier, "gold")
            || IsStatus(order.Customer.Tier, "platinum"));

    private static bool IsActive(string? status) =>
        IsStatus(status, "pending") || IsStatus(status, "processing");

    private static bool IsStatus(string? actual, string expected) =>
        string.Equals(actual, expected, StringComparison.OrdinalIgnoreCase);
}
