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

public sealed record SummaryResponse(
    int Pending,
    int Processing,
    int Completed,
    int Cancelled,
    int Overdue);

public static class OrderFlowEngine
{
    public static object Handle(Request request)
    {
        if (IsStatus(request.Operation, "transition"))
        {
            return Transition(request);
        }

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
        else if (IsStatus(request.Operation, "summary"))
        {
            return Summarize(orders, request.AsOf);
        }
        else
        {
            throw new InvalidOperationException($"Unknown operation: {request.Operation}");
        }

        return new Response(selected.Select(order => order.Id).ToArray());
    }

    private static TransitionResponse Transition(Request request)
    {
        if (string.IsNullOrEmpty(request.Id))
        {
            throw new InvalidOperationException("id is required for transition");
        }

        if (string.IsNullOrEmpty(request.ToStatus))
        {
            throw new InvalidOperationException("toStatus is required for transition");
        }

        var matches = NormalizeOrders(request.Orders)
            .Where(order =>
                string.Equals(order.Id, request.Id, StringComparison.Ordinal))
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

        var target = CanonicalTarget(matches[0].Status, request.ToStatus);
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

    private static SummaryResponse Summarize(
        IEnumerable<Order> orders,
        DateTimeOffset? asOf)
    {
        var pending = 0;
        var processing = 0;
        var completed = 0;
        var cancelled = 0;
        var overdue = 0;

        foreach (var order in orders)
        {
            var isPending = IsStatus(order.Status, "pending");
            var isProcessing = IsStatus(order.Status, "processing");

            if (isPending)
            {
                pending++;
            }
            else if (isProcessing)
            {
                processing++;
            }
            else if (IsStatus(order.Status, "completed"))
            {
                completed++;
            }
            else if (IsStatus(order.Status, "cancelled"))
            {
                cancelled++;
            }

            if (asOf.HasValue
                && (isPending || isProcessing)
                && order.DueAt.HasValue
                && order.DueAt.Value < asOf.Value)
            {
                overdue++;
            }
        }

        return new SummaryResponse(
            pending,
            processing,
            completed,
            cancelled,
            overdue);
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
