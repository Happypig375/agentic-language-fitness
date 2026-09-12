# Maintenance simulation reference-lineage review

**Status:** repaired lineage source review `COMMENT`, pending independent
behavioral acceptance; AI review, not human expert review or approval. This
record is separate from the approved seed review.

## Scope, blinding, and method

I inspected only the public seed contract, Episodes 01–08, shared/language
guidance, reference patches, and source snapshots produced read-only by
`maintenance.reconstruct`. I did not inspect fixtures/cases, validation reports,
model results, language outcomes, or token/byte counts. During review I was told
that independent validation had found F# removal regressions; this limits semantic
blinding but disclosed no model outcome. F# patches changed concurrently, so the
superseded hashes below identify the code on which findings were made; later
repair hashes are not approved by this review.

## Actionable findings

- **P1:** Both Episode-01 enqueue implementations classify malformed known-but-
  unsupported nested commands before validating their immediate shape (for
  example `{op:tick}`), producing `invalid_value` instead of `invalid_shape`.
  F# also classified an unknown nested operation as `invalid_value`, not
  `unknown_operation`. From C# Episode 03 onward, newly recognized valid nested
  operations were reported `unknown_operation`, not `invalid_value`.
- **P1:** C# Episode 03 accepts `spawn_follower` with `target:null`; the public
  operation requires an ID-shaped target string.
- **P1:** Episode-04 snapshot import misclassifies invalid representations: C#
  reports an unknown entity kind as `invalid_shape` and can report an invalid
  follower-target ID as `missing_entity`; F# accepts a mover carrying
  `target:null` and reports a self-target as `missing_entity` rather than
  `invalid_value`.
- **P1 (disclosed independent finding):** the inspected F# lineage failed to
  cancel later queued removals after a successful deferred removal from Episode
  02, and failed to detach follower targets after deferred removal in Episodes
  03–05. Concurrent repairs supersede those F# artifacts and require re-review.

## Stable-lineage re-review disposition

All four P1 groups above are resolved in the stable reconstructed lineages.
Episode 01 now explicitly limits recognized-but-unsupported checking to immediate
shape/types without future-name exposure, nested-payload semantics, or world
lookup. Both implementations preserve that boundary cumulatively. C# now rejects
null follower targets and correctly classifies snapshot kind/target errors. F#
now enforces exact mover/follower snapshot shapes and self-target classification;
successful deferred removal cancels later removals and detaches follower targets
from their introducing stages onward. No further source/architecture finding was
identified. The earlier `REQUEST_CHANGES` and superseded identities remain above
as review history, not approval of those artifacts.

Exact stable patch SHA-256, C# 01–08:
`569e71447035f1991f811dc359162fbbf09a53ab5856c92c047b457231b73845`,
`93f722fc0ed023e511e76d02bd717fce5cbf27a12877a0e2b9da13ad468ecc5d`,
`f72869b78673e357e66ba3a7bc2433b04eb8d7e98c190d2252f5bd0562027ebe`,
`dc950938f4b775be1ac0b0da8619da6a03ec28074d326124c756d21b11358dca`,
`b7d30be3d1ef687957611841132b2ff8bc11ed68cec12119713c5c5e1cc0530b`,
`8f2d3fafff1e15b30e08e2d485aa96d98e0243d9269c1642694c44c88079eee3`,
`87aba3671ad02100701634b553d61e805780d208050fdd73d3b777672b24fdad`,
`9996dc23381f41eac11bd0e8c306ef143541aab9e74e3d068040093434d525dc`.

Exact stable patch SHA-256, F# 01–08:
`1b8e598dcf7d5db0a801bb0180fe988e3dc13d912f12c775581bc148301b7630`,
`d2846868073608a74930f71c93c470e92164cb2220a29bffd773591202023c45`,
`f5503cf99133f1338fce936d7c89aa55e0d0265bbd3f2af990a34d7065543308`,
`95d6189986a246996067e832fccf4e6dc41c6250526d0ea0b3792d8dd8b4861f`,
`628495b47e3e5d5399f3b50c8d6a53817316dba8c1e2bc4fe75804cc6649efa0`,
`57d15d268bfb9e7f386b799091e16b571c9d843cb670a440c49eb920b37eaa7b`,
`7543500670bdcf209caa191b91f8d77b542637b07b38f99af85c083559dbe6ed`,
`302a689860dce4089c06c91eeb7cfb5ae2dc79f6cbec107f0f2e8c0ef28e5c7a`.

Exact stable reconstructed source SHA-256, C# `Program.cs` 01–08:
`f49b882a1b9ceec63e51c1ba449879492e66f50aa2937531620ada46708d60a1`,
`2d38815b282bc78c1dfb794e114ac6a9156d1160e22a19bf5c84d7ce92a756fe`,
`a8be2b3bd232115df3b882541d810cfee789dc117ba307453f4d3ef544a23165`,
`34c49a02e044ed5730eb9b1c707858cdc4fb97a5d70bdaa84dbdaf27b80562ea`,
`54a034044e3b325fe94dcc491daa43865881038aa47c91784df9d0a948efe0bc`,
`2bf76f3c0888f74a9f6b747331f56e077e52572410d1d0af2d71ad37e8f8cf94`,
`41bd7988b7226ac09c5df39d5834a8f9d1d88e1bad7df6c99258f3878fdba8a6`,
`30d125aab74b286ca2efabed93e2f08a659c443c53f2cc45b3ed67a9cb7cbe28`.

Exact stable reconstructed source SHA-256, F# `Simulation.fs` 01–08:
`8a78b52a093b2932ce8c2bd7e9512bda8f5dd9fb46eaf6ede1fa770b241c07cb`,
`daa7ca22e96d0d0bb82fba609560670f564ff3ccb022f7d1ac729572c539b9e3`,
`0ce0f7f6ea82e6e89ee0f2ceea3109f8c228e7e88fc79ad6de0e34b54cf46d87`,
`937bd5424589003d3c68b414196a0d9447a7adb7d7ebd14809525b9a64599c10`,
`dae955f396756bae53a672307402ed603a3722620ed85b9afb4c501476dc5be6`,
`6c071844f7283152b5b2aeaf192949d82d35577ff9f31e5cdcf9469ec1d2245c`,
`eca2d38befcb2c0ed2801ffb0a96acebaba87cd2c4597df0ddba0afcacbc0fe4`,
`8e1548e7aad146fb576fe5460e46acbc8517007d5b4935d81dd17f8f0db8a969`.

Project hashes remain C#
`1f638de8c09974d0ca7dda36c16d766c24398e36a538dd5a5a8e1af128526234`
and F#
`5cc8c353cf25358615df7f9996b8b57fdc3a8cbf469c41b5c9b08324b13f831e`
at every checkpoint.

Apart from these behavioral defects, the cumulative themes are plausible and
state/effect ownership remains identifiable. C# records/patterns/owned mutable
collections and F# records/maps/results/unions are credible modern idioms.
References are feasibility witnesses only; tasks permit alternative private
architectures and contain no requirement to translate or length-balance them.

## Exact reviewed public artifact SHA-256

- `contract.md`: `5f0cc0e10c61db2a6355a63c181e4c3653ba2da3fe96522342149d1850be5b79`
- episodes 01–08: `b728190959b5a7a768213f601b54a1a14ad05e48de195aa1860cb97e7468528d`, `5a8df8a523a450e928aa5901305debc6d5e6b303f3f1caf6ba526ad573a269e9`, `59aeb20d950c9bcdac78c6ec0290917f122191c079a6725d4e72196b8ff7ca16`, `fabe7b22ba01ac6dc56e8aadf764ca40555328b12cd00a2c155ce694412f57c7`, `3e91ba53db6afa0523324bf4a5d9b40cecc59c3da2dd8f55ca2ccd41693d22d8`, `1adc955e7dc79998ec9d3fb807af0efd8fc89c87a6406eaf971d1281520633e6`, `f2ead60e0eeca09fa98c00c7db5037740deb4e90d1513266ec02d14b02c67ebd`, `9e83da696e1f4aa47683e8e0ccd7f38c8c625f7b63d7fc144ab3d23b667cb627`.
- guidance common/C#/F#: `9412d3c70728ff828567dc6ce08d242a7755bcd8383651ed88c7697910ec2d11`, `ab426ea9b7f7b9953204475cffad81b9f05fe166da228f127db71d92126c6e09`, `322ffccd44c52e37f68a59816d0af555545bcf54d572591ad002d2e3751e4c65`.

Episode 01 was subsequently clarified as `fd20f66692692c9a9183e1715198f449cf149401800edea2027ba9de0914d7e1`; that revision governed the stable-lineage re-review but was not the task text used to discover the findings.

## Exact reviewed patch SHA-256

- C# 01–08: `a2db477bbbdedeb21edad5842c92a5743a8a0381c810528def0ecd7ee74e2c42`, `1a80a5d1b52d24cea68c45ef4bc9dd21d493e7f460c2528b9bdaadaceb66ddf7`, `059eb20b43c81a29dc087fc984cbe7fc35043b08c82611f915bd7cd4b4c5896b`, `1d0991aa30fe2ed2b2c65f1c423c1ecd2f101ca8d8f480e75263566f3c8a65ed`, `46cfcad2ecd1064fdc6c1d01dee1fde70f7b754907eaee3d5c4c3d3de35a9782`, `fb6669f91499e25b499874b1ccd997eb78e8f86fb99bd33a429f0bbd8ebbf29a`, `946cb1ab1e595573e634aedbb8897bb7b632140c04e923e36991e5e0a19559e7`, `738f2968d17067c68795914f7e9cc4297cba02f356e91c6df7b71833e329e0fa`.
- Superseded F# 01–08: `8a003dc575579e9b14f2af0ddabd240ad34be48e47cfd9e7bb5c1c67ba352c48`, `0d0193d7f0526e9c04d1bf22fec33a37598c760cf2238d3fd08f15e61a4af822`, `4e16463060390e8212463302eeb03b515ddeb242cd40c5b7ad16278a0715adba`, `8dc8c0f96ab87cd3ff59f11814b96fe4f2696d084c2651e98492538fb4331b04`, `b941f2e9d65f18978c22b6bf89188ebabcb04e59c099945f981a8f0a4079b39a`, `2e45ea70138fd95f37b78d53d1f2187cc7833c7dec8925acab317934e6ebc62b`, `58eca1da320de8b39526145204940daccf122dd5274cf451f6265b78bb21621f`, `28d3895dd1a3aff160d0468b3def5384f18d951ea27d0fbf9079a6aebfe2c330`.

## Reconstructed source identities

The reviewed C# `Program.cs` snapshots 01–08 were
`dc55c4da16ba9167f189b35c8aaf0e445c9660e78f08f5705a68e6ed555c4476`,
`c5c0d0916c8a9f9a5e23e1e3a65378408515d9c6bbfc75790cb36446ef666593`,
`7e9aeb79dbecf9dd75f2b9ebda0ad298adf1832337d7777edc7ba5fa3a41ee0e`,
`fe95cee10479500fae417ef13692079e8f62aa7fd080a891ca87473ea1afd972`,
`19a13a51a68d520054850d4930f20282a7804db669aa4883e7ec1c4632ee807b`,
`bb53abef7f45e9f7fda14cfc752f5735e9d477ba7e5887334f07a074d036abb8`,
`b7f6e24d6659e9fb642fccca95da6b36719666af939a072eb22e32c06c48fc32`,
`5c33085f91b5acbdb97c6a3d5b4eae0798f19ce7ee7152f69067a6143659a97e`;
the unchanged project hash is `1f638de8c09974d0ca7dda36c16d766c24398e36a538dd5a5a8e1af128526234`.

Concurrent F# patch replacement prevented a trustworthy post-hoc hash of the
exact reconstructed snapshots read earlier. The superseded patch identities
above plus seed identities in `seed-review.md` bind that inspected lineage;
the replacement lineage must record fresh reconstructed hashes on re-review.

## Limitations

Static AI review only: no build or execution and no qualified human F#, C#, or
domain approval. The author's build approval is not independent review.

**Verdict: APPROVE**

## Correction after dynamic defect discovery

The preceding static `APPROVE` missed a real F# cancellation defect: inside
`tickWorld`, a successful due removal filtered `current.Pending`, but the loop
then restored stale `later`; direct removal also omitted cancellation. Dynamic
checking disclosed the defect after this review, so the earlier approval is
retained only as fallible review history, not acceptance of that lineage.

Narrow source re-review finds the repair coherent from Episode 02 through 08:
both direct and deferred successful removal filter only future queued removes
for the same ID, while `pending <- current.Pending` preserves that transition.
The already-extracted due batch remains in the local iteration, so a later
same-batch remove still executes and can report `missing_entity`. Deferred
spawns are not filtered. Episode 03+ detaches follower targets, and Episode 06+
removes only the outstanding request while retaining the issued ledger.

New F# patch SHA-256, 01–08:
`1b8e598dcf7d5db0a801bb0180fe988e3dc13d912f12c775581bc148301b7630`,
`434d86c65c9386eee0901bce2daad7d86433bcfd205509d90396374e6ece054c`,
`b1cac5273e5198f708fd0681b49f6d6eaa8a6d58e0f939767cc29f217e842385`,
`91b4af35ac02a869df65c98ddb8832ae857e7e0df6996e2dd535d2609d5c7bd7`,
`d72c4bcfbce5642978f76b6a1a2ddebf3a2160b78d866be026b38307a985cea3`,
`5fcf6d676bf7c95d512f9344ba5df9f77f4ffca5d8b9376abde77aa1dccd835b`,
`6061e3f02c74b4ffa5094f89b30f5e580970696ff5ec860ddf0ac2531405855b`,
`fa60f4a90aa7f7da2876afc2c79966ed618d003350c8555d23fc8ff460a1386e`.

New reconstructed `Simulation.fs` SHA-256, 01–08:
`8a78b52a093b2932ce8c2bd7e9512bda8f5dd9fb46eaf6ede1fa770b241c07cb`,
`2fecfdfb59716c28b16d982321209baca606a51189d3d6ae04677b80b144bd56`,
`915ee1b154f475d208d560ac0e523673efe71054e79e728558ff18e84abbce77`,
`d1c1d6af68e1ef94086117e1210457e9794373cc8573a80cf19c0442b33c98d4`,
`ae685481ca757bfb9d538640294d4558b69d8a16ee5601ba4a921b528f785eeb`,
`5436f4faa82c940257729a21971f65410bb08b78473f1d923a538fe6afe091cf`,
`2dcd1c63e49a70398e20727ba41f184e46a5ab06d0cabe3bbd53b7a24867b323`,
`3bf006c3fa864dc9f17bd326d9f90b6a0476922db5e75f57d794cbd08ab719db`.

The F# project hash remains
`5cc8c353cf25358615df7f9996b8b57fdc3a8cbf469c41b5c9b08324b13f831e`.
Author diagnostics are not independent acceptance; an independent validator was
still running at this checkpoint. No cases, results, measurements, build, or
execution were inspected here.

**Current verdict: COMMENT**

## Final validator-evidence disposition

The independent validator subsequently reported one full CLI invocation exiting
zero. Its curated evidence records status `passed` across 18 checkpoints, 80
cases / 608 case-checks, eight qualifying semantic faults, 12 transition
scenarios, and 16 downstream-applicability witnesses. The final report is
`ab6e5a53023929b7d731a6675a455c3c877f1b42064b9d258c84bce152f2fea5`
(SHA-256). Its provenance binds the same corrected F# patch hashes recorded in
the preceding section and the same reviewed C#, task, contract, guidance, and
seed identities.

This is validator-produced evidence, not a test or build run performed by this
reviewer. Reading the curated `index.json` and `report.json` unblinded this final
disposition to validation outcomes; it is therefore limited evidence acceptance,
not a continuation of the earlier source/outcome-blinded review. I did not
inspect case files or change code, cases, or size policy. The earlier missed
dynamic defect and corrective source review remain part of the record.

The evidence is model-free and records `live=false`, candidate execution false,
and zero integration/pilot allocations. It supplies no human language/domain
approval and no live-execution authority.

**Final verdict: APPROVE**
