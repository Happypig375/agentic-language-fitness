# Workstream D v2 calibration incident (2026-08-31)

The v2 review, CI, and clean-freeze gates completed at commit
`eed5b4dc9657366822cd3833a990dfd569b921e9` (GitHub Actions `33309932298`,
Linux/Windows green). The subsequent non-counting calibration exposed a host
apparatus incident and closes v2; no model outcome is synthesized, retried, or
pooled across this incident.

## Evidence ledger

Result SHA-256 values below are hashes of the retained run result artifacts.

| Cell | Attempt | Disposition | Result SHA-256 |
| --- | --- | --- | --- |
| H/F# | `cal-h-primary-fsharp-01` | candidate timeout after tasks 001–005; valid candidate outcome, missing terminal usage | `981cb1846b3fb496a09ef0772d80495cfa93beed7360e774c59f918b64a9036a` |
| H/C# | `-01` | auth infrastructure-invalid | `045956c44e345a14688c7f694e88165d64f3ba141bb8bee88644b1e3eb4e8055` |
| H/C# | `-02` | auth infrastructure-invalid | `349dea4aad16f3fbeab30d8ed00d4cc5132ade3178ff8850c204e426cc656c20` |
| H/C# | `-03` | audited 8/8 outcome | `ac7706b1a6685ca569fb4a5586d641442fbec58cba6ed57962990dabe095a894` |
| M primary C# | `cal-m-primary-csharp-01` | audited 8/8; provisionally too easy | `f5a613d317112369920f1c1ef7b8462cea08b4463ca9195b448bc1fa4e82e8ea` |
| M primary F# | `cal-m-primary-fsharp-01` | audited 8/8; provisionally too easy | `bcc68bda85c94cf63b18d0106e8f4d7bbf6251404253872ae334dfb1c2474206` |
| M reverse C# | `cal-m-reverse-csharp-01` | audited 8/8; confirmed too easy | `ff50eabd54e5af25290fcd8c0800985aedb46db7fb389502eff163380848da05` |
| M reverse F# | `cal-m-reverse-fsharp-01` | audited 8/8; confirmed too easy | `59e616b00437b703734e37f14340665929d7764f5024aa7788e7f2e65418217e` |
| L/F# | `cal-l-primary-fsharp-01` | candidate outcome, substantive failure at task 007 | `a98939cb466993b5e17d45580a169e50b4d426dbb5ad29f59c55a6f7aa89016f` |
| L/C# | `cal-l-primary-csharp-01` | auth infrastructure-invalid | `d23e00b138564c7ec449cd28292657d50c40f4890f7a2af3b2cded7206174024` |
| L/C# | `cal-l-primary-csharp-02` | auth infrastructure-invalid | `1a66dc8ca2928808ce6e341ac6396de937a0434fad2c7b97412d0acd2f9a54f5` |
| L/C# | `cal-l-primary-csharp-03` | auth infrastructure-invalid | `e8356925ed1d6b9d2a37496cbbeb9a4d6adc82173c36324d0814554f5daf5a0c` |
| L/C# | `cal-l-primary-csharp-04` | auth infrastructure-invalid | `8c16f4cec2d82fe586cc818efa88b7b05f007ef141e41b1b9cc433b186fd3744` |

The M primary decision record hash is
`04ed140e0580eeb0239bd5c6dd6718dced925fe02ea2cae7e29077ce8703ef43`; the
final decision record hash is
`5fce0a3e1650fca4bf0cd9f42855f77e8dfb5008b22afbc6e444929cdf945f78`.

The L/C# `cal-l-primary-csharp-05` attempt remains `started`, attempt SHA
`84047de4cf0562d8279a913be75b4b0f858bcfee60b646865b73ac0cf895805d`, with 94 files / 1,280,680 bytes and canonical inventory SHA
`d1182affaca0dd25e33127ec2e7a5d5e800497b6d1d4b3f96efbdbc9e18cee45`. Task 008 has only three zero-byte logs and no usage or
task-result artifact. Windows System Event 2004 (RecordId 344966,
`2026-08-30T23:43:11.8119458+08:00`, message SHA
`8b92a009351140b50ac5f300a3915fba1a3b41d46146c5b92bba433ee7b1e8a6`) corroborates host out-of-memory pressure. Consumer names
are intentionally redacted. The user's report and this event explain the
orchestrator/agent stop; missing artifacts are not a candidate failure.

The v2 family is therefore closed and retired. A fresh, reviewed v3 family is
required before any further calibration.
