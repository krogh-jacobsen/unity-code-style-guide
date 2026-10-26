# Unity design audit

Load for responsibility, dependency, state-machine, or command-boundary review. Apply the
[shared evidence standard](ProjectReview.md#evidence-standard). Use `unity-project-review` for general
pitfall review when it is available; this guide stands alone and adds questions about actual ownership.

⚠️ Design findings are **proposals**, not defects, unless a rejected or repeated operation produces
wrong state. Report those two kinds separately: a confirmed defect carries the reproduced wrong state;
a proposal carries the countable trigger below plus its tradeoff.

## Establish the design

Read relevant domain documentation and recorded decisions. Map the command entry point, the owner
of its rules/state, composition, collaborators, and consumers. Trace representative success,
rejection, cancellation, and teardown paths. Judge complexity at the caller's interface, including
required setup and ordering, rather than by file size or interface count.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| One policy owner | The same rule in UI, simulation, preview, and save/load | Two implementations of the rule return different results for the same input, or one fix must be repeated in 2+ callers |
| Complete command | Validation, mutation, resource charging, registration, and events | A rejected operation leaves partial state, charges twice, or publishes success before commit |
| Valid state | Collection exposure and every mutation entry point | A public mutable collection or field is written outside its owner, or 3+ setters must run in a fixed order for the owner to be valid |
| State transitions | Allowed transitions, entry/exit effects, pending work | Re-entry, repeated requests, or interruption produces stale effects or an impossible state |
| Explicit dependencies | Constructors, serialized wiring, bootstrap, discovery calls | A consumer calls `Find*`, a static `Instance`, or `new` for a collaborator it does not own, or an initialization call skipped by a caller leaves the object throwing or half-working |
| Dependency direction | `.asmdef` reference lists, `using` directives, and serialized asset references of reusable (Core) code | A reusable assembly or namespace references game-specific content or presentation (count the references; each one is a candidate) |
| Useful abstractions | Callers and actual implementations | An interface or wrapper has one implementation, forwards every member one-to-one, and no second implementation, test double, or volatile boundary exists in the repository |
| Observable contracts | Return results, units, valid inputs, failure meanings | An operation returns `void` or a bare `bool` and N call sites read a field, catch an exception, or re-query state to learn whether it succeeded |

For a command that spends a resource and changes world state, trace the real entry point: a rejected
request must leave the resource, world state, and success events unchanged; a success must apply the
agreed effects exactly once. Adapt that check to the project's actual rules rather than introducing
a generic transaction framework.

## Interpret with care

- ℹ️ Composition-time injection can use concrete collaborators. Introduce an interface when it hides
  a volatile boundary or solves a demonstrated substitution/testing need.
- ℹ️ Direct calls suit owned collaborators; events suit observers. Audit event ownership and lifetime
  with [Scenes](UnityScenesAndLifecycleInstructions.md), rather than prescribing a global event bus.
- ℹ️ An enum/switch can be the clearest state machine. Recommend classes only when they reduce
  transition or per-state complexity. A singleton's risk is hidden scope/lifetime, not its name.
- ℹ️ ScriptableObject configuration and runtime state need explicit ownership; see
  [Assets](UnityAssetsAndMemoryInstructions.md). Shared event-channel assets need a session reset contract.
- ℹ️ Consolidation and deletion may improve a design more than splitting another manager. Preserve
  existing behavior and serialized identity when changing ownership.

## Recommendation

For each proposal, name the current owner, intended owner, smallest interface, concrete benefit, and
migration cost. State that crossing a save boundary belongs to
[Persistence](UnityPersistenceInstructions.md). A proposal is complete as an audit result when its
evidence and tradeoff are clear; implementation belongs to the selected follow-up work.
