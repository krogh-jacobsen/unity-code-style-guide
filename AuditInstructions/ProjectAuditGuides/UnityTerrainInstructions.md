# Unity terrain content audit

Load for owned Terrain/TerrainCollider/TerrainData, runtime height edits or terrain-tile streaming.
Apply the [shared evidence standard](ProjectReview.md#evidence-standard). Establish authoring tools,
data owners, tile layout, rendering pipeline and targets. Keep selected terrain/vegetation systems;
this lens reviews content correctness rather than prescribing a generator.
**Last verified: October 2026.**

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Tile boundaries | Actual edge heights, neighbor connections, grouping/auto-connect policy | A supported border has a seam or incorrect neighbor/LOD behavior; neighbor links alone do not repair authored height mismatches |
| Height synchronization | CPU/GPU/delayed height writes, supported sync path and subsequent consumers | A required CPU/LOD read observes stale terrain because delayed edits were not synchronized at the owning boundary |
| Collision agreement | TerrainCollider data/holes, visual terrain and live contacts/raycasts | Gameplay collision disagrees with required rendered geometry, including after runtime edits |
| Stream lifetime | Tile replacement/unload, neighbors, actors/navigation and resource ownership | Streaming leaves stale references, broken borders or actors without required collision; general ownership stays in [Scenes](UnityScenesAndLifecycleInstructions.md) |
| Shipped content | TerrainData, layers/materials, tree/detail prototypes and clean load | Missing/unsupported content changes intended terrain in a supported player; verify installed shader/platform support |
| Content scale | Height/detail/tree density, resolution/distances and measured budgets | A target capture exceeds the agreed memory/frame budget; fixed tile sizes or density prescriptions are proposals until measured |

## Interpret with care

Use the installed authoring tool and Editor APIs for asset changes. World generation, vegetation
packages, erosion and custom terrain shaders need their own source-matched review. Rendering cost,
lighting/LOD output and navigation correctness remain owned by their respective lenses; cross-link an
observed failure rather than counting those disciplines as reviewed here.

## Validation

Traverse borders/holes, inspect near/far views, test collision after runtime edits, stream tile cycles,
and reopen saved content. Validate shipped materials/prototypes in a representative player. Missing
live/player checks remain Not verified; a terrain screenshot alone proves neither collision nor streaming.

Technical references: [neighbor contract](https://docs.unity3d.com/ScriptReference/Terrain.SetNeighbors.html)
and [height synchronization](https://docs.unity3d.com/ScriptReference/TerrainData.SyncHeightmap.html).
These APIs support the boundary checks; exact generator settings and terrain budgets remain project choices.
