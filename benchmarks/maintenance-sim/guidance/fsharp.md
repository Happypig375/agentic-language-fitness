# F# language guidance

Use the .NET 10.0.302 SDK and the flat `Simulation.fsproj` project. Keep the
program dependency-free and communicate through JSON Lines on standard input
and output using `System.Text.Json`. F# records, discriminated unions,
immutable maps, and small private functions are natural choices for modelling
state transitions and checked arithmetic. Preserve ordinal ordering and the
public wire contract exactly; do not add libraries, services, or runtime
configuration.
