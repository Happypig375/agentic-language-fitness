using System.Globalization;
using System.Text.Json;
using System.Text.RegularExpressions;

namespace OrderFlow;

public static class Reconcile
{
    private static readonly Regex IntegerPattern = new(
        "^-?(0|[1-9][0-9]*)$",
        RegexOptions.CultureInvariant);

    private static readonly Regex TimestampPattern = new(
        "^[0-9]{4}-(0[1-9]|1[0-2])-([0-2][0-9]|3[01])T([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\\.[0-9]{1,7})?(Z|[+-](0[0-9]|1[0-3]):[0-5][0-9]|[+-]14:00)$",
        RegexOptions.CultureInvariant);

    private sealed record Candidate(string Id, int Priority, DateTimeOffset CreatedAt);

    public static object Run(JsonElement? left, JsonElement? right)
    {
        var leftValues = ValidateSide(left, "left");
        var rightValues = ValidateSide(right, "right");
        EnsureUnique(leftValues, "left");
        EnsureUnique(rightValues, "right");

        var winners = new Dictionary<string, (Candidate Value, string Origin)>(StringComparer.Ordinal);
        foreach (var value in leftValues)
        {
            winners.Add(value.Id, (value, "left"));
        }

        foreach (var value in rightValues)
        {
            if (!winners.TryGetValue(value.Id, out var prior) || Better(value, prior.Value))
            {
                winners[value.Id] = (value, "right");
            }
        }

        return new
        {
            items = winners
                .OrderBy(pair => pair.Key, StringComparer.Ordinal)
                .Select(pair => new { id = pair.Key, origin = pair.Value.Origin })
                .ToArray()
        };
    }

    private static Candidate[] ValidateSide(JsonElement? element, string side)
    {
        if (!element.HasValue || element.Value.ValueKind == JsonValueKind.Null)
        {
            return [];
        }

        if (element.Value.ValueKind != JsonValueKind.Array)
        {
            throw new InvalidOperationException($"{side} must be an array");
        }

        var result = new List<Candidate>();
        foreach (var record in element.Value.EnumerateArray())
        {
            if (record.ValueKind != JsonValueKind.Object)
            {
                throw new InvalidOperationException($"invalid {side} record");
            }

            result.Add(Parse(record, side));
        }

        return result.ToArray();
    }

    private static Candidate Parse(JsonElement record, string side)
    {
        if (!TryProperty(record, "id", out var id) || id.ValueKind != JsonValueKind.String)
        {
            throw new InvalidOperationException($"invalid {side} id");
        }

        if (!TryProperty(record, "priority", out var priority)
            || priority.ValueKind != JsonValueKind.Number
            || !IntegerPattern.IsMatch(priority.GetRawText())
            || !int.TryParse(
                priority.GetRawText(),
                NumberStyles.AllowLeadingSign,
                CultureInfo.InvariantCulture,
                out var number))
        {
            throw new InvalidOperationException($"invalid {side} priority");
        }

        if (!TryProperty(record, "createdAt", out var created)
            || created.ValueKind != JsonValueKind.String
            || !TryTimestamp(created.GetString()!, out var instant))
        {
            throw new InvalidOperationException($"invalid {side} createdAt");
        }

        return new Candidate(id.GetString()!, number, instant);
    }

    private static bool TryTimestamp(string value, out DateTimeOffset result)
    {
        result = default;
        return TimestampPattern.IsMatch(value)
            && DateTimeOffset.TryParseExact(
                value,
                "yyyy-MM-dd'T'HH:mm:ss.FFFFFFFK",
                CultureInfo.InvariantCulture,
                DateTimeStyles.None,
                out result);
    }

    private static bool TryProperty(JsonElement element, string name, out JsonElement value)
    {
        foreach (var property in element.EnumerateObject())
        {
            if (string.Equals(property.Name, name, StringComparison.OrdinalIgnoreCase))
            {
                value = property.Value;
                return true;
            }
        }

        value = default;
        return false;
    }

    private static void EnsureUnique(IEnumerable<Candidate> values, string side)
    {
        var seen = new HashSet<string>(StringComparer.Ordinal);
        foreach (var value in values)
        {
            if (!seen.Add(value.Id))
            {
                throw new InvalidOperationException($"duplicate {side} id");
            }
        }
    }

    private static bool Better(Candidate candidate, Candidate prior) =>
        candidate.Priority > prior.Priority
        || candidate.Priority == prior.Priority && candidate.CreatedAt >= prior.CreatedAt;
}
