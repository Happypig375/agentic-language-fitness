using System.Text.Json;

namespace OrderFlow;

public static class DependencyOrder
{
    private sealed record Edge(string Before, string After);

    public static object Run(JsonElement? idsElement, JsonElement? edgesElement)
    {
        var ids = ParseIds(idsElement);
        var edges = ParseEdges(edgesElement);
        var known = new HashSet<string>(ids, StringComparer.Ordinal);

        if (edges.Any(edge => !known.Contains(edge.Before) || !known.Contains(edge.After)))
        {
            throw new InvalidOperationException("unknown dependency");
        }

        if (edges.Any(edge => string.Equals(edge.Before, edge.After, StringComparison.Ordinal)))
        {
            throw new InvalidOperationException("self dependency");
        }

        var indegree = ids.ToDictionary(id => id, _ => 0, StringComparer.Ordinal);
        var outgoing = ids.ToDictionary(
            id => id,
            _ => new List<string>(),
            StringComparer.Ordinal);

        foreach (var edge in edges)
        {
            outgoing[edge.Before].Add(edge.After);
            indegree[edge.After]++;
        }

        var ready = new SortedSet<string>(
            ids.Where(id => indegree[id] == 0),
            StringComparer.Ordinal);
        var result = new List<string>();

        while (ready.Count > 0)
        {
            var id = ready.Min!;
            ready.Remove(id);
            result.Add(id);

            foreach (var dependent in outgoing[id])
            {
                indegree[dependent]--;
                if (indegree[dependent] == 0)
                {
                    ready.Add(dependent);
                }
            }
        }

        if (result.Count != ids.Length)
        {
            throw new InvalidOperationException("dependency cycle");
        }

        return new { ids = result.ToArray() };
    }

    private static string[] ParseIds(JsonElement? element)
    {
        if (!element.HasValue || element.Value.ValueKind == JsonValueKind.Null)
        {
            return [];
        }

        if (element.Value.ValueKind != JsonValueKind.Array)
        {
            throw new InvalidOperationException("invalid ids");
        }

        var result = new List<string>();
        foreach (var value in element.Value.EnumerateArray())
        {
            if (value.ValueKind != JsonValueKind.String)
            {
                throw new InvalidOperationException("invalid ids");
            }

            result.Add(value.GetString()!);
        }

        var seen = new HashSet<string>(StringComparer.Ordinal);
        if (result.Any(id => !seen.Add(id)))
        {
            throw new InvalidOperationException("duplicate id");
        }

        return result.ToArray();
    }

    private static Edge[] ParseEdges(JsonElement? element)
    {
        if (!element.HasValue || element.Value.ValueKind == JsonValueKind.Null)
        {
            return [];
        }

        if (element.Value.ValueKind != JsonValueKind.Array)
        {
            throw new InvalidOperationException("invalid edges");
        }

        var result = new List<Edge>();
        foreach (var value in element.Value.EnumerateArray())
        {
            if (value.ValueKind != JsonValueKind.Object
                || !TryString(value, "before", out var before)
                || !TryString(value, "after", out var after))
            {
                throw new InvalidOperationException("invalid edge");
            }

            result.Add(new Edge(before, after));
        }

        var seen = new HashSet<(string Before, string After)>();
        if (result.Any(edge => !seen.Add((edge.Before, edge.After))))
        {
            throw new InvalidOperationException("duplicate edge");
        }

        return result.ToArray();
    }

    private static bool TryString(JsonElement element, string name, out string value)
    {
        foreach (var property in element.EnumerateObject())
        {
            if (string.Equals(property.Name, name, StringComparison.OrdinalIgnoreCase)
                && property.Value.ValueKind == JsonValueKind.String)
            {
                value = property.Value.GetString()!;
                return true;
            }
        }

        value = "";
        return false;
    }
}

