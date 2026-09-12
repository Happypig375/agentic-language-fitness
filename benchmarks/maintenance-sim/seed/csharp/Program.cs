using System.Text.Json;
using System.Text.RegularExpressions;

namespace Simulation;

public sealed record Mover(string Id, long X, long Velocity);
public sealed record Saved(long Tick, Dictionary<string, Mover> Entities);

public sealed class World
{
    public long Tick;
    public Dictionary<string, Mover> Entities = new(StringComparer.Ordinal);
    public Dictionary<string, Saved> Snapshots = new(StringComparer.Ordinal);
    public List<string> Effects = [];
    public List<string> Errors = [];

    public World Copy() => new()
    {
        Tick = Tick,
        Entities = Entities.ToDictionary(x => x.Key, x => x.Value with { }, StringComparer.Ordinal),
        Snapshots = Snapshots.ToDictionary(x => x.Key,
            x => new Saved(x.Value.Tick, x.Value.Entities.ToDictionary(y => y.Key, y => y.Value with { }, StringComparer.Ordinal)), StringComparer.Ordinal),
        Effects = [.. Effects], Errors = [.. Errors]
    };
}

public static partial class Program
{
    private static readonly JsonSerializerOptions JsonOptions = new() { WriteIndented = false };
    private static readonly Regex IdPattern = IdRegex();

    public static void Main()
    {
        string? line;
        while ((line = Console.ReadLine()) is not null)
        {
            if (string.IsNullOrWhiteSpace(line)) continue;
            Console.WriteLine(Handle(line));
        }
    }

    public static string Handle(string input)
    {
        World world = new();
        try
        {
            using JsonDocument doc = JsonDocument.Parse(input);
            if (!ValidRequest(doc.RootElement, out JsonElement operations)) return Serialize(new World { Errors = ["invalid_shape"] });
            for (int i = 0; i < operations.GetArrayLength(); i++) Apply(world, operations[i]);
        }
        catch (JsonException) { return Serialize(new World { Errors = ["invalid_shape"] }); }
        return Serialize(world);
    }

    private static bool ValidRequest(JsonElement root, out JsonElement operations)
    {
        operations = default;
        if (root.ValueKind != JsonValueKind.Object || root.EnumerateObject().Count() != 2 ||
            !root.TryGetProperty("version", out JsonElement version) || !root.TryGetProperty("operations", out operations) ||
            version.ValueKind != JsonValueKind.Number || !Integer(version, out long v) || v != 1 ||
            operations.ValueKind != JsonValueKind.Array || operations.GetArrayLength() > 256) return false;
        return true;
    }

    private static void Apply(World world, JsonElement operation)
    {
        if (operation.ValueKind != JsonValueKind.Object) { world.Errors.Add("invalid_shape"); return; }
        if (!operation.TryGetProperty("op", out JsonElement op) || op.ValueKind != JsonValueKind.String) { world.Errors.Add("invalid_shape"); return; }
        string name = op.GetString()!;
        if (name is not ("spawn" or "remove" or "tick" or "save" or "load")) { world.Errors.Add("unknown_operation"); return; }
        if (!ShapeIsValid(operation, name)) { world.Errors.Add("invalid_shape"); return; }
        World next = world.Copy();
        try
        {
            switch (name)
            {
                case "spawn": Spawn(next, operation); break;
                case "remove": Remove(next, operation); break;
                case "tick": Tick(next, operation); break;
                case "save": Save(next, operation); break;
                case "load": Load(next, operation); break;
            }
            world.Tick = next.Tick; world.Entities = next.Entities; world.Snapshots = next.Snapshots;
            world.Effects = next.Effects; world.Errors = next.Errors;
        }
        catch (OpError e) { world.Errors.Add(e.Code); }
        catch (OverflowException) { world.Errors.Add("overflow"); }
    }

    private static void Spawn(World w, JsonElement o)
    {
        RequireKeys(o, "op", "id", "x", "velocity"); string id = StringField(o, "id"); long x = NumberField(o, "x"), velocity = NumberField(o, "velocity");
        if (!IdPattern.IsMatch(id) || x is < -1_000_000 or > 1_000_000 || velocity is < -1_000_000 or > 1_000_000) throw new OpError("invalid_value");
        if (w.Entities.ContainsKey(id)) throw new OpError("duplicate_id");
        w.Entities[id] = new(id, x, velocity); w.Effects.Add($"spawn:{id}");
    }
    private static void Remove(World w, JsonElement o)
    {
        RequireKeys(o, "op", "id"); string id = StringField(o, "id"); if (!IdPattern.IsMatch(id)) throw new OpError("invalid_value");
        if (!w.Entities.Remove(id)) throw new OpError("missing_entity"); w.Effects.Add($"remove:{id}");
    }
    private static void Tick(World w, JsonElement o)
    {
        RequireKeys(o, "op", "count"); long count = NumberField(o, "count"); if (count is < 1 or > 1000) throw new OpError("invalid_value");
        long t = checked(w.Tick + count); var moved = new Dictionary<string, Mover>(StringComparer.Ordinal);
        foreach (var (id, entity) in w.Entities) moved[id] = entity with { X = checked(entity.X + checked(entity.Velocity * count)) };
        w.Tick = t; w.Entities = moved; w.Effects.Add($"tick:{count}");
    }
    private static void Save(World w, JsonElement o)
    {
        RequireKeys(o, "op", "name"); string name = NameField(o, "name");
        w.Snapshots[name] = new(w.Tick, w.Entities.ToDictionary(x => x.Key, x => x.Value with { }, StringComparer.Ordinal)); w.Effects.Add($"save:{name}");
    }
    private static void Load(World w, JsonElement o)
    {
        RequireKeys(o, "op", "name"); string name = NameField(o, "name"); if (!w.Snapshots.TryGetValue(name, out var saved)) throw new OpError("missing_snapshot");
        w.Tick = saved.Tick; w.Entities = saved.Entities.ToDictionary(x => x.Key, x => x.Value with { }, StringComparer.Ordinal); w.Effects.Add($"load:{name}");
    }

    private static string StringField(JsonElement o, string key) { if (!o.TryGetProperty(key, out var x) || x.ValueKind != JsonValueKind.String) throw new OpError("invalid_shape"); return x.GetString()!; }
    private static string NameField(JsonElement o, string key) { string x = StringField(o, key); if (!IdPattern.IsMatch(x)) throw new OpError("invalid_value"); return x; }
    private static long NumberField(JsonElement o, string key) { if (!o.TryGetProperty(key, out var x) || x.ValueKind != JsonValueKind.Number || !Integer(x, out long n)) throw new OpError(x.ValueKind == JsonValueKind.Number ? "invalid_value" : "invalid_shape"); return n; }
    private static bool Integer(JsonElement x, out long value) { string raw = x.GetRawText(); return long.TryParse(raw, System.Globalization.NumberStyles.AllowLeadingSign, System.Globalization.CultureInfo.InvariantCulture, out value) && raw.IndexOfAny('.', 'e', 'E') < 0; }
    private static void RequireKeys(JsonElement o, params string[] keys) { if (o.EnumerateObject().Count() != keys.Length || keys.Any(k => !o.TryGetProperty(k, out _))) throw new OpError("invalid_shape"); }
    private static bool ShapeIsValid(JsonElement o, string name)
    {
        string[] fields = name switch { "spawn" => ["op", "id", "x", "velocity"], "remove" => ["op", "id"], "tick" => ["op", "count"], _ => ["op", "name"] };
        if (o.EnumerateObject().Count() != fields.Length || fields.Any(field => !o.TryGetProperty(field, out _))) return false;
        if (o.GetProperty("op").ValueKind != JsonValueKind.String) return false;
        if (name == "spawn") return o.GetProperty("id").ValueKind == JsonValueKind.String && o.GetProperty("x").ValueKind == JsonValueKind.Number && o.GetProperty("velocity").ValueKind == JsonValueKind.Number;
        if (name == "remove") return o.GetProperty("id").ValueKind == JsonValueKind.String;
        if (name == "tick") return o.GetProperty("count").ValueKind == JsonValueKind.Number;
        return o.GetProperty("name").ValueKind == JsonValueKind.String;
    }
    private static string Serialize(World w)
    {
        var result = new { version = 1, state = new { tick = w.Tick, entities = w.Entities.OrderBy(x => x.Key, StringComparer.Ordinal).Select(x => new { id = x.Value.Id, x = x.Value.X, velocity = x.Value.Velocity }) }, effects = w.Effects, errors = w.Errors,
            snapshots = w.Snapshots.OrderBy(x => x.Key, StringComparer.Ordinal).Select(x => new { name = x.Key, tick = x.Value.Tick, entities = x.Value.Entities.OrderBy(y => y.Key, StringComparer.Ordinal).Select(y => new { id = y.Value.Id, x = y.Value.X, velocity = y.Value.Velocity }) }) };
        return JsonSerializer.Serialize(result, JsonOptions);
    }
    private sealed class OpError(string code) : Exception { public string Code { get; } = code; }
    [GeneratedRegex(@"\A[a-z][a-z0-9_-]{0,31}\z")] private static partial Regex IdRegex();
}
