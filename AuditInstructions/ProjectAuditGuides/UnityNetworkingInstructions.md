# Unity networking and multiplayer audit

Load for owned replication, RPCs, network/session objects or multiplayer lifecycle. Apply the
[shared evidence standard](ProjectReview.md#evidence-standard). Establish topology, trusted authority,
package/transport versions, session ownership, targets, and authoritative game rules first. NGO examples
are conditional; third-party stacks and distributed authority need their own installed contracts.
**Last verified: October 2026.**

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Authority/request validation | Receive-side sender identity, object permission, ranges, rule validation, repeated requests | An untrusted peer can mutate another owner's state or authorize impossible effects; a client-supplied identity alone is not proof of authority |
| Durable state | Spawn/late-join initialization, current replicated state versus transient events | A late/reconnected player misses required persistent state because it existed only in past RPCs; a transient effect need not be replayed |
| Network lifetime | Spawn/despawn, subscription ownership, pool reuse, transfer/disconnect/shutdown | A stale owner/callback acts after despawn, a pool checkout inherits a prior network identity, or shutdown/restart leaves session state behind |
| Delivery/order | Reliability, ordering scope, local/remote execution, tick/time units, prediction if used | Required behavior depends on delivery/order not guaranteed by the installed transport/package, or host and remote paths apply effects differently |
| Connection trust | Authentication versus approval, payload, actual transport protection, credential/log lifetime | Untrusted approval data authorizes a session, or sensitive payload is exposed by the actual protection/logging path; approval alone is not authentication |
| Failure/recovery | Timeout, disconnect, failed join, overlapping session requests, reconnection policy | Failure strands loading/input/session ownership or reconnect duplicates committed state; general async ownership stays in [Scenes](UnityScenesAndLifecycleInstructions.md) |

## Interpret with care

Authority is a topology choice, not a universal server-only prescription. NGO NetworkVariables sync
current state to late joiners; RPCs are transient. Permissions, receive metadata, local RPC timing and
ordering vary by package/version. Treat payloads as untrusted at the authority boundary, even when a
caller-side UI validates them. Retry/deduplication policies should match command semantics rather than
adding a generic distributed transaction framework. Bandwidth/tick changes need measured workloads.

## Validation

Use real remote clients as well as host mode: join in progress, reconnect, transfer/disconnect owners,
despawn/reuse, shutdown/restart, invalid and repeated requests. Add representative latency, jitter and
loss with supported network simulation. Verify authority and exactly-once outcomes, not only smooth
local presentation. Keep missing multi-process/device/backend checks Not verified. This lens is not a
penetration test; backend infrastructure, service authorization and Netcode for Entities prediction
need separately scoped specialist review.

Technical references: [NGO state and late joining](https://docs.unity3d.com/Packages/com.unity.netcode.gameobjects@latest/index.html?subfolder=/manual/basics/networkvariable.html),
[RPC identity/timing](https://docs.unity3d.com/Packages/com.unity.netcode.gameobjects@latest/index.html?subfolder=/manual/advanced-topics/message-system/rpc.html), and
[approval protection limits](https://docs.unity3d.com/Packages/com.unity.netcode.gameobjects@latest/index.html?subfolder=/manual/basics/connection-approval.html).
Research inspected NGO 3.1.0; verify the project's actual package/topology before applying API claims.
