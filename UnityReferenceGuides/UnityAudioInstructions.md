# Unity Audio

> **General Unity best practice.** Applies to any Unity 6 project. Change these only if you
> know why. Personal style preferences live in [`UnityStyleGuide.md`](../UnityStyleGuide.md);
> project-specific settings live in [`UnityCustomInstructions/`](../UnityCustomInstructions/).

Runtime audio: mixers, sources, pooling, and spatialisation.

**Import settings are not covered here.** Load type, Force To Mono and compression live in
[Assets & Memory](UnityAssetsAndMemoryInstructions.md#audio-import-settings), because they're a
memory decision rather than a runtime one. Get those right first — no amount of good mixer routing
fixes a 30 MB music track loaded into RAM.

Table of contents:
- [Architecture](#architecture)
- [AudioMixer and groups](#audiomixer-and-groups)
- [Volume sliders and the decibel trap](#volume-sliders-and-the-decibel-trap)
- [Snapshots](#snapshots)
- [Playing sounds](#playing-sounds)
- [AudioSource pooling](#audiosource-pooling)
- [Spatial audio](#spatial-audio)
- [AudioListener](#audiolistener)
- [Troubleshooting](#troubleshooting)
- [Review checklist](#review-checklist)
- [Learn more](#learn-more)

---

## Architecture

- ✅ Route **all** audio through an `AudioMixer`. An `AudioSource` with no Output group bypasses your
  volume controls entirely, and you won't notice until someone complains that muting doesn't work.
- ✅ One audio service that owns playback. Components ask it to play a sound; they don't create
  `AudioSource`s themselves.
- ✅ Define sounds as ScriptableObjects (clip + volume + pitch range + mixer group), per
  [ScriptableObjects](../UnityStyleGuide.md#scriptable-objects). Designers tune them without touching
  code.
- ⚠️ Randomise pitch slightly (±0.05) on repeated SFX. Identical playback of the same clip is the
  single most fatiguing thing in game audio.

```
Master
├── Music
├── SFX
│   ├── UI
│   └── World
└── Voice
```

- ✅ Keep the group tree shallow. Every group is a DSP node with its own processing cost, and effects
  on a group run even when nothing is audible through it.

---

## AudioMixer and groups

- ✅ Assign `outputAudioMixerGroup` on every `AudioSource`, including pooled ones.
- ⚠️ Effects on a mixer group cost CPU whether or not sound is passing through. A reverb on an unused
  group is pure waste.
- ✅ Use **Duck Volume** on a sidechain to drop music under dialogue rather than scripting volume.
- ⚠️ Mixer parameter changes are not sample-accurate. For a hard cut, stop the source; for a smooth
  change, use a snapshot transition.

---

## Volume sliders and the decibel trap

This catches nearly everyone once. A mixer's volume is in **decibels**, on a logarithmic scale from
-80 to 0. A UI slider is linear from 0 to 1. Wiring one straight into the other gives a slider where
everything below about 0.8 sounds identical and the bottom half does nothing.

- ✅ Convert with `Mathf.Log10(value) * 20`.
- ⚠️ Guard against zero — `Log10(0)` is negative infinity, which the mixer rejects. Clamp to a small
  epsilon and treat it as -80 dB (silence).
- ✅ Expose the parameter in the Audio Mixer window first (right-click the volume → *Expose*), then
  rename it in the Exposed Parameters dropdown. `SetFloat` fails silently if the name doesn't match.

```csharp
public class VolumeSettings : MonoBehaviour
{
    private const float k_minDecibels = -80f;
    private const float k_silenceThreshold = 0.0001f;

    [SerializeField] private AudioMixer m_mixer;

    /// <summary>Sets a mixer volume from a linear 0–1 slider value.</summary>
    public void SetVolume(string exposedParameter, float linearValue)
    {
        // Log10(0) is -Infinity, which the mixer rejects - clamp to silence instead
        float decibels = linearValue <= k_silenceThreshold
            ? k_minDecibels
            : Mathf.Log10(linearValue) * 20f;

        if (!m_mixer.SetFloat(exposedParameter, decibels))
        {
            Debug.LogError($"[{GetType().Name}] '{exposedParameter}' is not exposed on the mixer.", this);
        }
    }

    /// <summary>Reads a mixer volume back as a linear 0–1 value, for restoring a slider.</summary>
    public float GetVolume(string exposedParameter)
    {
        if (!m_mixer.GetFloat(exposedParameter, out float decibels))
        {
            return 1f;
        }

        return Mathf.Pow(10f, decibels / 20f);
    }
}
```

- ⚠️ **Mixer values don't survive a play session in the Editor** the way you might expect — the mixer
  asset stores the values you set at runtime. Persist the player's choice yourself (`PlayerPrefs` or
  your settings save) and re-apply it on startup.
- ⚠️ Setting an exposed parameter while a **snapshot transition** is running has no effect; the
  snapshot wins.

---

## Snapshots

- ✅ Use snapshots for whole-mix states: normal, paused, underwater, low-health.
- ✅ `TransitionToSnapshots` blends between several at once with weights.
- ✅ Transition over 0.1–0.5s. Instant snapshot changes are audible as a click.
- ⚠️ Snapshots capture *every* mixer value, so a snapshot recorded before you added a group will
  reset that group when it's applied.

```csharp
public void SetPaused(bool isPaused)
{
    AudioMixerSnapshot target = isPaused ? m_pausedSnapshot : m_defaultSnapshot;
    target.TransitionTo(0.25f);
}
```

---

## Playing sounds

- ❌ **Never use `AudioSource.PlayClipAtPoint` for frequent SFX.** It creates a GameObject with an
  `AudioSource`, plays, then destroys it — an allocation and a destroy per shot. Fine for a one-off
  in a prototype, disastrous in a gun loop.
- ✅ Use `PlayOneShot` on an existing source for overlapping sounds. It doesn't interrupt what the
  source is already playing and doesn't need a free source per sound.
- ⚠️ `Play()` restarts the source, cutting off whatever it was playing. That's what you want for
  music, not for SFX.
- ✅ `PlayOneShot` respects the source's `outputAudioMixerGroup`, spatial settings, and position — so
  a pooled positional source plus `PlayOneShot` covers most cases.

| Method | Overlaps | Allocates | Use for |
|---|---|---|---|
| `Play()` | ❌ restarts | No | Music, looping ambience |
| `PlayOneShot(clip)` | ✅ | No | Most SFX |
| `PlayClipAtPoint(clip, pos)` | ✅ | ⚠️ GameObject per call | Never in a hot path |
| Pooled source + `Play()` | ✅ | No | Positional SFX needing individual control |

---

## AudioSource pooling

A positional sound needs an `AudioSource` at a position. Creating one per shot is the same mistake as
instantiating a bullet per shot — pool them.

- ✅ Use `UnityEngine.Pool.ObjectPool<T>`, consistent with
  [Object Pooling](UnityDesignPatternsInstructions.md#object-pooling).
- ✅ Return the source to the pool when the clip finishes. A coroutine or `Awaitable` timed to
  `clip.length / pitch` is simpler and cheaper than polling `isPlaying` every frame.
- ⚠️ Reset `pitch`, `volume`, `loop` and `spatialBlend` on release. A pooled source that kept
  `loop = true` never returns.
- ⚠️ Cap the pool. Fifty simultaneous explosions is a mix nobody can hear anyway, and each voice
  costs CPU.

```csharp
public class AudioService : MonoBehaviour
{
    [SerializeField] private AudioSource m_sourcePrefab;
    [SerializeField] private int m_maxVoices = 32;

    private ObjectPool<AudioSource> m_pool;

    private void Awake()
    {
        m_pool = new ObjectPool<AudioSource>(
            createFunc: () => Instantiate(m_sourcePrefab, transform),
            actionOnGet: source => source.gameObject.SetActive(true),
            actionOnRelease: ResetSource,
            actionOnDestroy: source => Destroy(source.gameObject),
            collectionCheck: false,
            defaultCapacity: 8,
            maxSize: m_maxVoices);
    }

    public async Awaitable PlayAtAsync(SoundDataSO sound, Vector3 position, CancellationToken token)
    {
        AudioSource source = m_pool.Get();

        source.transform.position = position;
        source.clip = sound.Clip;
        source.outputAudioMixerGroup = sound.MixerGroup;
        source.volume = sound.Volume;
        source.pitch = sound.RandomPitch();      // Slight variation stops ear fatigue
        source.spatialBlend = sound.SpatialBlend;
        source.Play();

        // Wait the real duration - pitch changes how long the clip takes
        await Awaitable.WaitForSecondsAsync(sound.Clip.length / source.pitch, token);

        if (this == null) return;

        m_pool.Release(source);
    }

    private static void ResetSource(AudioSource source)
    {
        // Without this, a pooled looping source never comes back
        source.Stop();
        source.clip = null;
        source.loop = false;
        source.pitch = 1f;
        source.volume = 1f;
        source.gameObject.SetActive(false);
    }
}
```

---

## Spatial audio

- ⚠️ **`spatialBlend` defaults to 0, which is fully 2D.** A "3D sound" that plays at the same volume
  everywhere in the level almost always means this was never set to 1.
- ✅ Set `spatialBlend = 1` for anything positional, `0` for UI and music.
- ✅ Use **Custom Rolloff** or Linear rather than the default Logarithmic if you want audible control
  over the falloff curve — logarithmic drops off very fast up close and very slowly far away.
- ✅ Set `maxDistance` to something meaningful. The default of 500 means almost nothing attenuates in
  a normal-scale level.
- ⚠️ `minDistance` is where attenuation *starts*, not where the sound begins. Inside it, the sound is
  at full volume.
- ✅ Force 3D clips to mono on import — stereo data is discarded for spatialised playback anyway. See
  [Assets & Memory](UnityAssetsAndMemoryInstructions.md#audio-import-settings).

---

## AudioListener

- ⚠️ **Exactly one active `AudioListener` per scene.** Two produces a Unity warning and unpredictable
  mixing; zero produces total silence with no error at all.
- ⚠️ Additive scene loading is the usual cause of two listeners — each scene ships with a camera.
  Strip listeners from additively-loaded scenes, or disable them on load. See
  [Scenes & Lifecycle](UnityScenesAndLifecycleInstructions.md#additive-scene-loading).
- ✅ The listener normally lives on the main camera. For a third-person game, consider putting it on
  the character instead so distance attenuation matches where the player *is* rather than where the
  camera is.
- ✅ `AudioListener.pause` freezes all audio; `AudioListener.volume` is a global master independent of
  the mixer.

---

## Troubleshooting

**No sound at all, no errors.**
Work down this list in order — it's almost always one of the first three.

```csharp
private void DiagnoseSilence(AudioSource source)
{
    Debug.Log($"--- {source.gameObject.name} ---", source);
    Debug.Log($"  clip:        {source.clip?.name ?? "NONE"}");
    Debug.Log($"  isPlaying:   {source.isPlaying}");
    Debug.Log($"  volume:      {source.volume}   mute: {source.mute}");
    Debug.Log($"  enabled:     {source.enabled}   activeInHierarchy: {source.gameObject.activeInHierarchy}");
    Debug.Log($"  mixer group: {source.outputAudioMixerGroup?.name ?? "NONE (bypasses mixer)"}");
    Debug.Log($"  spatialBlend:{source.spatialBlend}  (0 = 2D, 1 = 3D)");
    Debug.Log($"  maxDistance: {source.maxDistance}");

    int listeners = FindObjectsByType<AudioListener>(FindObjectsSortMode.None).Length;
    Debug.Log($"  active AudioListeners in scene: {listeners}  (must be exactly 1)");

    Debug.Log($"  AudioListener.volume: {AudioListener.volume}  pause: {AudioListener.pause}");
}
```

**Volume slider does nothing until the last 20%.**
Linear slider value written straight to a decibel parameter. See
[the decibel trap](#volume-sliders-and-the-decibel-trap).

**`SetFloat` on the mixer returns false / has no effect.**
The parameter isn't exposed, or the name doesn't match. Exposing it in the mixer window is a separate
step from naming it — check the Exposed Parameters dropdown.

**Volume changes are ignored.**
A snapshot transition is running and overriding the parameter, or the `AudioSource` has no output
group and bypasses the mixer entirely.

**3D sound doesn't get quieter with distance.**
`spatialBlend` is 0, or `maxDistance` is larger than your level.

**Sound cuts off partway through.**
A pooled source was released too early, the source was reused by another `Play()` call, or the
GameObject holding it was destroyed. `PlayOneShot` on a persistent source survives the latter;
`Play()` on a destroyed object doesn't.

**Audio distorts when many sounds play.**
Summed voices clipping the master. Add a compressor/limiter on Master, lower per-sound volumes, and
cap the voice pool.

**A pooled source stops working after a while.**
It was released while `loop = true` and never returned. Reset state on release.

**Music restarts on scene load.**
The music source is in the scene rather than on a persistent object. See
[Scenes & Lifecycle](UnityScenesAndLifecycleInstructions.md#the-bootstrap-scene-pattern).

---

## Review checklist

| Check | Look for |
|---|---|
| Routing | `AudioSource` with no `outputAudioMixerGroup` |
| Volume | Linear slider value passed to a dB parameter without `Log10` |
| Volume | `Log10` with no guard against zero |
| Allocation | `PlayClipAtPoint` in a frequently-called path |
| Pooling | `Instantiate` of an audio GameObject per sound |
| Pooling | Pooled source not fully reset on release |
| Spatial | `spatialBlend` left at 0 for a positional sound |
| Spatial | `maxDistance` left at the 500 default |
| Listener | More than one, or zero, active `AudioListener` |
| Mixer cost | Effects on groups that carry no audio |
| Variety | Repeated SFX with no pitch variation |
| Persistence | Runtime mixer values not saved and re-applied on startup |

---

## Learn more

- [Audio overview, Unity manual](https://docs.unity3d.com/6000.3/Documentation/Manual/Audio.html)
- [AudioMixer](https://docs.unity3d.com/6000.3/Documentation/Manual/AudioMixer.html)
- [AudioSource scripting reference](https://docs.unity3d.com/6000.3/Documentation/ScriptReference/AudioSource.html)
