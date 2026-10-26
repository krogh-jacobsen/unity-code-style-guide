# Re-check checklist for CoreCLRUpgrade.md

Maintainer notes, not an agent document (Unity ignores this `Tools~` folder). Run this whenever Unity
publishes a CoreCLR update, when a Unity 7.0 or 6.7 Editor reaches a new milestone, and at least every
six months. `python3 AuditInstructions/Tools/validate_all.py` warns when a "Last verified" date is older than that.

After re-checking, update the **Last verified** line in `CoreCLRUpgrade.md` and the CHANGELOG.

## Claims that rest on thin evidence

| Claim in `CoreCLRUpgrade.md` | Why it is weak | Source to re-read |
|---|---|---|
| Unity 7.0 Alpha CoreCLR Editor targets C# 9 and .NET Standard 2.1 | Forum announcement, not product documentation | [October 2026 update](https://discussions.unity.com/t/coreclr-scripting-and-net-update-october-2026/1738338) |
| Full .NET 10 and C# 14 have no committed date | A roadmap statement that can move at any update | The same post, then newer updates in that thread series |
| `AfterCodeReloadSerialization` namespace and name | Read from a living upgrade guide; not checked against an installed Editor | [Upgrade guide](https://discussions.unity.com/t/path-to-coreclr-2026-upgrade-guide/1714279), then the installed assemblies |
| `AutoStaticsCleanup` and `BeforeCodeUnloading` exist and mean what the guide says | "Discussed" in the guide, not demonstrated | The same guide; compile a sample on the migration Editor |
| 6.7 experimental players | Listed as separate options; support level not read from a manual page | 6.7 Player settings pages for each platform |
| `BinaryFormatter` as the usual unsupported serializer | General .NET knowledge, not a Unity statement | The upgrade guide's serialization section |

## Not yet run

The workflow in `CoreCLRUpgrade.md` has not been executed end to end against a real project or a
CoreCLR Editor. Run it once on a disposable project and record the result in `Validation.md`.
