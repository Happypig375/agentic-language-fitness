module Simulation

open System
open System.IO
open System.Text.Json
open System.Text.RegularExpressions
open System.Collections.Generic

type Entity = { Id: string; X: int64; Velocity: int64 }
type Snapshot = { Tick: int64; Entities: Map<string, Entity> }
type World = { Tick: int64; Entities: Map<string, Entity>; Snapshots: Map<string, Snapshot>; Effects: string list; Errors: string list }

let empty = { Tick = 0L; Entities = Map.empty; Snapshots = Map.empty; Effects = []; Errors = [] }
let idPattern = Regex("\A[a-z][a-z0-9_-]{0,31}\z", RegexOptions.CultureInvariant)

let private props (e: JsonElement) = e.EnumerateObject() |> Seq.map (fun p -> p.Name) |> Set.ofSeq
let private exact (expected: string list) (e: JsonElement) =
    let names = props e
    names.Count = expected.Length && expected |> List.forall names.Contains
let private stringField (name: string) (e: JsonElement) =
    match e.TryGetProperty(name) with | true, v when v.ValueKind = JsonValueKind.String -> Some (v.GetString()) | _ -> None
let private integerField (name: string) (e: JsonElement) =
    match e.TryGetProperty(name) with
    | true, v when v.ValueKind = JsonValueKind.Number && Regex.IsMatch(v.GetRawText(), "^-?(0|[1-9][0-9]*)$") ->
        let raw = v.GetRawText()
        match Int64.TryParse(raw, Globalization.NumberStyles.AllowLeadingSign, Globalization.CultureInfo.InvariantCulture) with | true, n -> Some n | _ -> None
    | _ -> None
let private validId (s: string) = idPattern.IsMatch(s)
let private inRange n = n >= -1000000L && n <= 1000000L
let private fieldHasKind (name: string) (kind: JsonValueKind) (e: JsonElement) =
    match e.TryGetProperty(name) with | true, value -> value.ValueKind = kind | _ -> false
let private fieldsHaveKinds (fields: (string * JsonValueKind) list) (e: JsonElement) =
    fields |> List.forall (fun (name, kind) -> fieldHasKind name kind e)
let private sortedEntities (m: Map<string, Entity>) = m |> Map.toList |> List.sortWith (fun (a,_) (b,_) -> StringComparer.Ordinal.Compare(a,b)) |> List.map snd
let private sortedSnapshots (m: Map<string, Snapshot>) = m |> Map.toList |> List.sortWith (fun (a,_) (b,_) -> StringComparer.Ordinal.Compare(a,b))

let private addError code w = { w with Errors = w.Errors @ [code] }
let private addEffect effect w = { w with Effects = w.Effects @ [effect] }

let private tickWorld count w =
    try
        let mutable entities = w.Entities
        let mutable tick = w.Tick
        for _ in 1 .. int count do
            entities <- entities |> Map.map (fun _ e -> { e with X = e.X + e.Velocity })
            tick <- tick + 1L
        Ok { w with Tick = tick; Entities = entities }
    with :? OverflowException -> Error ()

let private operation (op: JsonElement) (w: World) : Result<World,string> =
    if op.ValueKind <> JsonValueKind.Object || not (op.TryGetProperty("op") |> fst) then Error "invalid_shape"
    else
        match stringField "op" op with
        | None -> Error "invalid_shape"
        | Some name ->
            let shape expected = if exact expected op then Ok () else Error "invalid_shape"
            match name with
            | "spawn" ->
                match shape ["op";"id";"x";"velocity"] with
                | Error e -> Error e
                | Ok () ->
                    if not (fieldsHaveKinds ["op",JsonValueKind.String; "id",JsonValueKind.String; "x",JsonValueKind.Number; "velocity",JsonValueKind.Number] op) then Error "invalid_shape"
                    else
                        match stringField "id" op, integerField "x" op, integerField "velocity" op with
                        | Some id, Some x, Some velocity when validId id && inRange x && inRange velocity ->
                            if w.Entities.ContainsKey id then Error "duplicate_id"
                            else Ok (addEffect ("spawn:" + id) { w with Entities = w.Entities.Add(id,{Id=id;X=x;Velocity=velocity}) })
                        | _ -> Error "invalid_value"
            | "remove" ->
                match shape ["op";"id"] with
                | Error e -> Error e
                | Ok () ->
                    if not (fieldsHaveKinds ["op",JsonValueKind.String; "id",JsonValueKind.String] op) then Error "invalid_shape"
                    else
                        match stringField "id" op with
                        | Some id when validId id ->
                            if w.Entities.ContainsKey id then Ok (addEffect ("remove:"+id) {w with Entities=w.Entities.Remove id})
                            else Error "missing_entity"
                        | _ -> Error "invalid_value"
            | "tick" ->
                match shape ["op";"count"] with
                | Error e -> Error e
                | Ok () ->
                    if not (fieldsHaveKinds ["op",JsonValueKind.String; "count",JsonValueKind.Number] op) then Error "invalid_shape"
                    else
                        match integerField "count" op with
                        | Some n when n >= 1L && n <= 1000L ->
                            match tickWorld n w with
                            | Ok next -> Ok (addEffect ("tick:"+string n) next)
                            | Error () -> Error "overflow"
                        | _ -> Error "invalid_value"
            | "save" ->
                match shape ["op";"name"] with
                | Error e -> Error e
                | Ok () ->
                    if not (fieldsHaveKinds ["op",JsonValueKind.String; "name",JsonValueKind.String] op) then Error "invalid_shape"
                    else
                        match stringField "name" op with
                        | Some n when validId n ->
                            let snapshot = { Tick = w.Tick; Entities = w.Entities }
                            Ok (addEffect ("save:"+n) { w with Snapshots = w.Snapshots.Add(n, snapshot) })
                        | _ -> Error "invalid_value"
            | "load" ->
                match shape ["op";"name"] with
                | Error e -> Error e
                | Ok () ->
                    if not (fieldsHaveKinds ["op",JsonValueKind.String; "name",JsonValueKind.String] op) then Error "invalid_shape"
                    else
                        match stringField "name" op with
                        | Some n when validId n ->
                            match w.Snapshots.TryFind n with
                            | Some s -> Ok (addEffect ("load:"+n) { w with Tick = s.Tick; Entities = s.Entities })
                            | None -> Error "missing_snapshot"
                        | _ -> Error "invalid_value"
            | _ -> Error "unknown_operation"

let private writeEntity (j: Utf8JsonWriter) e =
    j.WriteStartObject(); j.WriteString("id",e.Id); j.WriteNumber("x",e.X); j.WriteNumber("velocity",e.Velocity); j.WriteEndObject()
let private response (w: World) =
    use stream = new MemoryStream()
    use j = new Utf8JsonWriter(stream)
    j.WriteStartObject(); j.WriteNumber("version",1); j.WriteStartObject("state"); j.WriteNumber("tick",w.Tick); j.WriteStartArray("entities"); sortedEntities w.Entities |> List.iter (writeEntity j); j.WriteEndArray(); j.WriteEndObject()
    j.WriteStartArray("effects"); w.Effects |> List.iter j.WriteStringValue; j.WriteEndArray(); j.WriteStartArray("errors"); w.Errors |> List.iter j.WriteStringValue; j.WriteEndArray(); j.WriteStartArray("snapshots")
    sortedSnapshots w.Snapshots |> List.iter (fun (name,s) -> j.WriteStartObject(); j.WriteString("name",name); j.WriteNumber("tick",s.Tick); j.WriteStartArray("entities"); sortedEntities s.Entities |> List.iter (writeEntity j); j.WriteEndArray(); j.WriteEndObject())
    j.WriteEndArray(); j.WriteEndObject(); j.Flush(); Text.Encoding.UTF8.GetString(stream.ToArray())

let private handle (line: string) =
    try
        use doc = JsonDocument.Parse(line)
        let root = doc.RootElement
        if root.ValueKind <> JsonValueKind.Object || not (exact ["version";"operations"] root) then
            response (addError "invalid_shape" empty)
        else
            let version = root.GetProperty("version")
            let ops = root.GetProperty("operations")
            if version.ValueKind = JsonValueKind.Number && Regex.IsMatch(version.GetRawText(), "^-?(0|[1-9][0-9]*)$") && version.GetInt64() = 1L && ops.ValueKind = JsonValueKind.Array && Seq.length (ops.EnumerateArray()) <= 256 then
                let mutable world = empty
                for op in ops.EnumerateArray() do
                    match operation op world with | Ok next -> world <- next | Error code -> world <- addError code world
                response world
            else
                response (addError "invalid_shape" empty)
    with _ -> response (addError "invalid_shape" empty)

[<EntryPoint>]
let main _ =
    let mutable line = Console.ReadLine()
    while not (isNull line) do
        if not (String.IsNullOrWhiteSpace line) then Console.WriteLine(handle (line.TrimStart([| '\uFEFF' |])))
        line <- Console.ReadLine()
    0
