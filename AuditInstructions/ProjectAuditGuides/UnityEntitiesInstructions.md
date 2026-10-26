# Unity Entities correctness audit

Load for owned Entities systems/jobs, bakers, EntityCommandBuffers or SubScenes. Apply the
[shared evidence standard](ProjectReview.md#evidence-standard). Establish package version, worlds,
system groups, player/baking paths and resource owners. Installed Entities alone is weak evidence.
**Last verified: October 2026.**

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| World/order | Effective world/group, creation versus update order, producer/consumer dependencies | A required producer is absent or runs too late; relative update attributes are assumed to constrain systems outside their supported same-group scope |
| Job dependencies | Scheduled handles, reads/writes, state dependency propagation and completion | Data is consumed/disposed while a job still uses it, or a required dependency is lost; Complete alone is not a defect |
| Deferred entity scope | ECB temporary entities and their consumers | A temporary entity is used with EntityManager or another ECB before valid playback remapping |
| Playback visibility | Producer completion, ECB playback/disposal and downstream consumers | Playback races a producer or a consumer expects structural changes before they become visible |
| Resource/world lifetime | Native containers, world/system creation and teardown, repeated Play | Owned resources survive beyond their intended world/session, are disposed twice, or remain in use at disposal |
| Baked/shipped state | Required components/references in authored SubScenes versus clean player load | Live baking masks missing runtime components/content or a player consumes invalid entity references |

## Interpret with care

Creation order and update order are different contracts. Inspect the actual world and group tree;
attributes alone are not proof. ECBs defer structural changes and have their own entity scope and
playback lifetime. Framework-managed cleanup can satisfy ownership; do not demand a second disposal
path. General native-container cost belongs in [Performance](UnityPerformanceOptimizationInstructions.md).
DOTS Physics contacts/step ordering and Netcode for Entities prediction/ghost baking exceed this
lens; record those specialist checks Outside coverage unless separately reviewed.

## Validation

Inspect the actual Systems window/order, use available safety/race checks, and exercise spawn/despawn,
world disposal/recreation and SubScene unload/reload. Validate required baked content in a normal
player. Static scheduling inspection does not prove race freedom; absent live/build checks are Not verified.

Technical references: [system groups/order](https://docs.unity3d.com/Packages/com.unity.entities@latest/index.html?subfolder=/manual/systems-update-order.html),
[ECB scope and safety](https://docs.unity3d.com/Packages/com.unity.entities@latest/index.html?subfolder=/manual/systems-entity-command-buffers.html), and
[job scheduling](https://docs.unity3d.com/Packages/com.unity.entities@latest/index.html?subfolder=/manual/systems-scheduling-jobs.html).
Research inspected Entities 1.3.15; newer package behavior must be matched to installed source.
