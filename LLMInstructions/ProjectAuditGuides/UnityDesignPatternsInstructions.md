# Unity design audit

Load for responsibility, dependency, state-machine, or command-boundary review. Apply the
[shared evidence standard](ProjectReview.md#evidence-standard). Use `codebase-design` for design work and
`unity-project-review` for general pitfall review; this guide adds questions about actual ownership.

## Establish the design

Read relevant domain documentation and recorded decisions. Map the command entry point, the owner
of its rules/state, composition, collaborators, and consumers. Trace representative success,
rejection, cancellation, and teardown paths. Judge complexity at the caller's interface, including
required setup and ordering, rather than by file size or interface count.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| One policy owner | The same rule in UI, simulation, preview, and save/load | Implementations disagree, or a fix must be repeated across callers |
| Complete command | Validation, mutation, resource charging, registration, and events | A rejected operation leaves partial state, charges twice, or publishes success before commit |
| Valid state | Collection exposure and every mutation entry point | Callers bypass invariants or configure an owner through several order-sensitive setters |
| Explicit dependencies | Constructors, serialized wiring, bootstrap, discovery calls | A consumer discovers/recreates services or depends on undocumented initialization order |
| Dependency direction | Source and serialized asset references, including reusable Core | Reusable logic depends on game-specific content or presentation without an intentional boundary |
| Useful abstractions | Callers and actual implementations | A wrapper exposes the same complexity as its internals, or a speculative framework has no current need |
| State transitions | Allowed transitions, entry/exit effects, pending work | Re-entry, repeated requests, or interruption produces stale effects or an impossible state |
| Observable contracts | Return results, units, valid inputs, failure meanings | Callers cannot distinguish rejection from success or must inspect internals to use the operation |

For a purchase/build command, trace the real entry point: insufficient funds must leave money,
world state, and success events unchanged; success must apply the agreed effects exactly once.
Adapt that example to the project's actual rules rather than introducing a generic transaction framework.

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

## Validation and recommendation

For each proposal, name the current owner, intended owner, smallest interface, concrete benefit,
and migration cost. Exercise the real command boundary using [Testing](UnityTestingInstructions.md),
including rejected and repeated operations. Use [Persistence](UnityPersistenceInstructions.md) when
state crosses a save boundary. A design proposal is complete as an audit result when its evidence
and tradeoff are clear; implementation belongs to the selected follow-up work.
