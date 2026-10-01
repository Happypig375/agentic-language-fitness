# S181 — bounded check of the released material

This supplements the [paper reconstruction](S181-displayed-metric-anchoring.md). It records passive file inspection and own descriptive arithmetic, not execution or reproduction of the authors' analysis or experiment.

## Identity and coverage

The paper cites concept DOI [10.5281/zenodo.4001763](https://doi.org/10.5281/zenodo.4001763). Its [primary API](https://zenodo.org/api/records/4001763) resolves to record **4498084**, created February 3 and modified February 4, 2021, with version DOI [10.5281/zenodo.4498084](https://doi.org/10.5281/zenodo.4498084). The metadata's version field is unset; concept and record identifiers are not two independent packages.

`the_mind_powerful_place-replication.zip`: **618,482 bytes**, SHA-256 `f4a96c5b9880dfe2874e55f7381e7ff11a975e72eb6110d2fbf4484f8c8d9462`, metadata-matching MD5 `bdf7bfc510742699b8289b9a88e8e25d`. Native attachment `ZRWIN6MM` under parent `LTYWLNHD` was uploaded and stored bytes verified through the authorized native API. The archive inventory has **173 entries / 159 files**; most interface dependencies were not body-read.

Seventeen selected files were hashed and boundedly inspected. Complete reads cover the root/environment READMEs, all 6,943 bytes of `data/analysis.R`, all **45 rows / 34 columns** of `data/dataset.csv`, both example and all three task Java files, the three-page translated task sheets and two single-page result plots. All five PDF pages were extracted, rendered and visually inspected. Only metric configuration lines of five HTML files were read; whole markup, vendor JavaScript and styles were not reviewed. The cached per-file manifest preserves individual identities outside public Git.

Selected file hashes: CSV `0e5176d124096149b0a687e71ee72960f25d19f6de6701faa5465586af959892`; R analysis `d08a6d97bfd8c9ed13d4a163a2cd2a217fa6810360dbbdb9b335a5fc42f3fc6e`; translated task sheets `51b0410c074355ff5f0e21189541f8331120afa676a7a6835b4b166bdf36e7e6`.

## Data transformation and own checks

The R script applies `na.omit` to the full dataframe before all three research questions. All 45 participants have complete ratings, task timings and scored answer counts. Data row 8 lacks the affect-balance components; row 42 lacks fifteen personality/subscale fields. Both are display-4 participants. Those row numbers denote file order, not personal identities. Global deletion changes the task-complete 22/23 groups into the reported 20/23 groups.

The script sums ratings, times and code/documentation correctness across the three tasks, computes TAU using the longest retained total time, then runs Welch's test for ratings and a rank test for TAU. It computes Cohen's d and exploratory group/pooled Spearman correlations. We read this text without running it, installing its packages or launching the study environment.

Own standard-library arithmetic over the released values yields:

| Quantity | Display 4, twenty retained | Display 8, twenty-three retained |
| --- | --- | --- |
| Rating sum, mean / SD | 15.4000 / 4.1726 | 20.8261 / 4.2282 |
| Total seconds, mean | 3,007.85 | 2,943.39 |
| Correct answers out of thirty, mean | 25.7500 | 25.5217 |
| TAU, mean / SD | .370353 / .171864 | .371230 / .115120 |

The rating difference is −5.4261, pooled-standard-deviation d = −1.29115, Welch t = −4.22701 and degrees of freedom 40.31751. TAU difference is −.0008765, d = −.00608, and the rank statistic is 256. These reproduce the paper's main point statistics from the dataset. We did **not** rerun the author R script or independently reproduce its p-values/confidence intervals.

As a descriptive sensitivity check, retaining all 45 task-complete rows gives display-4 mean rating 14.9091 versus the unchanged display-8 mean 20.8261, difference −5.9170 and d = −1.3760. TAU means are .359472 versus .371230, d = −.08167. The positive judgment-effect direction remains. These are not a newly executed experiment, an inferential complete-case correction or evidence of TAU equivalence; the original allocation uncertainty remains.

Equal Cognitive Complexity does not equate the three tasks' human difficulty. Retained mean seconds for tasks 1/2/3 are **411/1,623/974** in the display-4 arm and **475/1,550/918** in the display-8 arm. Mean difficulty ratings are **3.25/7.45/4.70** versus **5.35/9.00/6.48**. This does not undermine the same-task between-arm contrast; it limits the rationale for treating equal metric scores as calibrated task difficulty.

## Material correspondence and remaining gaps

The Java files contain deliberate implementation/documentation discrepancies that define the task. These are not defects in the study merely because they disagree. No Java was run and individual answer scoring was not independently verified: the release has aggregate correct-count columns, not each participant's answer text and a complete scoring audit.

The selected HTML lines show introductory values 1 and 9 and value **4** on all three actual task pages. The README describes the alternative value-8 condition; a separately preserved value-8 deployment and assignment log are absent from the inspected inventory. This does not imply the reported harder condition was never administered. The English task sheets are translations, with original German forms outside the bounded release.

Missing slot identifiers prevent reconstruction of the assignment unit, schedule balance or within-slot dependence. Full raw questionnaire items, withheld demographic details and individual answer content likewise prevent stronger checks. The package makes the reported aggregation and positive rating result inspectable; it does not validate the entire experimental process or establish effects on actual maintenance. Copyrighted bodies, raw dataset and extraction output remain outside public Git.
