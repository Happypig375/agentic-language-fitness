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
    public string? Id { get; init; }
    public string? ToStatus { get; init; }
}

public sealed record Response(string[] Ids);

public sealed record TransitionResponse(string Id, string Status);

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

    private static object Handle(Request loc_zk64hdzcrs)
    {
        if (IsStatus(loc_zk64hdzcrs.Operation, "transition"))
        {
            return Transition(loc_zk64hdzcrs);
        }

        var orders = NormalizeOrders(loc_zk64hdzcrs.Orders);
        IEnumerable<Order> selected;

        if (IsStatus(loc_zk64hdzcrs.Operation, "ready"))
        {
            selected = Ready(orders);
        }
        else if (IsStatus(loc_zk64hdzcrs.Operation, "overdue"))
        {
            var asOf = loc_zk64hdzcrs.AsOf
                ?? throw new InvalidOperationException("asOf is required for overdue");
            selected = Overdue(orders, asOf);
        }
        else if (IsStatus(loc_zk64hdzcrs.Operation, "atRisk"))
        {
            var asOf = loc_zk64hdzcrs.AsOf
                ?? throw new InvalidOperationException("asOf is required for atRisk");
            selected = AtRisk(orders, asOf);
        }
        else if (IsStatus(loc_zk64hdzcrs.Operation, "vipReady"))
        {
            selected = Ready(orders).Where(IsVip);
        }
        else
        {
            throw new InvalidOperationException($"Unknown operation: {loc_zk64hdzcrs.Operation}");
        }

        return new Response(selected.Select(loc_dagq2dkqyn => loc_dagq2dkqyn.Id).ToArray());
    }

    private static TransitionResponse Transition(Request loc_zk64hdzcrs)
    {
        if (string.IsNullOrEmpty(loc_zk64hdzcrs.Id))
        {
            throw new InvalidOperationException("id is required for transition");
        }

        if (string.IsNullOrEmpty(loc_zk64hdzcrs.ToStatus))
        {
            throw new InvalidOperationException("toStatus is required for transition");
        }

        var matches = NormalizeOrders(loc_zk64hdzcrs.Orders)
            .Where(loc_dagq2dkqyn =>
                string.Equals(loc_dagq2dkqyn.Id, loc_zk64hdzcrs.Id, StringComparison.Ordinal))
            .Take(2)
            .ToArray();

        if (matches.Length == 0)
        {
            throw new InvalidOperationException("order not found for transition");
        }

        if (matches.Length > 1)
        {
            throw new InvalidOperationException("duplicate order id for transition");
        }

        var target = CanonicalTarget(matches[0].Status, loc_zk64hdzcrs.ToStatus);
        return new TransitionResponse(matches[0].Id, target);
    }

    private static string CanonicalTarget(string? source, string target)
    {
        if (IsStatus(source, "pending"))
        {
            if (IsStatus(target, "processing"))
            {
                return "processing";
            }

            if (IsStatus(target, "cancelled"))
            {
                return "cancelled";
            }
        }
        else if (IsStatus(source, "processing"))
        {
            if (IsStatus(target, "completed"))
            {
                return "completed";
            }

            if (IsStatus(target, "cancelled"))
            {
                return "cancelled";
            }
        }

        throw new InvalidOperationException("invalid transition");
    }

    private static Order[] NormalizeOrders(Order?[]? orders) =>
        orders?.OfType<Order>().ToArray() ?? [];

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

    private static bool IsVip(Order loc_dagq2dkqyn) =>
        loc_dagq2dkqyn.Customer is not null
        && (IsStatus(loc_dagq2dkqyn.Customer.Tier, "gold")
            || IsStatus(loc_dagq2dkqyn.Customer.Tier, "platinum"));

    private static bool IsActive(string? status) =>
        IsStatus(status, "pending") || IsStatus(status, "processing");

    private static bool IsStatus(string? actual, string expected) =>
        string.Equals(actual, expected, StringComparison.OrdinalIgnoreCase);
}
