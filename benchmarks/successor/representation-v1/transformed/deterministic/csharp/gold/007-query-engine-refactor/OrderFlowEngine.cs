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

public static class OrderFlowEngine
{
    public static object Handle(Request loc_zk64hdzcrs)
    {
        if (fun_qbwdskpmpf(loc_zk64hdzcrs.Operation, "transition"))
        {
            return fun_2eafckheko(loc_zk64hdzcrs);
        }

        var orders = fun_svzzyc72ua(loc_zk64hdzcrs.Orders);
        IEnumerable<Order> selected;

        if (fun_qbwdskpmpf(loc_zk64hdzcrs.Operation, "ready"))
        {
            selected = fun_rtvkjd7gi7(orders);
        }
        else if (fun_qbwdskpmpf(loc_zk64hdzcrs.Operation, "overdue"))
        {
            var asOf = loc_zk64hdzcrs.AsOf
                ?? throw new InvalidOperationException("asOf is required for overdue");
            selected = fun_jjxhcduzec(orders, asOf);
        }
        else if (fun_qbwdskpmpf(loc_zk64hdzcrs.Operation, "atRisk"))
        {
            var asOf = loc_zk64hdzcrs.AsOf
                ?? throw new InvalidOperationException("asOf is required for atRisk");
            selected = fun_6q4qho5po5(orders, asOf);
        }
        else if (fun_qbwdskpmpf(loc_zk64hdzcrs.Operation, "vipReady"))
        {
            selected = fun_rtvkjd7gi7(orders).Where(fun_7j64sig4qk);
        }
        else
        {
            throw new InvalidOperationException($"Unknown operation: {loc_zk64hdzcrs.Operation}");
        }

        return new Response(selected.Select(loc_dagq2dkqyn => loc_dagq2dkqyn.Id).ToArray());
    }

    private static TransitionResponse fun_2eafckheko(Request loc_zk64hdzcrs)
    {
        if (string.IsNullOrEmpty(loc_zk64hdzcrs.Id))
        {
            throw new InvalidOperationException("id is required for transition");
        }

        if (string.IsNullOrEmpty(loc_zk64hdzcrs.ToStatus))
        {
            throw new InvalidOperationException("toStatus is required for transition");
        }

        var matches = fun_svzzyc72ua(loc_zk64hdzcrs.Orders)
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

        var target = fun_53ppru7gia(matches[0].Status, loc_zk64hdzcrs.ToStatus);
        return new TransitionResponse(matches[0].Id, target);
    }

    private static string fun_53ppru7gia(string? source, string target)
    {
        if (fun_qbwdskpmpf(source, "pending"))
        {
            if (fun_qbwdskpmpf(target, "processing"))
            {
                return "processing";
            }

            if (fun_qbwdskpmpf(target, "cancelled"))
            {
                return "cancelled";
            }
        }
        else if (fun_qbwdskpmpf(source, "processing"))
        {
            if (fun_qbwdskpmpf(target, "completed"))
            {
                return "completed";
            }

            if (fun_qbwdskpmpf(target, "cancelled"))
            {
                return "cancelled";
            }
        }

        throw new InvalidOperationException("invalid transition");
    }

    private static Order[] fun_svzzyc72ua(Order?[]? orders) =>
        orders?.OfType<Order>().ToArray() ?? [];

    private static IEnumerable<Order> fun_rtvkjd7gi7(IEnumerable<Order> orders) =>
        orders
            .Where(loc_dagq2dkqyn => fun_qbwdskpmpf(loc_dagq2dkqyn.Status, "pending"))
            .OrderByDescending(loc_dagq2dkqyn => loc_dagq2dkqyn.Priority ?? 0)
            .ThenBy(loc_dagq2dkqyn => loc_dagq2dkqyn.CreatedAt)
            .ThenBy(loc_dagq2dkqyn => loc_dagq2dkqyn.Id, StringComparer.Ordinal);

    private static IEnumerable<Order> fun_jjxhcduzec(
        IEnumerable<Order> orders,
        DateTimeOffset asOf) =>
        orders
            .Where(loc_dagq2dkqyn =>
                fun_7hdzz5dlwr(loc_dagq2dkqyn.Status)
                && loc_dagq2dkqyn.DueAt.HasValue
                && loc_dagq2dkqyn.DueAt.Value < asOf)
            .OrderBy(loc_dagq2dkqyn => loc_dagq2dkqyn.DueAt!.Value)
            .ThenByDescending(loc_dagq2dkqyn => loc_dagq2dkqyn.Priority ?? 0)
            .ThenBy(loc_dagq2dkqyn => loc_dagq2dkqyn.Id, StringComparer.Ordinal);

    private static IEnumerable<Order> fun_6q4qho5po5(
        IEnumerable<Order> orders,
        DateTimeOffset asOf)
    {
        var upperBound = asOf.AddHours(24);

        return orders
            .Where(loc_dagq2dkqyn =>
                fun_7hdzz5dlwr(loc_dagq2dkqyn.Status)
                && loc_dagq2dkqyn.DueAt.HasValue
                && loc_dagq2dkqyn.DueAt.Value >= asOf
                && loc_dagq2dkqyn.DueAt.Value < upperBound)
            .OrderBy(loc_dagq2dkqyn => loc_dagq2dkqyn.DueAt!.Value)
            .ThenByDescending(loc_dagq2dkqyn => loc_dagq2dkqyn.Priority ?? 0)
            .ThenBy(loc_dagq2dkqyn => loc_dagq2dkqyn.Id, StringComparer.Ordinal);
    }

    private static bool fun_7j64sig4qk(Order loc_dagq2dkqyn) =>
        loc_dagq2dkqyn.Customer is not null
        && (fun_qbwdskpmpf(loc_dagq2dkqyn.Customer.Tier, "gold")
            || fun_qbwdskpmpf(loc_dagq2dkqyn.Customer.Tier, "platinum"));

    private static bool fun_7hdzz5dlwr(string? status) =>
        fun_qbwdskpmpf(status, "pending") || fun_qbwdskpmpf(status, "processing");

    private static bool fun_qbwdskpmpf(string? actual, string expected) =>
        string.Equals(actual, expected, StringComparison.OrdinalIgnoreCase);
}
