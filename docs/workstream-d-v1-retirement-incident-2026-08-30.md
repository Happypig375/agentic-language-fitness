# Workstream D v1 retirement incident

The v1 family was clean-frozen from attempted head
`965b44716470fc3f97cdd144aa0425594ceee8d9`, then retired after its first
H/F# calibration. Run `cal-h-primary-fsharp-01` reached `started` and ended as
an unresolved apparatus-terminated attempt: command sidecar validation raised
`KeyError: snapshot`. The sidecar recorded `auth_ok: true`, `timed_out: true`,
19 events, and zero usage records; accounting was unavailable.

Preserved raw hashes:

- attempt: `76d20b8598e42c8ee68fa6d13d216e672aaca2471b2c5f3d518b4acfc3d99490`
- protocol manifest: `05d26ae5f8ae461788adcd15a22609736c2689a3aca9bcd488e1799ba666e50c`
- usage: `77a2977ddcebfbc2ecacf962a6d4187ad323de88b14643470d155a019d71f696`
- v1 frozen manifest internal hash:
  `ce126c7d2df61931d7352174089bd0896a71567a74f285db800051aff266c559`

There is no analyzable candidate outcome. Do not synthesize missing
result/log files, retry v1, or pool this attempt with any later family. The
replacement, with the schema-aware command repair, is
`workstream-d-language-v2`.
