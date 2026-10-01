# S167 — bounded released-report check

This supplements the [complete five-page reading](S167-instrumentation-flakiness.md), 2026-10-01. Public [Bitbucket package at commit `9fb5651d0cd8ede72c58861cf0282058ca1eee96`](https://bitbucket.org/unshorn/inst-study/src/9fb5651d0cd8ede72c58861cf0282058ca1eee96/) (2 February 2023), acquired through its native public API. No study Java code, instrumentation, build or author analysis was executed. The operation was passive inventory/reading and our own descriptive arithmetic.

## Coverage and boundary

Root and dataset listings, all **eleven results-list pages**, and the three textual files below were read. The inventory contains **1,080 ZIPs, 540,332,537 listed bytes**, exactly nine project names × six configurations × run indices 1–20. The eleven-project dataset file also includes excluded hbase/ozone; retained identifiers agree with Table I. A complete name inventory is not complete file coverage. No analysis script appears in the listed root/dataset/results package.

The selected check requested eighty-four ZIPs: all twenty Exhibitor baseline and JFR runs; Flow baseline/OpenTelemetry runs 1 and 20; and all twenty MockServer baseline/OpenTelemetry runs. **47 ZIPs / 8,174,391 bytes** were fetched before **HTTP 429**; further requests stopped. Their **3,401 XML reports** were parsed for test identity/outcome, suite counts and selected non-success messages, not read in full for every property/stdout/log field. The 37 requested but unfetched files are MockServer baseline runs **2–10 and 13–20**, and all twenty OpenTelemetry runs. The other 996 inventory entries were outside this selected download request. Exact manifest follows; local cache remains outside Git, with no claim that these ZIPs are Zotero attachments.

## Checks and unresolved discrepancies

| Check | What the released fields establish | Limit |
| --- | --- | --- |
| Exhibitor baseline, all twenty runs | Fifty-three distinct regular class/method identities all pass. Each normally appears in individual-class and aggregate suite XML, giving **106 raw success entries**. | Raw report entries are not independent test identities. |
| Exhibitor JFR, all twenty runs | Nineteen runs have identical relevant outcomes. Run 6 has raw **104 success / 2 failure / 2 skip** entries, 55 distinct keys including setup/teardown. Raw averages are **105.9 / .1 / .1**, matching Table III. | `TestZookeeperConfigProvider::testConcurrentModification` conflicts between aggregate skipped and class failed records. Initial dictionary deduplication cannot adjudicate it; neither state is silently chosen as ground truth. |
| Exhibitor JFR score | Only nineteen of 190 unordered run pairs can differ. Jaccard distance is at most one, so the printed mean formula gives **at most .100**, not the reported **.200**. For the single common varying regular test it gives .100. | Requires the paper's stated common test set and mean over all run pairs. Duplicate resolution cannot increase this bound. Author implementation is unavailable in the listed release; cause and other rows remain unresolved. |
| Exceptional JFR run | Setup reports `IllegalArgumentException` about repeated Curator instance keys, with the same localhost port. | Observed failure is not proof of JFR causation. |
| Four Flow runs | Each has 4,400 distinct identities without duplicate keys. In both baseline and OpenTelemetry, run 1 errors on `FrontendToolsTest::getPnpmExecutable_executableIsAvailable` because pnpm is too old; run 20 passes. | Paper's named `FrontendToolsLocatorTest::toolLocated` is absent from these four reports. This is not a reconstruction of all forty runs or an instrumental attribution. |
| Three MockServer baseline runs, 1/11/12 | Each records 2,870 successes. | No instrumented MockServer ZIP fetched; the paper's port-conflict attribution remains unverified from artifacts. |

There are 2,120 duplicate-key occurrences in the selected parse, all from the forty Exhibitor runs, and one conflicting regular-method outcome. These observations preserve both the matching aggregate averages and the unresolved score/identity boundaries. No corrected universal score, runtime replication or causal effect is claimed.

## Textual files read completely

| Relative path | Bytes | SHA-256 |
| --- | ---: | --- |
| `README.md` | 447 | `e08e19940734ac5873590ccd9afc781e15b9d619b70898f4d1a04caf3e17cc1a` |
| `dataset/README.md` | 416 | `8e7b77b6bd3e722a56b5fdb500dcc7e0fa9f41cd9cd5f7684f9f367c37acb696` |
| `dataset/repos.txt` | 289 | `bd0ff72a326831e2ee5bf5262c940c5714667890d74161dbe2c888ed0e79b4a1` |

## Cached ZIP manifest

Paths below are relative to the pinned repository; hashes were rechecked against cached bytes. XML count is report files parsed for selected fields, not unique tests or full textual reading.

| Path | Bytes | XML reports | SHA-256 |
| --- | ---: | ---: | --- |
| `results/testresults-inst-exhibitor-baseline-1.zip` | 14268 | 21 | `83e836e5d1ae3b59798d5f42e44e05db59b5e147b412e323a04ba87c0e97bffb` |
| `results/testresults-inst-exhibitor-baseline-2.zip` | 14223 | 21 | `78a9bd136c6c0917392702bb9e399d88be1ded8c77d23e48c547a1f9e0334905` |
| `results/testresults-inst-exhibitor-baseline-3.zip` | 14252 | 21 | `5ba9718b9a47cd04037ab344f301927c4faa590135761bb59035654768b10782` |
| `results/testresults-inst-exhibitor-baseline-4.zip` | 14235 | 21 | `4418077e00a1e6011aaf091c1619dc3b01bd0a76d5168e445fe48c844e5310e4` |
| `results/testresults-inst-exhibitor-baseline-5.zip` | 14230 | 21 | `6463ced35fafcbaae342176676abee1e2a1a98c1dbe2d8fe0572e48f86122e2b` |
| `results/testresults-inst-exhibitor-baseline-6.zip` | 14255 | 21 | `607b001fddddafce2bff6fa512e7c8bd45c371d34181fda6915d14f5885fc8c9` |
| `results/testresults-inst-exhibitor-baseline-7.zip` | 14237 | 21 | `50e7b440cebc035ca29bc33f81c4d525eb3a5db7176b01918bc4dc9a810a65f8` |
| `results/testresults-inst-exhibitor-baseline-8.zip` | 14237 | 21 | `0e3d61cb08e850402362e8c1148ea9b0a3e968f3af0ae82aa97ec51881f2c51b` |
| `results/testresults-inst-exhibitor-baseline-9.zip` | 14246 | 21 | `5008fc78dd1b76d66a8bd19a012aa505fced2d1fdf86f1d678e6240146e95d07` |
| `results/testresults-inst-exhibitor-baseline-10.zip` | 14301 | 21 | `41e5f3cef52c08e986f716e3b874f49345084aa9387277d2e7501cf3038860c7` |
| `results/testresults-inst-exhibitor-baseline-11.zip` | 14310 | 21 | `19a775ef80175edab383f1f49f279ce5a74cf3b6fcf3076b9e39c9d687eaa984` |
| `results/testresults-inst-exhibitor-baseline-12.zip` | 14308 | 21 | `ca28400761f110a6459d6161157bdc236ff6f6709bac6b506cdb788e1f3d2880` |
| `results/testresults-inst-exhibitor-baseline-13.zip` | 14305 | 21 | `3db56b028023cb5bf43c6e0f159d69686fcf006cf3eb6358f03c9e4461d2fa9f` |
| `results/testresults-inst-exhibitor-baseline-14.zip` | 14304 | 21 | `342747bc2d42571134b291745d8f4c3f1fd3d2c72c3f864cab9c0039d5ca4a09` |
| `results/testresults-inst-exhibitor-baseline-15.zip` | 14341 | 21 | `1c26fea9f3da84331b58bbb336c7b0b164248bab942e8809a50efee5b86dbb4c` |
| `results/testresults-inst-exhibitor-baseline-16.zip` | 14314 | 21 | `ee34674cefeae938519372c82f8612aab435d0641939a769e100f183f5de2d76` |
| `results/testresults-inst-exhibitor-baseline-17.zip` | 14328 | 21 | `7a413ac7bcf39124b1431409216a1558b1859b2eba372d2ebd26210f8055ae8d` |
| `results/testresults-inst-exhibitor-baseline-18.zip` | 14325 | 21 | `4d146d6d33edfa286c9fab0cf86ceefb47810295e9bda11ea701c491713674cd` |
| `results/testresults-inst-exhibitor-baseline-19.zip` | 14333 | 21 | `9f5552db6152704b4a37d7957fac08c14068f91f3330845329ed392f11cd45a3` |
| `results/testresults-inst-exhibitor-baseline-20.zip` | 14375 | 21 | `5a4addcbbd9b6448122c652034582720a154f20d8fbad92cfdf467aac6f94a02` |
| `results/testresults-inst-exhibitor-jfr-1.zip` | 14079 | 21 | `21cc3baf508c2b3b056c67f33ee7cbc7d852fbd0b826409afa83329aa18782d2` |
| `results/testresults-inst-exhibitor-jfr-2.zip` | 14080 | 21 | `b56dc8f1f6f1a1466327eafac146e20cf92e6e45e651d4a13b0c8fbbe814f24b` |
| `results/testresults-inst-exhibitor-jfr-3.zip` | 14065 | 21 | `fab616423d1c59f616eafc90cbd1e2523df770f1ffa8d4f470c1e17905d551b6` |
| `results/testresults-inst-exhibitor-jfr-4.zip` | 14068 | 21 | `7e38e454a3480411dd4918ef690537870f6831e2878af3a3b8d1cd1cbe2c55e3` |
| `results/testresults-inst-exhibitor-jfr-5.zip` | 14073 | 21 | `3da824faead7d885bb166a20041ba964b33731299daad26f1a20ce728c49f29e` |
| `results/testresults-inst-exhibitor-jfr-6.zip` | 15607 | 21 | `5a1a4c1a15f6615af4e87c27b72df9d4d52a32b71883069e32f1c8cdaf400923` |
| `results/testresults-inst-exhibitor-jfr-7.zip` | 14076 | 21 | `4daa55bdfcfe08836c7f052964f43518d7c978b8525efc18cbe96ed99e7351f1` |
| `results/testresults-inst-exhibitor-jfr-8.zip` | 14079 | 21 | `469dd06c4eefbbe723f1f2b2a6031f97f59e44611ffd4bc731b9162d384a6344` |
| `results/testresults-inst-exhibitor-jfr-9.zip` | 14072 | 21 | `119e97e4af120ed7ec793b09d49d5ca181adfd1fb10bee30be4ca5293d4cf05e` |
| `results/testresults-inst-exhibitor-jfr-10.zip` | 14122 | 21 | `3ee0758e5d7f40bab61574a1d94c8cf341b4e5e661ee83fd96d2e337b878431c` |
| `results/testresults-inst-exhibitor-jfr-11.zip` | 14106 | 21 | `1a391dcdec2f94667ddc4447478e09846367cbb879ee6527de85520160ba55a3` |
| `results/testresults-inst-exhibitor-jfr-12.zip` | 14099 | 21 | `b7b30e0912bc60dc124625d966d8c840b0bc60179d9ee4708dd90334a5612d58` |
| `results/testresults-inst-exhibitor-jfr-13.zip` | 14100 | 21 | `888d55c9ad67b81b91689a1e518a12ec574a858ded6fe72b34287f133e6f48fe` |
| `results/testresults-inst-exhibitor-jfr-14.zip` | 14104 | 21 | `e6bd2b72bececb1ce9123f01a4140390b99d2f442a5c1eca2404275cadc0340e` |
| `results/testresults-inst-exhibitor-jfr-15.zip` | 14102 | 21 | `7b03c94bc7f0fe625ddb1be5d8d1d598ad34559d86b015ed2e51c0ef3e4fb933` |
| `results/testresults-inst-exhibitor-jfr-16.zip` | 14101 | 21 | `51fa9eace8890b14d2a66c34b3064da438c915d89cf3527b9e7030581bdf0762` |
| `results/testresults-inst-exhibitor-jfr-17.zip` | 14102 | 21 | `890ee5fbe80e693559a6efda1b310548c1826ec96ee4a12b9348f2e4b10ba83b` |
| `results/testresults-inst-exhibitor-jfr-18.zip` | 14096 | 21 | `fb8f502784526d6780488f774018fac233de55779c7e483d717d9b441b46d169` |
| `results/testresults-inst-exhibitor-jfr-19.zip` | 14091 | 21 | `3bf730d1cca8cb189312759dc2882467c8bf1735c88de8e79439dd8760b766a2` |
| `results/testresults-inst-exhibitor-jfr-20.zip` | 14161 | 21 | `89e546e38751576ebb9be5f1f0521d6969acbf60f26321cc4b7346725cf77f74` |
| `results/testresults-inst-flow-baseline-1.zip` | 1113937 | 419 | `5b82b75da3bc05921514ca1eaf0aed0a3ef58c677a412cd59d1526aebe8efa32` |
| `results/testresults-inst-flow-baseline-20.zip` | 1113911 | 419 | `16419d0bbedf9eba3c7d6fca281a98732effae31054a4055df5562241a59b6a1` |
| `results/testresults-inst-flow-opentele-1.zip` | 1114629 | 419 | `768c291fdb4521d539cc5a30b4d4a0558f982528bb4888bdba9be0bb3f2a4713` |
| `results/testresults-inst-flow-opentele-20.zip` | 1113379 | 419 | `fe8f5b6e24e428cc2bf2a0fce82d162751c94bae296b09f3e8585bf0c534c5da` |
| `results/testresults-inst-mockserver-baseline-1.zip` | 1049562 | 295 | `f0c67562a470f85fc3f394ba2de7ef722ff07fc0d63b573cb5da802adfb3ad58` |
| `results/testresults-inst-mockserver-baseline-11.zip` | 1050294 | 295 | `5c06c863d2746355fcacd414e77eb286d17a85bad6d8cb122b4c55fc83addb9a` |
| `results/testresults-inst-mockserver-baseline-12.zip` | 1049569 | 295 | `064cbd9fb98a951c8ce62ecbc15228cbacdaf676ea984449ca10912da698ff6e` |
