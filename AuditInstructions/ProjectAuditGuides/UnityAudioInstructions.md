# Unity audio audit

Load for runtime mixer routing, volume settings, pooled/overlapping voices, spatial sound, or
scene persistence. Apply the [shared evidence standard](ProjectReview.md#evidence-standard).
`unity:audio-setup-mixers` owns routing setup and `unity:optimize-audio` owns import/DSP tuning recipes;
[Assets](UnityAssetsAndMemoryInstructions.md) owns audio import, memory, and streaming findings.
Without those skills, use the checks below and the official docs.
**Last verified: October 2026.**

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Routing contract | `outputAudioMixerGroup` on every AudioSource in saved prefabs/scenes, and in pooled and one-shot setup code | A shipped source has no mixer group in saved data and no runtime assignment on any path that plays it, where the project routes audio through a mixer. Read the pool and one-shot setup code first: a pooled source whose `outputAudioMixerGroup` is assigned in code is routed |
| Volume units | Slider handlers that call `SetFloat`, and the exposed parameter's units | A slider value reaches a dB parameter without conversion, or the conversion has no zero guard (`Log10(0)`) |
| Parameter control | Exposed names in code against the `.mixer` asset (mixer dump), the `SetFloat` return, the call site | A missing exposed parameter or incorrect timing prevents applying required settings. An ignored `SetFloat` return is a candidate when no other validation protects the contract; call from Start or later under the documented API |
| Voice ownership | The pool's get/reset path and any voice cap | A checkout inherits mutable state from a previous voice, or the intended active-voice limit is enforced only by the pool’s inactive `maxSize`. Pool-wide invariant properties need not be rewritten every checkout |
| Pool return | What triggers return to the pool | Return runs after a fixed wait of the clip length while pitch, pause, time scale, or loop can change. Cancellation and stale checkout: [Scenes](UnityScenesAndLifecycleInstructions.md) |
| Spatial contract | `spatialBlend`, `minDistance`/`maxDistance`, rolloff on world-space sources | `minDistance` is greater than or equal to `maxDistance`, or a source the project treats as positional has `spatialBlend` 0 (state the policy first) |
| Listener/session state | Enabled `AudioListener` components across all loaded scenes; code that sets `AudioListener.pause` or `volume` | The count of enabled listeners across loaded scenes is not 1, or code sets listener pause/volume with no restore path |
| Settings reapply | Saved volume values and the call that applies them after load; music owner creation | Loaded settings never reach their playback owner, or scene entry duplicates persistent music. A surviving mixer/owner need not reapply settings on every scene start when values remain correct |
| Pause/completion identity | `Pause`/`UnPause`, `isPlaying`, listener pause, `ignoreListenerPause`, scheduled/loop playback | A paused voice is returned because `isPlaying` is false, a required resume is lost, or UI/audio violates the agreed pause policy |
| Voice priority | Real/virtual voice limits, priorities, representative overlap on target | Critical cues/dialogue become inaudible under supported concurrency; priority/voice counts alone do not prove failure and priority behavior differs on Web |
| Music clock | DSP scheduling, clip readiness, lead time, pause/resume | A gapless/rhythm requirement fails through measured gaps/drift or late starts; ordinary sound effects need not use DSP scheduling |

## Cases worth explicit inspection

- ⚠️ A common convention maps a 0.0001 to 1 slider to decibels with `20 * Log10(v)`, which gives -80 at
  the floor; Unity's own sample can instead use a dB slider and pass it straight through. This is a
  convention, not an engine rule. Label the slider contract and handle silence and range explicitly.
- ⚠️ `AudioMixer.SetFloat` returns false if the exposed parameter is not found or snapshots are being
  edited, and the reference says to call it from `Start` or later, not `Awake` or `OnEnable`. After a
  scripted `SetFloat`, snapshots no longer control that parameter until `ClearFloat`. A snapshot
  transition does not simply override every scripted setting.
- ⚠️ The `AudioListener` reference states you can only have one listener in a Scene. With additive
  scenes, count enabled listeners across the whole loaded world.
- ⚠️ A fixed wait of clip length assumes pitch, pause, time scale, loops, and playback ownership stay
  compatible. Match completion/cleanup to actual playback.
- ℹ️ Reverb placement, pitch randomization, stereo/mono, and rolloff shape are design/platform choices
  rather than automatic defects.

## Validation

Exercise mute/volume extremes, restart and scene changes, overlapping sounds, pause/resume, changed
pitch, loops, and cancellation during playback as applicable. Listen on the target setup; inspect
voice/checkout counts after repeated cycles. Verify saved mixer/source wiring and re-read settings.

Technical references: [AudioMixer.SetFloat](https://docs.unity3d.com/ScriptReference/Audio.AudioMixer.SetFloat.html)
and [AudioListener](https://docs.unity3d.com/ScriptReference/AudioListener.html).

Additional references: [paused isPlaying](https://docs.unity3d.com/ScriptReference/AudioSource-isPlaying.html),
[listener/DSP pause](https://docs.unity3d.com/ScriptReference/AudioListener-pause.html),
[priority](https://docs.unity3d.com/ScriptReference/AudioSource-priority.html), and
[scheduled playback](https://docs.unity3d.com/ScriptReference/AudioSource.PlayScheduled.html).
