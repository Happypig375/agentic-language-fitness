# S212 — passive AEC-v2 artifact reconstruction

This note supports the [complete arXiv-v1 reading](S212-persistent-iterators.md), with no compilation, tests, Docker execution or author-script execution.

## Identity and coverage

The paper cites [Zenodo10.5281/zenodo.19392634](https://zenodo.org/records/19392634), version `pldi-2026-aec-v2`, published April3,2026. Its description identifies source commit **`cd7d155`** and an associated image digest beginning `db63db4`. The source archive and separate README are downloaded normally and checked against Zenodo's declared MD5. The1.9GB AMD64 and1.8GB ARM64 images are metadata-only, not downloaded; the archive is not a fingerprint of the exact macOS paper run.

| Asset | Identity and native attachment |
| --- | --- |
| Source tar.xz | **67,824bytes**; SHA-256 `2562ecf343ed86c8c4cae965eac3e50af0e850991ed70abe200e7bed03b0f38e`; MD5 `2220144091ef31e81f6acb6caf7517d5`; **`TC67MAA9` v5092** |
| AEC README | **12,753bytes**; SHA-256 `49d37020159ee54d74c567f102514e2aadded8d2de9d07b75cd13684839f0326`; MD5 `906cb3c486041a146c58c778d8d3dae8`; **`B5HEQMFP` v5094** |

Both attachments are read back under the existing S212 parent with matching hashes, preserving collections/earlier attachments. The archive contains **121regular files /603,709uncompressed bytes**, including66AppleDouble metadata files and55ordinary files. No `.csv`, `.xml`, `.json`, `.pdf` or `.png` result artifact is present in this source package. Bodies remain outside Git.

**Eight complete files** are read: the separate AEC README; root README; `xmake.lua`; `src/testing/memory.cpp`; `scripts/draw_graph.py`; `src/libfpp/containers/iterator.mpp`; and both `src/examples/editor.stl.cpp` / `editor.fpp.cpp`. Selected coverage is `test/vector.cpp`318–727; `test/set.cpp`440–554 and656–810; `containers/vector.mpp`296–337; `containers/set.mpp`762–867; `core/alloc.mpp`55–167 with allocator-selection/heap-definition search context; `core/monoid.mpp`142–158 and227–275; `core/internal_itr.cpp`294–350 and1460–1474, with additional symbol-location snippets. The remaining library/tests, including the large sequence implementation, are not fully read. A truncated search listing is not credited as full-file coverage.

## What the actual benchmark programs return

The source confirms independent cursor ownership. `begin()` creates an iterator value; its zipper constructor increments the source-node reference count. `insert`/`assign` swap the iterator's own context. A nil-sequence insertion constructs a fresh singleton and returns a new zipper; it does not rebind the originating container. The explicit extraction operation is `finalize()`, corresponding to the paper's `value()`.

The vector and set **Append*** registrations repeatedly call `temp.begin().insert(elem)` and discard that temporary iterator, then return `temp`. Under the documented semantics and the inspected empty-input branch, temp remains empty: this performs repeated insertion into temporary empty-version cursors, not construction of the stated n-element result. This is a source-level output mismatch, not an executed timing correction. No original run log establishes whether the paper used these exact bytes or a corrected variant.

Vector **Update*** creates xs2, changes an iterator over it, discards that iterator at loop end, then returns the original xs2's first element. The local traversal may do substantial update/reconstruction work, but the resulting container is neither extracted nor checked. The Folly counterpart also copies `folly2` but updates `folly`, a separate state/setup discrepancy. By contrast, LibFpp **Erase*** keeps the cursor through all erasures and returns `finalize()`. Mutable vector erasure proceeds from the back, avoiding quadratic shifts; it is not the forward-erasure algorithm used in the paper's motivation. Baseline mutable copies occur inside the timed lambdas. Some source registrations for Immer's modifying iterator-labelled cases use ordinary container operations; their existence does not supply the absent iterator cells in the paper.

The ordinary vector append builds a growing result, indexed update copies its starting value inside timing, and concat joins ten references/copies of one repeated chunk. Intermediate versions are overwritten. Set construction inserts sorted0…n−1 values. These details preserve meaningful indexed/concat/erase evidence while preventing transfer to arbitrary operation mixes or a retained-history workload.

## Allocation and control-condition interpretation

`memory.cpp` adds requested bytes on every allocator call and never subtracts them on deallocation. LibFpp's `raw_alloced` likewise rises even when a freed64byte slot is reused; a separate `alloced` counter is decremented but is not the plotted measure. Figure9's released procedure therefore measures **cumulative requested allocation**, not current reachable or resident memory. An illustrative doubling-array calculation `(1+2+4+8+16)*8=248` bytes matches the README's ten-element STL example even though its final16-slot buffer is128bytes. This is our arithmetic illustration, not a reproduced run.

The benchmark explicitly instantiates `InlinedVector<T,1000>`; the1000-element inline capacity is a chosen parameter, not a library-wide default. Zero measured heap allocation below that capacity excludes its inline storage. None of these counters includes all process/allocator reserve, stack or retained-history memory.

The README says to reproduce “unopt” by rebuilding in debug mode. `xmake.lua` selects different compiler optimization settings between modes; `alloc.mpp` enables the CMA with literal `#if 1` and disables the `operator new` implementation with `#if 0`, without a debug selector. Thus the documented mode switch is not an isolated change of allocator in the inspected source. Dependency constraints are also broader than the exact versions in the paper. This limits causal attribution and recipe correspondence, not the existence of the reported point comparisons.

The graph script reads Catch2 mean/lower/upper values and plots them; its CSV export retains means. It contains no computation of the paper's caption ratios. The build file requests an80% benchmark confidence interval and seed12345. The README's printed example has100samples, but this is not a recovered sample log for every published point. Its figure numbers6/7/8 precede the chosen paper's7/8/9, another source/version boundary.

## Bounded semantic checks

The set scan accumulates0…n−1 in `int`. On a32bit-int target, the registered70k/80k/90k/100k cases exceed the signed range; at100k the mathematical sum is4,999,950,000. The [C++ draft arithmetic rule](https://eel.is/c%2B%2Bdraft/expr.pre) does not define signed overflow as ordinary wrapping. This identifies a source-level validity concern in those cells, without claiming an observed optimizer effect or that every point is unusable.

The generic iterator advertises a random-access tag, but the paper gives logarithmic jumps and the source returns values from `+=`. The [standard iterator contract](https://eel.is/c%2B%2Bdraft/iterator.concept.random.access) requires constant-time advancement and reference-returning compound assignment. An STL-like syntax/tag is not proof of full standard-algorithm substitutability. No compiler/concept test is run.

Finally, Figure3's STL editor and its source call `string.erase(pos)` for backspace. The [string erase contract](https://eel.is/c%2B%2Bdraft/string.erase) makes the omitted count default to the remaining suffix, not one character. For buffer `abc` with cursor position2, the printed backspace removes `bc`, whereas the proposed one-character action would retain `ac`. The persistent-cursor design still demonstrates an economical state representation; the paired listings do not establish equivalent editor behavior or measured development savings.

These findings delimit the evidence. A corrected artifact or exact original outputs could resolve correspondence; passive reading alone cannot produce replacement benchmark outcomes. No author code was changed, and no experiment is authorized.
