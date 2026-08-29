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
        string? loc_ey5euhrnbl;
        while ((loc_ey5euhrnbl = Console.ReadLine()) is not null)
        {
            try
            {
                var loc_zk64hdzcrs = JsonSerializer.Deserialize<Request>(loc_ey5euhrnbl, Options)
                    ?? throw new InvalidOperationException("Request was null");
                var loc_r43bavyf4z = Handle(loc_zk64hdzcrs);
                Console.WriteLine(JsonSerializer.Serialize(loc_r43bavyf4z, Options));
            }
            catch (Exception loc_fnvfrnyz4a)
            {
                Console.WriteLine(JsonSerializer.Serialize(new { error = loc_fnvfrnyz4a.Message }, Options));
            }
        }
    }

    private static Response Handle(Request loc_zk64hdzcrs)
    {
        IEnumerable<Order> selected;

        if (IsStatus(loc_zk64hdzcrs.Operation, "ready"))
        {
            selected = Ready(loc_zk64hdzcrs.Orders);
        }
        else if (IsStatus(loc_zk64hdzcrs.Operation, "overdue"))
        {
            var asOf = loc_zk64hdzcrs.AsOf
                ?? throw new ArgumentException(
                    "asOf is required for overdue",
                    nameof(loc_zk64hdzcrs.AsOf));
            selected = Overdue(loc_zk64hdzcrs.Orders, asOf);
        }
        else if (IsStatus(loc_zk64hdzcrs.Operation, "atRisk"))
        {
            var asOf = loc_zk64hdzcrs.AsOf
                ?? throw new InvalidOperationException("asOf is required for atRisk");
            selected = AtRisk(loc_zk64hdzcrs.Orders, asOf);
        }
        else
        {
            throw new InvalidOperationException($"Unknown operation: {loc_zk64hdzcrs.Operation}");
        }

        return new Response(selected.Select(loc_dagq2dkqyn => loc_dagq2dkqyn.Id).ToArray());
    }

    private static IEnumerable<Order> Ready(IEnumerable<Order> orders) =>
        orders
            .Where(loc_dagq2dkqyn => IsStatus(loc_dagq2dkqyn.Status, "pending"))
            .OrderByDescending(loc_dagq2dkqyn => loc_dagq2dkqyn.Priority ?? 0)
            .ThenBy(loc_dagq2dkqyn => loc_dagq2dkqyn.CreatedAt)
            .ThenBy(loc_dagq2dkqyn => loc_dagq2dkqyn.Id, StringComparer.Ordinal);

    private static IEnumerable<Order> Overdue(
        IEnumerable<Order> orders,
        DateTimeOffset asOf) =>
        orders
            .Where(loc_dagq2dkqyn =>
                IsActive(loc_dagq2dkqyn.Status)
                && loc_dagq2dkqyn.DueAt.HasValue
                && loc_dagq2dkqyn.DueAt.Value < asOf)
            .OrderBy(loc_dagq2dkqyn => loc_dagq2dkqyn.DueAt!.Value)
            .ThenByDescending(loc_dagq2dkqyn => loc_dagq2dkqyn.Priority ?? 0)
            .ThenBy(loc_dagq2dkqyn => loc_dagq2dkqyn.Id, StringComparer.Ordinal);

    private static IEnumerable<Order> AtRisk(
        IEnumerable<Order> orders,
        DateTimeOffset asOf)
    {
        var upperBound = asOf.AddHours(24);

        return orders
            .Where(loc_dagq2dkqyn =>
                IsActive(loc_dagq2dkqyn.Status)
                && loc_dagq2dkqyn.DueAt.HasValue
                && loc_dagq2dkqyn.DueAt.Value >= asOf
                && loc_dagq2dkqyn.DueAt.Value < upperBound)
            .OrderBy(loc_dagq2dkqyn => loc_dagq2dkqyn.DueAt!.Value)
            .ThenByDescending(loc_dagq2dkqyn => loc_dagq2dkqyn.Priority ?? 0)
            .ThenBy(loc_dagq2dkqyn => loc_dagq2dkqyn.Id, StringComparer.Ordinal);
    }

    private static bool IsActive(string? status) =>
        IsStatus(status, "pending") || IsStatus(status, "processing");

    private static bool IsStatus(string? actual, string expected) =>
        string.Equals(actual, expected, StringComparison.OrdinalIgnoreCase);
}
