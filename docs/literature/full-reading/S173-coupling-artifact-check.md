# S173 — bounded reconstruction of released coupling data

**Passive artifact inspection, 2026-10-02 HKT.** This supports the [complete S173 publication reading](S173-mutant-real-fault-coupling.md). It does not execute mutation tools, test generators, candidate programs, author analysis or benchmark suites.

The publication URL redirects from `ucd-csl` to [ComplexSoftwareLab/MUTATION_2022_Revisiting](https://github.com/ComplexSoftwareLab/MUTATION_2022_Revisiting). The inspected revision is **`731f4832a0da0fd0f662332b5f823b4b92cfa6fa`**, dated7July2023. Its complete recursive tree response has41,365 entries and is not truncated. This is metadata inventory, not41,365 file-body readings or proof of exact2022 experiment binding.

## Identities and coverage

All four selected READMEs were read: root57lines, CSV65, important-log26 and merged-map16,164lines total. Four337-row CSV tables, the337-ID cohort file, the ten-line intermediate count summary and all337 final suite-list files were parsed with own standard-library arithmetic. All final suite-list Git blob identities were verified against the pinned tree. Six selected triggering-test files were acquired: generated/developer pairs for Chart-11f, Chart-2f and Closure-50f. The12-line Chart-2f generated list, one Closure generated entry and five developer lines were read completely; Chart-11f's18,657 generated identifiers were counted programmatically with twelve opening entries inspected, not manually read in full.

| Released file | Bytes | SHA-256 |
| --- | ---: | --- |
| `csv_data/report.csv` | 12,905 | `3693145f34d7c606849978f70faebe49b4c50f757d547a2baea2f1b1ed9f9a6a` |
| `csv_data/bug_struct.csv` | 6,290 | `31dd66a3958e4af608c73128608b2ac869e9a9ac05c02063773a1c5431075c34` |
| `csv_data/major_mutators.csv` | 25,160 | `185a8eaafcf4749b0f4417da518322f96a0a372b346c22997232174259d221ff` |
| `csv_data/pit_mutators.csv` | 64,931 | `08fcb094cf8886388d45d5b2079fbe3e8903f6d9b64b413fbfc23df084fafa3a` |
| `important_log_files/valid_bugs` | 6,022 | `6cf92d61bfe4f83faa774c11a5b362987dc7188549f146bf77b775b405f90f65` |
| Major kill-map archive | 82,852,608 | `bccd7abd60a9dd87f8a709472007515c2f034f7831464894f3e2aabec5d0c38d` |

The Major archive is stored under the existing native S173 parent as **`IMDHI47E`v4977**, with native byte/hash readback. Its acquisition follows the public Git LFS media URL and matches the repository's pointer identity. The Pitest archive and distance CSV have pointer-only inspection:112,670,188bytes/SHA-256 `e063281324d0f1aaa9a05123524b991d85af81b04976a6597dce00defd612c38`, and76,183,225bytes/SHA-256 `90f99f07b96b0ffa905d194d2dafec4973f8444922a06b19c84fa933ceaafbcf`. Their payloads remain unacquired. Pointer byte counts/hashes are not actual payload verification.

Sixteen small text/CSV/list files total886,543bytes, including the later three-line Closure-50f trigger check; the337 additional suite lists total59,206bytes. Per-file identities, own intermediates and source bodies remain ignored local artifacts. None is committed as a copyrighted body or represented as an independently performed experiment.

## What reproduces from the summary data

The four CSVs and `valid_bugs` have the same337 unique fault IDs. Project counts reproduce TableI. Boolean coupling flags match positive coupled-mutant counts in `report.csv`, and each row's combined count equals its two tool counts. The four fault categories reproduce **199 both,38 Major-only,35 Pitest-only,65 neither**.

All TableIV minimum/quartile/median/mean/maximum values reproduce to printed precision using the **237 Major-positive** and **234 Pitest-positive** rows separately. Across all337 report rows, Major totals166,216 mutants/2,119 coupled and Pitest663,563/6,140. These totals, conditional mean percentages and existence rates are different summaries.

All337 patch rows satisfy additions+deletions=total. Coupled/non-coupled groups have272/65 rows, medians6/4, means10.882/7.985 and maxima225/38 changed lines. This reproduces the descriptive contrast without rerunning the published significance test or inferring a significant difference.

## Operator and denominator correspondence

The operator tables reproduce Figure4's five Major and eleven Pitest nonzero exclusive-fault counts. Major's2,100 operator-attributed coupled mutants also reproduce Figure2a's printed leading proportions; Pitest's6,140 reproduce its corresponding shares.

Major operator rows disagree with `report.csv` on total counts for **eleven faults**. Only **Closure-50f** differs in coupled counts:6 in the operator table versus25 in the report, accounting for the19-mutant aggregate difference. The fault remains positively coupled under either count. All337 Pitest rows reconcile on both total and coupled counts. This is a bounded release correspondence issue, not a reason to replace the reproduced272-fault result with a different rate.

Figure3's leading bars fit **covered** denominators. For example Major COR is382/(382+15,883)=2.349%, versus1.436% when10,343 uncovered mutants are included. Pitest BigInteger is4/(4+119)=3.252%, versus3.150% including four uncovered mutants. Other leading bars show the same pattern. Full plotted tails and the original plotting implementation are not reconstructed, so no exact all-bar reproduction is claimed. Both definitions retain a small coupled fraction; the denominator matters when interpreting generation cost and yield.

## Suite selection and intermediate counts

The337 final suite-list files contain **2,828 distinct suite IDs**:290 developer,1,317 EvoSuite and1,221 Randoop. Counts per fault are5–11; their distribution is5:32,6:80,7:23,8:26,9:31,10:55,11:90. Forty-seven retained faults have no developer-suite entry in these lists. A listed suite is not a test-method count or an execution newly performed here.

The intermediate summary totals831 faults and explicitly gives423 with **at least one** generated triggering suite. Its categories0:408,1:52,`<5`:124,`5-10`:192,10:55 are printed labels, without an inferred alternative boundary convention. They do not support the paper's literal at-least-five description of all423 faults.

For a targeted correspondence check, Chart-11f has all ten retained generated suite IDs represented in its triggering-test list. Chart-2f's final list instead contains three EvoSuite suites, Randoop5 and its developer suite. Its generated triggering list names only Randoop1/5, with no EvoSuite entry. The raw check below confirms actual kill observations from those three EvoSuite suites. Therefore the release cannot be assumed to implement the printed all-suites-triggering filter literally. This is not a measured correction to the study's overall coupling rate.

## Two raw-map checks

The Major archive was streamed through1,000 member headers and5,064,384,536 declared uncompressed member bytes to retain only the selected Chart-2f and Closure-50f CSV/log pairs. Unselected bodies were traversed, not read as research content or extracted. No downloaded code was run. Only the four selected bodies below are credited for passive parsing.

| Member basename | Bytes | SHA-256 |
| --- | ---: | --- |
| `Chart-2f-MAJOR-merged.csv` | 12,951,727 | `c37e1547da369824921ae517e4f0b021c5bba9f6b119f458e351a889b8d8b004` |
| `Chart-2f-mutants.log` | 181,702 | `23fc70126175893e889c37fbfd3c405253bdc385e6163d7578f43f36be31c82e` |
| `Closure-50f-MAJOR-merged.csv` | 196,666 | `ad64af1a68f9fd27e952ee0804691a0e82ba28418978201b6534c570f662d5ff` |
| `Closure-50f-mutants.log` | 142,240 | `9a5dcc6bfbf1ce837bdd5ee09d61ee2bf9469f63c17bf9f9876abe1f0cd1a0cf` |

Each CSV row names a mutant followed by its killing tests; rows have variable length and no header. The developer trigger names receive the documented fault/developer-suite prefix; generated names already contain their suite prefixes. Own set arithmetic applies a nonempty killing set wholly contained in the supplied triggering set. Both cases' CSV IDs and log IDs are unique and agree in count.

| Check | Chart-2f | Closure-50f |
| --- | ---: | ---: |
| Mutant rows/log IDs | 972 | 587 |
| Rows with no recorded killer | 184 | 190 |
| Rows with at least one killer | 788 | 397 |
| Coupled under the nonempty subset rule | 10 | 25 |
| Coupled count in `report.csv` | 10 | 25 |
| Distinct observed killing-test names | 11,620 | 196 |

Chart-2f's map includes kill observations from all five listed suites, including the three EvoSuite suites absent from its triggering list. Those observations can disconfirm coupling and were not universally removed. Its ten coupled mutants span LVR1,COR2,STD7. Closure-50f reproduces the report's25 coupled mutants, distributed COR4,ROR6,STD6,LVR4,AOR5. This supports `report.csv` for that disputed row, while the operator CSV's6 remains unreconciled; no cause is invented.

These checks reproduce two observed relations without executing a test or establishing source/oracle correctness. They also verify that empty killing sets are not being credited as positive witnesses in these two reported results. The other335 raw cases, generated test bodies, original selection/analysis implementation and Pitest/distance payloads remain outside this bounded inspection. The complete study is not reproduced.
