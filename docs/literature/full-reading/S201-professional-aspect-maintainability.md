# S201 — Professional aspect-oriented maintenance exercise

**Full publication reading, 2026-10-02 HKT.** Marc Bartsch and Rachel Harrison, *An exploratory study of the effect of aspect-oriented programming on maintainability*, Software Quality Journal16(1),2008,pp.23–44, DOI [10.1007/s11219-007-9022-7](https://doi.org/10.1007/s11219-007-9022-7); online8May2007. Eleven professionals complete a randomized, between-participant paper-and-email exercise on Java or AspectJ. The reported tests find no significant differences, with a descriptive timing trend favoring Java. This is neither an equivalence result nor a trial of compiled, tested maintenance changes.

Existing native Zotero parent `LIDXWTCA` and note `W2R9Y3AC` preceded reading. Newly available final PDF **`63WDY7C9`v4828** is **22 pages,374,611 bytes**, SHA-256 `33a2418a826bbf4fb418be5d11ac869416a345084f04da3a8f99ab70aa87049c`. Its attachment URL is absent; no acquisition route is inferred. The earlier primary-repository/publisher access limit is superseded. All22 pages were read as text, including AppendixA's four questions,31 references, six numbered footnotes and both author biographies. Fourteen pages were inspected visually: **1,4–7,11–18,20**. These cover all nine figures, seven tables and the appendix questionnaire/scale. Remaining pages are text-only. No separate tutorial, original responses or source archive was acquired.

## What is compared

The mechanism is separation of crosscutting concerns versus the burden of reconstructing their interaction with base code. The treatment systems share requirements and a public interface for a small online shop, with authentication, authorization, null checks and logging. The authors state that outputs are identical. No independent execution/equivalence check is supplied by this reading.

| System | Reported size and organization | Material design consequence |
| --- | --- | --- |
| Java OO | About460 noncomment lines,11 classes, no inheritance; `ShopManager`154 lines | Several checks/logging concerns occur within the public-interface implementation |
| AspectJ1.3 AO | About490 noncomment lines,9 classes plus8 aspects, no inheritance; `ShopManager`80 lines | Concerns move to aspects, with explicit precedence preserving the intended order; three separate logging aspects keep their individual scopes narrow |

The AO version is derived from the OO template by moving crosscutting code. It has more components and more total source despite a smaller central class. This is a specific organization/language contrast, not a pure intervention on component size or a guarantee that separation reduces the authored envelope. Both versions permit a localized solution to the selected modification.

The proposed quality model uses component identification, output prediction and subjective understanding for understandability, plus time and changed noncomment lines for modifiability. These are distinct proxies. In particular, source-line changes are not interchangeable with elapsed effort, correctness or production maintainability. Section3.7 reverses the usual independent/dependent-variable labels; the operational assignment is the system, and the responses are participant performance/ratings.

## Participants, preparation and actual task

Eleven professionals volunteer without compensation, recruited through an author's contacts/colleagues and a Java user-group posting. Professional status is self-reported for respondents to the posting. All have object-oriented experience, described as a minimum of2–5 years; none has prior aspect-oriented experience. They are assigned randomly to the two groups, with five receiving AO and six OO. The allocation mechanism/sequence is not given. This is a convenience sample of motivated professionals, not representative sampling.

Before assignment to the questionnaire, participants complete five AspectJ tutorial sessions published over two weeks, at their own pace. Sessions cover basic aspects/debugging, advice/inter-type declarations, logging/reflection, contracts/invariants and caching. Admission requires submitting all five exercise solutions by email. The paper gives no total tutorial-hour measure or mastery equivalence between paradigms.

A pre-pilot with two PhD students revises the materials. A separate12-student pilot uses a1.5-hour tutorial the previous day and a60-minute task limit. Only one pilot participant answers every task correctly; four supply no modification solution. These pilot observations motivated the professional study's more extensive preparation. They are not independent replications of the final protocol or extra professional observations.

Each professional receives one program as a printable PDF, with copying disabled to discourage tool use. The experiment asks for an undisturbed setting, no advance inspection and no aids/resources, explicitly including pencils, Internet and programs. Participants are asked to spend approximately60 minutes but to finish rather than stop at that time; there is no submission deadline. This remotely conducted exercise relies on their declaration of adherence.

AppendixA asks participants to identify classes/aspects, predict every output line, propose a change rejecting shop use after more than five idle minutes, and rate understandability from1 to5. They record times before and after each question. The modification answer must describe line additions/removals/changes; either Java or AspectJ is allowed. **Detailed pseudocode and minor syntax errors are accepted if the proposed solution is judged specific enough to yield a correct program.** No compilation, behavioral test execution or independent temporal fault sensitivity is reported. All eleven receive full modification marks. OO participants extend classes; AO participants extend/add aspects as well as classes. No participant adds a class; two add an aspect.

This matters for the interactive-software background: a proposal concerning an idle-time threshold is not evidence that correct trigger boundaries, elapsed time, stale sessions or external effects were exercised. It is nevertheless a real professional cognitive task whose observed difficulty deserves its stated scope.

## Results and outcome-dependent omissions

Seven of eleven identify all components, nine predict all output lines, and all eleven receive full marks for the proposed modification. Most rate the programs easy to understand. Those ceiling effects limit discrimination; the paper accordingly emphasizes time and changed lines.

After inspecting outliers, the authors omit participant5's Q2 time and Q2+Q3 total, and participant6's Q1 time, attributing zero correctness to possible question misunderstanding. Both are OO participants. Participant6's60%-correct Q2 and its time remain. The available publication does not provide a predeclared omission rule or all omitted times; it does state that participant6 spent one minute on Q1. Thus timing samples differ by outcome and do not represent an unchanged all-assigned-participant contrast. Preserve the errors as outcomes rather than treating the retained sample as proof of a pure comprehension mechanism.

| Reported time, minutes | Retained OO / AO n | Median OO / AO | Mean OO / AO | Reported two-sided Mann–Whitney p |
| --- | --- | --- | --- | --- |
| Q1 component identification | 5 / 5 | 5 / 5 | 5.20 / 5.60 | .65 |
| Q2 output prediction | 5 / 5 | 23 / 29 | 22.40 / 29.40 | .25 |
| Q3 proposed modification | 6 / 5 | 22 / 27 | 21.67 / 25.20 | .46 |
| Q2+Q3 | 5 / 5 | 45 / 52 | 43.40 / 54.60 | .21 |

The subjective understanding median is2 in both groups, with reported Mann–Whitney p=.91. Reported unpaired t-test p values for Q2, Q3 and Q2+Q3 are .27,.42,.13; Q1 is not given a t-test. A passive arithmetic check of the eleven printed Table3 rows reproduces the timing sample sizes, medians and means above. This checks the publication's table correspondence, not the underlying self-reported times or inferential tests.

None of these reported tests is significant at.05 or.10. The paper's language about accepting null hypotheses and interpreting p values as probabilities of equal populations is too strong: nonsignificance in this small study does not establish equivalence or absence of a practically meaningful effect. Random assignment supports the intended contrast within this setting; disparate prior experience, remotely reported timing, omitted observations, tool restrictions and the selected small task bound its interpretation. The Java-favoring descriptive timing pattern remains evidence rather than being erased because of those limits.

## The changed-line tables do not reconcile

The final edition itself contains a material numerical discrepancy. Visually checked Table4 lists changed noncomment lines for every participant, while Table5 and Figure9 summarize a different range/median. Straight arithmetic on Table4 gives:

| NCLOC quantity | OO | AO |
| --- | --- | --- |
| Table4-derived range | 6–20 | 5–27 |
| Table4-derived median | 10.5 | 10 |
| Table4-derived mean | 12 | 13.2 |
| Table5 printed range | 10–26 | 6–33 |
| Table5 printed median | 15 | 16 |

Table7 prints an OO NCLOC mean of16.50 and p=.61, but no AO mean row appears in the table. Table6 reports NCLOC p=.93. Figure9 is visually consistent with Table5's larger ranges, without supplying exact observations. The prose's identification of the largest/smallest individual changes agrees with Table4. No recovered material establishes which numbers were analyzed or whether a definition/transcription changed.

Do not silently replace the paper's statistical results with a reanalysis of Table4, or treat Table5 as verified raw data. The arithmetic above establishes an internal correspondence gap. Exact changed-line effect estimates and their tests remain unresolved. The reported nonsignificant outcome is preserved as reported; it cannot establish equal effort, and the publication's timing result does not depend on resolving this separate table discrepancy.

## Access and related-method consequence

The paper links `http://www.personal.rdg.ac.uk/~sir04mb2/ShopSystem.zip`. HTTP/HTTPS web opens failed; ordinary native HTTP returned403, and HTTPS failed hostname certificate verification. The exact-archive and exact-title/error-data searches did not recover the original material in their returned passages. This is a bounded access result, not permanent absence or proof that no correction exists. A Scite exact DOI lookup returns truncated metadata and content denial for the article; it supplies no editorial-notice determination.

The publication distinguishes Walker/Baniassad/Murphy's1999 initial assessment from its own study: earlier purpose-specific Cool/Ridl/early AspectJ and Emerald comparisons versus this general-purpose AspectJ1.3/Java exercise, different participants/preparation and qualitative versus quantitative emphasis. The earlier method is a consequential conditional lead, not independently reconstructed here. The2010 comparative AOP review also appears in the targeted search and exact lookup; only supplied metadata/reference and three method-context passages are screened. Its synthesis and underlying cases remain unread, so no pooled verdict is borrowed.

For B01/B02/B10/B11/B12, the paper challenges automatic maintenance-benefit inference from separation of concerns while retaining a bounded professional result: a Java-favoring timing trend, no detected significance, and successful paper proposals in both groups. It does not contradict S200's historical concern/defect associations or S203's prepared-tool localization benefit, because those treatments and outcomes differ. Useful modularization may require tooling, expertise or larger/different tasks; this study does not measure those alternatives.

**Next consequential action:** inspect S202's available maintainer study and its released materials to distinguish perceived documentation usefulness from observed maintenance outcomes and ongoing update burden. S204's industrial history, the comparative AOP review/predecessor methods, and independent runtime/type/oracle routes remain open. The S201 original source/responses/NCLOC analysis are an explicit residual; their absence does not prevent the independent work. No experiment, installation or additional worker is authorized.
