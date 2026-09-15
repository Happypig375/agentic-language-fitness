# S24 — Context-aware runtime service selection

**Full target-chapter reading completed 2026-09-16 HKT by the main Codex AI session.** Mauro Caporuscio, Marco De Toma, Henry Muccini and Karthik Vaidhyanathan, *A Machine Learning Approach to Service Discovery for Microservice Architectures*, ECSA 2021, LNCS 12857, 66–82. [DOI](https://doi.org/10.1007/978-3-030-86044-8_5).

## Asset and coverage

| Field | Evidence |
| --- | --- |
| Zotero | Parent `IH9FMDJ2`, user-supplied proceedings PDF `8MX4RAH6`, collection `PKLXQNEE` |
| PDF | Whole volume: 339 pages, 18,513,573 bytes; SHA-256 `10956af8213888fa28793730e518912d2379fde26c0db7593e320fef3a8b8c6b` |
| Reading | **Only target PDF pp. 83–99**, all 17 chapter pages and 24 references; no appendix. The whole volume is not claimed as read |
| Visual checks | Chapter identity p. 83; all five figures pp. 86, 88, 92, 94, 96; Algorithm 1 p. 91; selection/forecast/QoS/RMSE equations and definitions pp. 86–91, 95; no numbered table |
| Artifact | [ML-SD](https://github.com/karthikv1392/ML-SD/tree/4738ccfcdc9703a01fbe6faba7163d64095cbbb2), commit `4738ccfcdc9703a01fbe6faba7163d64095cbbb2`; untruncated file inventory and bounded training, prediction, registry, greedy/Q-learning selection, state and analysis-query inspection |
| Limit | No cloud deployment, model training, SQL data import or benchmark reproduction. Current artifact/publication differences remain unresolved |

## Reconstruction

The decision is **which running instance of a service to invoke for the next request**, after matching the required interface. It is not selection of a starting code package for a future maintenance sequence. The selector uses monitored QoS history and current context, LSTM response-time forecasts, and an updating Q table. Batch retraining and repeated decisions are integral to the treatment.

The prototype is a coin-collection application with five service roles and 25 deployed instances, distributed across two cloud VMs. Ten clients generate time-varying Poisson workloads; instance/time-dependent artificial delays create performance variation. A week of monitored data supplies the forecasting setup. The comparison deploys each of five strategies for 72 hours: static/greedy, linear-regression/greedy, LSTM/greedy, linear-regression/Q-learning, and LSTM/Q-learning. Thus it includes useful component comparisons, not only one bundled treatment against a static baseline.

The reported results include forecasting RMSE 406.73 ms, per-minute accumulated mean service response time, per-request response time and discovery overhead. The preferred LSTM/Q-learning combination reports 1,236.23 ms mean response time and improvements of 20/19/21/16% over the other strategies (p. 79). The reported 10,449 versus 11,762 seconds of accumulated mean response time corresponds to about **11.2% reduction relative to the static baseline**, rather than the printed 12%; it is not total elapsed user time saved. Discovery averages 0.10 seconds and batch training about 125 minutes every 12 hours. Keeping training off the request path does not eliminate its resource cost.

## Method and artifact limits

- **A forecast metric is not selection value.** This paper does measure executed service response times as well as forecast accuracy, so it must not be dismissed as label-only recommendation. The reported effect is nevertheless specific to one synthetic-workload application; requests/time points are not independent applications or maintenance decisions. Matched workload replay, deployment order and independent replicate uncertainty are not sufficiently established in the chapter to transfer the effect.
- **Feedback is part of the policy.** Page 79 describes Q-learning feedback through the next forecast. The released `postAction` instead uses `MonitoringData` response time; the static source therefore does not cleanly reproduce that account. ALF must specify whether advice receives subsequent observations and distinguish a frozen adoption decision from an online controller.
- **Development is not an untouched test.** The method describes retuning when test accuracy is low (p. 73), while the 60-neuron choice was selected experimentally. The stated 7:3 split differs from the reported 8,903/2,206 sample counts, which are approximately 80:20. The temporal and tuning boundaries need reconstruction before interpreting prediction accuracy as independent confirmation.
- **The current code is a different specification in material respects.** `time-series-training.py` scales the full time series before its 70:30 chronological split, uses two LSTM layers of 110/55 units, 50 epochs and one one-minute forecast step; the paper describes one 60-unit hidden layer, 250 epochs and a five-minute horizon. The released Q-learning update is also different from Algorithm 1: it updates all cells matching the previous state using `gamma + reward * max(...)`, and has epsilon exploration. This is a static discrepancy finding, not proof of which program produced the paper's results.
- **Analysis queries are not a complete result pipeline.** The released `analysis.sql` filters `id > 600000` without an explanation there. No result is recomputed from that fragment; it cannot establish that all initial/transient costs were included. Downloaded source is not a reproduced experiment.

## Consequences and next readings

The chapter is established prior art for context-dependent service selection with behavioral QoS evaluation. Its online policy, information and costs differ from ALF's proposed one-time adoption decision. Consequently it does not directly settle the architectural-information question, but it rules out broad firstness claims about selecting services using predicted outcomes.

Retain independent profile units, an explicit feedback policy, component-matched comparisons, separate prediction/decision outcomes and full offline/online cost accounting. Do not import a percentage improvement or adopt its learning algorithm. Its LSTM, Q-learning and earlier service-assembly references remain conditional because ALF does not use those mechanisms. **S29 (ExTrA)** is the closer architectural explanation/value branch, discovered in the same proceedings' contents and pursued through its journal extension. The 2021 ExTrA precursor is available in this volume but not silently counted as read; consult it if the extension leaves an important edition-specific dependency.

**Uniqueness remains unconfirmed, ALF value remains a testable adoption benefit, and no runtime-selection result validates ALF's proposed methodology.**
