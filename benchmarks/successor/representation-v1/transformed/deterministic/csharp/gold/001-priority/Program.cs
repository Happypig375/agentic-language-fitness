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
        if (!string.Equals(loc_zk64hdzcrs.Operation, "ready", StringComparison.OrdinalIgnoreCase))
            throw new ArgumentException($"Unknown operation: {loc_zk64hdzcrs.Operation}", nameof(loc_zk64hdzcrs.Operation));

        var ids = loc_zk64hdzcrs.Orders
            .Where(loc_dagq2dkqyn => string.Equals(loc_dagq2dkqyn.Status, "pending", StringComparison.OrdinalIgnoreCase))
            .OrderByDescending(loc_dagq2dkqyn => loc_dagq2dkqyn.Priority ?? 0)
            .ThenBy(loc_dagq2dkqyn => loc_dagq2dkqyn.CreatedAt)
            .ThenBy(loc_dagq2dkqyn => loc_dagq2dkqyn.Id, StringComparer.Ordinal)
            .Select(loc_dagq2dkqyn => loc_dagq2dkqyn.Id)
            .ToArray();
        return new Response(ids);
    }
}
