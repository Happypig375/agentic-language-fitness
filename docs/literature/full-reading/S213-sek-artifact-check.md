# S213 — bounded release-source correspondence

This passive inspection supports the [complete author-edition reading](S213-transient-sequence.md). It does not execute Sek, Monolith, a benchmark, a compiler or an author script.

## Identity and actual coverage

The [official opam record](https://opam.ocaml.org/packages/sek/) identifies version **20260619**, published June22, and a [source archive](https://gitlab.inria.fr/fpottier/sek/-/archive/20260619/archive.tar.gz). Normal HTTP retrieves it despite the web tool's denial at the GitLab root. The archive is **224,070bytes**, SHA-256 `e95ecd31c7767f926a5a8fb3d240dc49605e662a09df0c7a964a95ce0f3a7fe9`, MD5 `56c31c65f3b0431943218f58d0ebda99`. Its SHA-512 is `dfe7886d046c119780a196e17ac7efa8e989bcef3743f01d08d9aabc871fdc6b59d16b7445d01b30d3eb1bf4addca6c46e283065ff207ff4354a2ce6af245be7`; MD5/SHA-512 match the opam declaration. The archive prefix identifies **`2f75899639fdff427b81069114fcdd9464939825`**. This is a dated release, not an exact cryptographic binding to the paper's benchmark runs.

The145 regular files contain960,013uncompressed bytes. No `.out`, `.csv`, `.tsv`, `.json` or `.pdf` file is present; this filename inventory is not proof that no public data exist elsewhere. Native attachment **`JI8C6U7I` v5087** is imported under the existing parent and read back to the same SHA-256. Existing memberships and attachments remain. The archive and extracted bodies are outside public Git.

**Eleven files are fully read:** root README and CHANGES; benchmark README; `benchmark/src/stack/Main.ml` and its Makefile; `benchmark/src/Time.ml`; `benchmark/src/Settings.ml`; `src/PublicSettings.ml`; `src/Owner.ml`; `benchmark/src/StackFixedArray.ml`; and `benchmark/src/stack/StackVector.ml`. Selected ranges: `src/PublicSignature.ml`360–429 and1798–1845; `src/Sek.ml`327–391; `src/EphemeralSequence.ml`665–761; `benchmark/make.sh`302–360, its K/M suffix definitions and surrounding stack/heap/threshold registrations found by text search. These selected ranges are not full-file readings. An earlier combined output overflowed; the needed passages were reread in smaller outputs before crediting them.

## Ownership, conversions and invalidation

The release's `Owner.fresh` uses a centralized integer counter, checks wraparound and tests owner equality against the distinguished non-owner value. It is not an atomic multicore ownership protocol. This agrees with the paper's separate concurrent-push limitation; no whole-library thread-safety claim follows.

For a long input, `Sek.snapshot` calls `snapshot_and_clear_long(ESeq.shallow_copy s)`. The shallow copy flushes inner chunks, gives a new owner identity to the original and copy, copies outer front/back chunks and shares the middle. Its comments explicitly preserve existing iterator validity. The public API documents O(K), including the possibility that introduced sharing increases later costs.

`snapshot_and_clear` instead transfers the sequence's data, marks the ephemeral wrapper for lazy reinitialization and invalidates iterators. Its documented cost is O(min(K,n)); push-built input has an explicitly stated amortized O(1) interpretation. Short snapshots copy their elements into the short representation. `edit` copies the boundary representation under a fresh owner, sharing the middle. Therefore the paper's schematic O(1) long-snapshot row does not specify the preserving conversion in this release. No exact final-edition correspondence is asserted.

Most ephemeral changes invalidate all associated iterators. Updating through an iterator keeps that iterator valid while invalidating others; `reset` can restore an invalid iterator. Runtime checks default to enabled. Disabling them permits arbitrary behavior on invalid use; it is a configuration choice with an obligation, not a verified way to retain iterator semantics after arbitrary mutation.

## Timing and workload correspondence

The two `bigstack` registrations say they produce the paper's stack plots, choose100million requested pushes,25peak lengths from1 to100million, and three runs. The transient/persistent sides use the listed paper comparators, with10/20second timeouts. Raw completion/missingness logs are absent from this archive. A commented-out additional vector is described as uncompetitive; it is an author exclusion rationale, not an independently reproduced result.

`Main.ml` updates one sequence/reference, not a collection of old versions. Each pop checks the expected integer. The fixed array is sized to the known maximum; the resizing vector doubles when full and halves at or below one-quarter occupancy. Timing encloses creation and the push/pop loops, while `Gc.compact()` occurs before `Sys.time()` starts. This is CPU time per requested operation, not wall-clock frame response. The configured minor heap has1,048,576words, consistent with8MiB at8bytes/word despite an imprecise1MB source comment/printed label.

There is a bounded normalization discrepancy: repetition count is `floor(p/n)`, but elapsed time is divided by2p rather than `2n floor(p/n)`. At p=100million and n=21.5million, actual pushes are86million; the displayed ns/requested-operation value is0.86 times ns/actually-executed-operation. This is the minimum factor among the25registered lengths. The same divisor applies to every comparator at that n, so within-size time ratios are unchanged by this normalization alone. It affects absolute per-operation interpretation; it does not erase the reported relative advantages or prove those exact source bytes generated every published point.

CHANGES attributes up-to4× packed-access gains and10–30% persistent-concat gains to the June release, with no significant ephemeral-concat difference below1million and possible slowdown up to30% above it. These are release-note reports without inspected raw rows, separate from the paper's two stack plots. The release documents corrected complexity claims, but that does not establish which final-edition paragraph changed.

## Elementary checks on the printed analysis

AppendixB p.32 defines front potential in units of C″ as `2 abs(K−nf−nif) + (K−nm)`. Changing the first sum by one can increase potential by **2C″**, rather than the printed C″. For K=16, nf=8→7, nif=0 and nm=16, the value changes16→18. In the full/full push case it changes32→2, so the displayed decrease is30C″, not31C″. Charging2C″+O(1) and using the actual decrease covers the described local/full-push costs for K≥2 without changing O(log_K N). The pop case's adjacent-density inequality supplies its stated release of more than K units. These are our algebra checks on the presented cases, not a complete mechanized proof or evidence that the implementation fails.

The consequential correspondence gaps are the exact final edition/run, preserving versus consuming snapshots, and costs under retained histories and other operation mixes. They do not justify running an unapproved experiment or repairing the author's library within this literature assignment.
