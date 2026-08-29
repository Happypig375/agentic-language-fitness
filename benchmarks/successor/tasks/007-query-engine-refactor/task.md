# Extract the OrderFlow engine

Refactor the application without changing behavior:

- move the domain model and live operation dispatch out of `Program.cs` or `Program.fs`;
- place them in `OrderFlowEngine.cs` or `OrderFlowEngine.fs`, respectively;
- leave `Program` responsible only for line input/output, JSON adaptation, error adaptation, and calling the engine;
- preserve every existing request, response, validation error, ordering rule, and stateless behavior.

The F# project must compile `OrderFlowEngine.fs` before `Program.fs`. The evaluator checks cumulative black-box behavior and a narrow workspace contract covering the engine file, live engine call, prohibited model/handler declarations in Program, and known operation literals in Program. These checks are minimum modularization evidence; the live design must still place the model and dispatch in the engine.
