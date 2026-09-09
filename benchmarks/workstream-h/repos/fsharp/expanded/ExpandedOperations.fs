module ExpandedOperations

open System
open System.Collections.Generic
open System.Globalization
open System.Text.Json
open System.Text.RegularExpressions

type ReconcileRecord =
    { Id: string
      Priority: int
      CreatedAt: DateTimeOffset }

[<CLIMutable>]
type ReconcileItem =
    { id: string
      origin: string }

[<CLIMutable>]
type ReconcileResponse = { items: ReconcileItem array }

type private DependencyEdge = { Before: string; After: string }

let private property name (element: JsonElement) =
    element.EnumerateObject()
    |> Seq.tryFind (fun candidate ->
        String.Equals(candidate.Name, name, StringComparison.OrdinalIgnoreCase))
    |> Option.map (fun candidate -> candidate.Value)

let private sideArray side (element: JsonElement) =
    match element.ValueKind with
    | JsonValueKind.Undefined
    | JsonValueKind.Null -> [||]
    | JsonValueKind.Array -> element.EnumerateArray() |> Seq.toArray
    | _ -> raise (InvalidOperationException($"{side} must be an array"))

let private requiredString error name (element: JsonElement) =
    match property name element with
    | Some value when value.ValueKind = JsonValueKind.String ->
        value.GetString()
        |> Option.ofObj
        |> Option.defaultWith (fun () -> raise (InvalidOperationException(error)))
    | _ -> raise (InvalidOperationException(error))

let private integerPattern = Regex(@"^-?(0|[1-9][0-9]*)$", RegexOptions.CultureInvariant)

let private requiredInt32 error name (element: JsonElement) =
    match property name element with
    | Some value when value.ValueKind = JsonValueKind.Number ->
        let raw = value.GetRawText()
        let mutable parsed = 0

        if integerPattern.IsMatch(raw)
           && Int32.TryParse(raw, NumberStyles.AllowLeadingSign, CultureInfo.InvariantCulture, &parsed) then
            parsed
        else
            raise (InvalidOperationException(error))
    | _ -> raise (InvalidOperationException(error))

let private timestampPattern =
    Regex(
        @"^[0-9]{4}-(0[1-9]|1[0-2])-([0-2][0-9]|3[01])T([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9](\.[0-9]{1,7})?(Z|[+-](0[0-9]|1[0-3]):[0-5][0-9]|[+-]14:00)$",
        RegexOptions.CultureInvariant
    )

let private requiredTimestamp error name (element: JsonElement) =
    let text = requiredString error name element
    let mutable parsed = DateTimeOffset.MinValue

    if timestampPattern.IsMatch(text)
       && DateTimeOffset.TryParseExact(
           text,
           "yyyy-MM-dd'T'HH:mm:ss.FFFFFFFK",
           CultureInfo.InvariantCulture,
           DateTimeStyles.None,
           &parsed
       ) then
        parsed
    else
        raise (InvalidOperationException(error))

let private parseRecord side (element: JsonElement) =
    if element.ValueKind <> JsonValueKind.Object then
        raise (InvalidOperationException($"invalid {side} record"))

    { Id = requiredString $"invalid {side} id" "id" element
      Priority = requiredInt32 $"invalid {side} priority" "priority" element
      CreatedAt = requiredTimestamp $"invalid {side} createdAt" "createdAt" element }

let private rejectDuplicateRecordIds side records =
    let seen = HashSet<string>(StringComparer.Ordinal)

    if records |> Array.exists (fun record -> not (seen.Add(record.Id))) then
        raise (InvalidOperationException($"duplicate {side} id"))

let reconcile (leftElement: JsonElement) (rightElement: JsonElement) =
    let left = sideArray "left" leftElement |> Array.map (parseRecord "left")
    let right = sideArray "right" rightElement |> Array.map (parseRecord "right")
    rejectDuplicateRecordIds "left" left
    rejectDuplicateRecordIds "right" right

    let selected = Dictionary<string, ReconcileRecord * string>(StringComparer.Ordinal)

    for record in left do
        selected.Add(record.Id, (record, "left"))

    for record in right do
        match selected.TryGetValue(record.Id) with
        | true, (leftRecord, _) ->
            let preferRight =
                record.Priority > leftRecord.Priority
                || (record.Priority = leftRecord.Priority
                    && record.CreatedAt >= leftRecord.CreatedAt)

            if preferRight then
                selected[record.Id] <- (record, "right")
        | false, _ -> selected.Add(record.Id, (record, "right"))

    { items =
        selected
        |> Seq.map (fun pair -> pair.Key, snd pair.Value)
        |> Seq.sortWith (fun (leftId, _) (rightId, _) ->
            StringComparer.Ordinal.Compare(leftId, rightId))
        |> Seq.map (fun (id, origin) -> { id = id; origin = origin })
        |> Seq.toArray }

let private parseIds (element: JsonElement) =
    let ids =
        match element.ValueKind with
        | JsonValueKind.Undefined
        | JsonValueKind.Null -> [||]
        | JsonValueKind.Array ->
            element.EnumerateArray()
            |> Seq.map (fun value ->
                if value.ValueKind <> JsonValueKind.String then
                    raise (InvalidOperationException("invalid ids"))

                value.GetString())
            |> Seq.toArray
        | _ -> raise (InvalidOperationException("invalid ids"))

    let seen = HashSet<string>(StringComparer.Ordinal)

    if ids |> Array.exists (fun id -> not (seen.Add(id))) then
        raise (InvalidOperationException("duplicate id"))

    ids

let private parseEdges (element: JsonElement) =
    let rawEdges =
        match element.ValueKind with
        | JsonValueKind.Undefined
        | JsonValueKind.Null -> [||]
        | JsonValueKind.Array -> element.EnumerateArray() |> Seq.toArray
        | _ -> raise (InvalidOperationException("invalid edges"))

    let edges =
        rawEdges
        |> Array.map (fun edge ->
            if edge.ValueKind <> JsonValueKind.Object then
                raise (InvalidOperationException("invalid edge"))

            { Before = requiredString "invalid edge" "before" edge
              After = requiredString "invalid edge" "after" edge })

    let seen = HashSet<struct (string * string)>()

    if edges |> Array.exists (fun edge -> not (seen.Add(struct (edge.Before, edge.After)))) then
        raise (InvalidOperationException("duplicate edge"))

    edges

let dependencyOrder (idsElement: JsonElement) (edgesElement: JsonElement) =
    let ids = parseIds idsElement
    let edges = parseEdges edgesElement
    let known = HashSet<string>(ids, StringComparer.Ordinal)

    if edges |> Array.exists (fun edge -> not (known.Contains(edge.Before) && known.Contains(edge.After))) then
        raise (InvalidOperationException("unknown dependency"))

    if edges |> Array.exists (fun edge -> edge.Before = edge.After) then
        raise (InvalidOperationException("self dependency"))

    let indegree = Dictionary<string, int>(StringComparer.Ordinal)
    let outgoing = Dictionary<string, ResizeArray<string>>(StringComparer.Ordinal)

    for id in ids do
        indegree.Add(id, 0)
        outgoing.Add(id, ResizeArray())

    for edge in edges do
        outgoing[edge.Before].Add(edge.After)
        indegree[edge.After] <- indegree[edge.After] + 1

    let ready = SortedSet<string>(StringComparer.Ordinal)

    for id in ids do
        if indegree[id] = 0 then
            ready.Add(id) |> ignore

    let ordered = ResizeArray<string>()

    while ready.Count > 0 do
        let id = ready.Min
        ready.Remove(id) |> ignore
        ordered.Add(id)

        for dependent in outgoing[id] do
            indegree[dependent] <- indegree[dependent] - 1

            if indegree[dependent] = 0 then
                ready.Add(dependent) |> ignore

    if ordered.Count <> ids.Length then
        raise (InvalidOperationException("dependency cycle"))

    ordered.ToArray()
