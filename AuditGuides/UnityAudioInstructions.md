# Unity audio audit

Load for runtime mixer routing, volume settings, pooled/overlapping voices, spatial sound, or
scene persistence. Apply the [shared evidence standard](README.md#evidence-standard).
`audio-setup-mixers` owns routing setup and `optimize-audio` owns import/DSP tuning recipes.

## Audit checks

| Check | Evidence to inspect | Finding when |
|---|---|---|
| Routing contract | Every source path, including pooled and one-shot playback | Sound bypasses intended volume/mute/effect controls |
| Volume units | Slider interpretation, range, conversion, zero guard | Amplitude is passed as decibels or conversion produces invalid values |
| Parameter control | Exposed names, SetFloat outcome, snapshots, initialization | A setting is never applied or two owners disagree about the parameter |
| Voice ownership | Playback, overlap, limits, priority/stealing, source lifetime | A reused source cuts off required audio or active voices exceed the intended policy |
| Pool return | Completion, pause/pitch/loop, cancellation, generation identity | A canceled sound leaks a checkout or a stale completion releases a reused source |
| Spatial contract | Listener, source position/blend, rolloff, scale | Audible position/range disagrees with intended presentation |
| Listener/session state | All loaded scenes, camera switches, listener pause/volume | The loaded world has unintended zero/multiple active listeners or stale global mute state |
| Persistence | Saved settings and reapply path, music owner | Scene/restart resets user choices or creates duplicate music playback |

## Cases worth explicit inspection

- `20 * Log10(v)` maps linear amplitude to decibels. A deliberately perceptual/logarithmic slider
  can use another mapping; label the slider contract and handle silence/range explicitly.
- Check `AudioMixer.SetFloat`'s return value. Apply startup values at a supported phase (`Start` or
  later), and remember a scripted exposed parameter is no longer controlled by snapshots until
  control is cleared. A snapshot transition does not simply override every scripted setting.
- An ObjectPool's `maxSize` is not a simultaneous-voice cap. The audio owner needs its own active
  voice policy; follow [Performance](UnityPerformanceOptimizationInstructions.md) for pool semantics.
- A fixed wait of clip length assumes pitch, pause, time scale, loops, and playback ownership stay
  compatible. Match completion/cleanup to actual playback; use
  [Scenes](UnityScenesAndLifecycleInstructions.md) for cancellation and stale checkout handling.
- `PlayOneShot` uses its AudioSource's lifetime; destroying the source is not a persistence strategy.
  Pool reset includes clip, mixer, pitch, volume, loop, spatial state, and any per-sound overrides.
- Count active listeners across the loaded world, not one per additive scene. Reverb placement,
  pitch randomization, stereo/mono, and rolloff are design/platform choices rather than automatic defects.

## Validation

Exercise mute/volume extremes, restart and scene changes, overlapping sounds, pause/resume, changed
pitch, loops, and cancellation during playback as applicable. Listen on the target setup; inspect
voice/checkout counts after repeated cycles. Verify saved mixer/source wiring and re-read settings.
Use [Assets](UnityAssetsAndMemoryInstructions.md) for residency and
[Persistence](UnityPersistenceInstructions.md) for settings recovery.

Technical reference: [AudioMixer.SetFloat](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Audio.AudioMixer.SetFloat.html).
