# Unity localization and accessibility audit

Load for supported languages/localization readiness, or player-facing UI, controls and information.
Apply the [shared evidence standard](ProjectReview.md#evidence-standard). Establish supported locales,
platforms, input methods, font/UI systems, and adopted accessibility requirements. Localization and
accessibility are distinct: one language can still have access barriers, and a package install solves
neither by itself. **Last verified: October 2026.**

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Content/fallback | Supported locale tables or custom store, text/images/audio, fallback policy | Supported content exposes keys/blanks/wrong assets or lacks the agreed fallback; a missing cell with a valid regional fallback is not itself a defect |
| Formatting | Sentence templates, arguments, plurals, number/date/currency culture | Supported language/count/value produces wrong meaning or formatting errors; equivalent custom formatting is valid |
| Locale lifetime | Initialization, subscriptions, refresh, pending load and locale replacement | Cold startup assumes unavailable data, old results overwrite a newer locale, or visible content fails to refresh; Web startup must not rely on synchronous Localization initialization |
| Script/layout coverage | Glyph fallback, shaping/direction, text expansion, rendered controls | A supported script is missing/incorrect, essential text clips, or text growth makes controls unusable at supported sizes |
| Perceptible information | Essential audio/color cues, subtitles, captions and source/speaker identity | A supported task requires information unavailable through the player's supported settings/input; document the concrete barrier and equivalent cue |
| Operable interaction | Focus/navigation, remapping, hold/mash/drag demands, supported devices | A required task cannot be completed using a supported control path or adopted access option; broader options remain proposals with their audience/tradeoff |
| Readability/comfort | Actual text/backgrounds, scaling, motion/shake/bob and cinematic settings | A demonstrated barrier or adopted requirement fails; numeric contrast/size targets follow the adopted standard and element category |
| Settings ownership | Accessibility/locale values, runtime application, restart and view recreation | An offered setting is inaccessible, lost, or does not change the intended behavior; storage checks belong to [Persistence](UnityPersistenceInstructions.md) |

## Interpret with care

Pseudo-localization screens expansion, untranslated content and formatting issues; it does not prove
real translation, shaping or right-to-left correctness. Test actual supported scripts. Subtitles cover
dialogue; captions can also convey essential non-speech sounds. Assess real gameplay backgrounds,
controls and information rather than the existence of a checkbox. Use platform-owner accessibility
guidelines as a review source; this lens is not legal or platform certification. Classify unadopted
improvements as proposals and state who benefits. UI wiring and input arbitration stay in their lenses.

## Validation

Cold-start, switch locale rapidly, reopen views, remove a translation, and test fallback in a player.
Exercise representative plurals, largest supported text and real supported languages at target sizes.
Complete representative tasks muted, without color differentiation, and through supported alternate
controls. Verify focus restoration and settings after restart. Record absent device/user testing Not verified.

Technical references: [pseudo-localization](https://docs.unity3d.com/Packages/com.unity.localization@latest/index.html?subfolder=/manual/Pseudo-Localization.html),
[locale refresh](https://docs.unity3d.com/Packages/com.unity.localization@latest/index.html?subfolder=/manual/Scripting.html),
[formatting](https://docs.unity3d.com/Packages/com.unity.localization@latest/index.html?subfolder=/manual/Smart/SmartStrings.html),
[initialization/platform limits](https://docs.unity3d.com/Packages/com.unity.localization@latest/index.html?subfolder=/api/UnityEngine.Localization.Settings.LocalizationSettings.html), and
[Xbox Accessibility Guidelines](https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/).
Match the installed implementation; research inspected Localization 1.5.13. Platform guidelines are
recommendations unless the project has adopted them as requirements.
