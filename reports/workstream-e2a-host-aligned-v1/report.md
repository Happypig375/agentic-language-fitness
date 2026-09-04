# Workstream E2a exact-command, host-aligned model-free baseline

Definition: `8e1f417f2355c169102b68495dc083a0c61e0ea3e180914568be7603651448df`  
Inventory: `794591e97d150bdc13d7a9079cee72cbd92f3057a639f71addc71c3f5fad4de3`  
Runner: `901260d7473648f67ee6dd9e469a922023866e2c`  
Samples: 1020 across five paired rounds.

No candidate, Codex process, authentication cache, model endpoint, or paid request was used.
The accepted offline E2 result remains a separate ecology and is not pooled with E2a.

## Paired command timing

| Task | Form | Operation | Audit | C# mean s | F# mean s | F#−C# mean s | F#/C# geometric mean |
|---|---|---|---|---:|---:|---:|---:|
| 001-priority | form-0e61b927152ad4aa | restore | audit_off | 1.357124 | 2.022863 | 0.665739 | 1.491797 |
| 001-priority | form-0e61b927152ad4aa | restore | audit_on | 1.394903 | 7.809989 | 6.415086 | 5.598517 |
| 001-priority | form-3318ac702e2a2303 | run | audit_on | 0.883468 | 0.895253 | 0.011785 | 1.015288 |
| 001-priority | form-4173ceefd9ab3d20 | run | audit_on | 0.921025 | 0.894446 | -0.026579 | 0.972376 |
| 001-priority | form-4322f88a13c7bc79 | build | audit_on | 1.143152 | 3.775125 | 2.631973 | 3.302126 |
| 001-priority | form-4dbeb44293358931 | run | audit_on | 0.902124 | 0.857719 | -0.044405 | 0.946811 |
| 001-priority | form-76b207f2e5ea05d5 | run | audit_on | 0.895685 | 0.914305 | 0.018620 | 1.020781 |
| 001-priority | form-95c252f778b70638 | build | audit_off | 1.917586 | 5.241566 | 3.323980 | 2.730778 |
| 001-priority | form-95c252f778b70638 | build | audit_on | 1.905704 | 11.336434 | 9.430730 | 5.948980 |
| 001-priority | form-cc6f7230ce3280a8 | run | audit_on | 0.940022 | 0.893332 | -0.046691 | 0.951561 |
| 001-priority | form-f135b0b833548d26 | build | audit_off | 1.914367 | 5.181126 | 3.266759 | 2.706527 |
| 001-priority | form-f135b0b833548d26 | build | audit_on | 1.901487 | 11.406452 | 9.504966 | 6.000545 |
| 002-overdue | form-0e61b927152ad4aa | restore | audit_off | 1.364823 | 2.280831 | 0.916008 | 1.622996 |
| 002-overdue | form-0e61b927152ad4aa | restore | audit_on | 1.348228 | 8.073004 | 6.724776 | 5.969845 |
| 002-overdue | form-4173ceefd9ab3d20 | run | audit_on | 0.852810 | 0.892281 | 0.039470 | 1.050377 |
| 002-overdue | form-4322f88a13c7bc79 | build | audit_on | 1.168027 | 3.806879 | 2.638852 | 3.257727 |
| 002-overdue | form-4dbeb44293358931 | run | audit_on | 0.897766 | 0.890519 | -0.007247 | 0.990339 |
| 002-overdue | form-76b207f2e5ea05d5 | run | audit_on | 0.925529 | 0.925033 | -0.000496 | 1.001501 |
| 002-overdue | form-95c252f778b70638 | build | audit_off | 1.923776 | 5.209907 | 3.286132 | 2.707836 |
| 002-overdue | form-95c252f778b70638 | build | audit_on | 1.851404 | 11.450708 | 9.599304 | 6.198951 |
| 002-overdue | form-cc6f7230ce3280a8 | run | audit_on | 0.906875 | 0.874820 | -0.032056 | 0.960137 |
| 002-overdue | form-f135b0b833548d26 | build | audit_off | 1.887253 | 5.205424 | 3.318171 | 2.762189 |
| 002-overdue | form-f135b0b833548d26 | build | audit_on | 1.849007 | 11.189381 | 9.340374 | 6.062448 |
| 003-at-risk-window | form-0e61b927152ad4aa | restore | audit_off | 1.405905 | 1.983414 | 0.577509 | 1.410700 |
| 003-at-risk-window | form-0e61b927152ad4aa | restore | audit_on | 1.384385 | 7.634090 | 6.249705 | 5.515511 |
| 003-at-risk-window | form-3318ac702e2a2303 | run | audit_on | 0.930299 | 0.919594 | -0.010704 | 0.988665 |
| 003-at-risk-window | form-4173ceefd9ab3d20 | run | audit_on | 0.903515 | 0.884098 | -0.019416 | 0.977941 |
| 003-at-risk-window | form-41de0218a97feb51 | run | audit_on | 0.894148 | 0.904394 | 0.010246 | 1.012311 |
| 003-at-risk-window | form-4322f88a13c7bc79 | build | audit_on | 1.179747 | 3.902576 | 2.722829 | 3.309342 |
| 003-at-risk-window | form-4dbeb44293358931 | run | audit_on | 0.881558 | 0.881099 | -0.000459 | 0.997540 |
| 003-at-risk-window | form-62fccf232488c40f | build | audit_on | 1.164673 | 3.825960 | 2.661286 | 3.286533 |
| 003-at-risk-window | form-76b207f2e5ea05d5 | run | audit_on | 0.896649 | 0.924132 | 0.027483 | 1.031757 |
| 003-at-risk-window | form-8dbc61371c91197f | run | audit_on | 0.900020 | 0.887074 | -0.012946 | 0.988488 |
| 003-at-risk-window | form-b5ec78b85ff7a1da | run | audit_on | 1.725765 | 4.424889 | 2.699125 | 2.564215 |
| 003-at-risk-window | form-cc6f7230ce3280a8 | run | audit_on | 0.893432 | 0.895622 | 0.002190 | 1.002429 |
| 003-at-risk-window | form-f135b0b833548d26 | build | audit_off | 1.933739 | 5.545802 | 3.612063 | 2.852904 |
| 003-at-risk-window | form-f135b0b833548d26 | build | audit_on | 1.930731 | 11.388450 | 9.457719 | 5.898489 |
| 004-vip-ready | form-1291d1adebaf93d1 | restore | audit_off | 1.395724 | 2.019275 | 0.623551 | 1.446377 |
| 004-vip-ready | form-1291d1adebaf93d1 | restore | audit_on | 1.395549 | 7.865147 | 6.469598 | 5.634166 |
| 004-vip-ready | form-3318ac702e2a2303 | run | audit_on | 0.916831 | 0.917149 | 0.000319 | 1.000265 |
| 004-vip-ready | form-4173ceefd9ab3d20 | run | audit_on | 0.909592 | 0.897583 | -0.012009 | 0.986794 |
| 004-vip-ready | form-4322f88a13c7bc79 | build | audit_on | 1.161115 | 3.857724 | 2.696609 | 3.322470 |
| 004-vip-ready | form-4dbeb44293358931 | run | audit_on | 0.925685 | 0.922116 | -0.003569 | 0.996364 |
| 004-vip-ready | form-76b207f2e5ea05d5 | run | audit_on | 0.917745 | 0.919248 | 0.001503 | 1.001698 |
| 004-vip-ready | form-8dbc61371c91197f | run | audit_on | 0.922524 | 0.917387 | -0.005137 | 0.994732 |
| 004-vip-ready | form-cc6f7230ce3280a8 | run | audit_on | 0.840571 | 0.923562 | 0.082991 | 1.104065 |
| 004-vip-ready | form-cd02eb97c5cc435a | run | audit_on | 1.679527 | 4.448034 | 2.768507 | 2.653416 |
| 004-vip-ready | form-f135b0b833548d26 | build | audit_off | 1.939981 | 5.507084 | 3.567103 | 2.834029 |
| 004-vip-ready | form-f135b0b833548d26 | build | audit_on | 1.926621 | 12.513419 | 10.586798 | 6.462061 |
| 005-null-order-robustness | form-3318ac702e2a2303 | run | audit_on | 0.914194 | 0.904345 | -0.009849 | 0.989537 |
| 005-null-order-robustness | form-4173ceefd9ab3d20 | run | audit_on | 0.832468 | 0.892516 | 0.060048 | 1.073901 |
| 005-null-order-robustness | form-4322f88a13c7bc79 | build | audit_on | 1.099049 | 3.800655 | 2.701607 | 3.463643 |
| 005-null-order-robustness | form-4dbeb44293358931 | run | audit_on | 0.875003 | 0.883248 | 0.008245 | 1.010977 |
| 005-null-order-robustness | form-62fccf232488c40f | build | audit_on | 1.173934 | 3.794839 | 2.620905 | 3.228456 |
| 005-null-order-robustness | form-6311f3089a3fe56f | run | audit_off | 2.518277 | 6.371033 | 3.852756 | 2.524475 |
| 005-null-order-robustness | form-6311f3089a3fe56f | run | audit_on | 2.513968 | 12.251910 | 9.737942 | 4.874732 |
| 005-null-order-robustness | form-76b207f2e5ea05d5 | run | audit_on | 0.906896 | 0.913151 | 0.006254 | 1.007604 |
| 005-null-order-robustness | form-95c252f778b70638 | build | audit_off | 1.933924 | 5.718232 | 3.784308 | 2.947955 |
| 005-null-order-robustness | form-95c252f778b70638 | build | audit_on | 1.957519 | 11.571405 | 9.613886 | 5.912573 |
| 005-null-order-robustness | form-cc6f7230ce3280a8 | run | audit_on | 0.890183 | 0.887076 | -0.003107 | 0.996848 |
| 005-null-order-robustness | form-f135b0b833548d26 | build | audit_off | 1.856239 | 5.171618 | 3.315379 | 2.783829 |
| 005-null-order-robustness | form-f135b0b833548d26 | build | audit_on | 1.821953 | 11.359049 | 9.537095 | 6.264247 |
| 005-null-order-robustness | form-fb5776eeb54d0d0f | direct | audit_on | 0.127564 | 0.131226 | 0.003661 | 1.028927 |
| 006-transition-validation | form-0e61b927152ad4aa | restore | audit_off | 1.380873 | 2.009731 | 0.628857 | 1.455305 |
| 006-transition-validation | form-0e61b927152ad4aa | restore | audit_on | 1.368559 | 7.726038 | 6.357479 | 5.645141 |
| 006-transition-validation | form-4173ceefd9ab3d20 | run | audit_on | 0.882104 | 0.886839 | 0.004735 | 1.005245 |
| 006-transition-validation | form-4322f88a13c7bc79 | build | audit_on | 1.171162 | 3.916000 | 2.744838 | 3.342878 |
| 006-transition-validation | form-4dbeb44293358931 | run | audit_on | 0.942301 | 0.933569 | -0.008732 | 0.991978 |
| 006-transition-validation | form-4e6ce4fa80260684 | test | audit_on | 0.654923 | 0.638613 | -0.016310 | 0.974590 |
| 006-transition-validation | form-76b207f2e5ea05d5 | run | audit_on | 0.933107 | 0.910221 | -0.022885 | 0.975651 |
| 006-transition-validation | form-95c252f778b70638 | build | audit_off | 1.875609 | 5.500866 | 3.625258 | 2.929014 |
| 006-transition-validation | form-95c252f778b70638 | build | audit_on | 1.905677 | 11.999350 | 10.093673 | 6.286073 |
| 006-transition-validation | form-cc6f7230ce3280a8 | run | audit_on | 0.878424 | 0.935993 | 0.057570 | 1.067606 |
| 006-transition-validation | form-f135b0b833548d26 | build | audit_off | 1.927705 | 5.492244 | 3.564539 | 2.841882 |
| 006-transition-validation | form-f135b0b833548d26 | build | audit_on | 1.923016 | 11.615236 | 9.692221 | 6.038674 |
| 007-query-engine-refactor | form-0e61b927152ad4aa | restore | audit_off | 1.393939 | 2.137676 | 0.743736 | 1.530110 |
| 007-query-engine-refactor | form-0e61b927152ad4aa | restore | audit_on | 1.397646 | 7.879177 | 6.481532 | 5.637228 |
| 007-query-engine-refactor | form-3318ac702e2a2303 | run | audit_on | 0.957903 | 0.926615 | -0.031288 | 0.968992 |
| 007-query-engine-refactor | form-3da1eea2e6fdc2ce | build | audit_on | 1.184439 | 3.902494 | 2.718056 | 3.294797 |
| 007-query-engine-refactor | form-4173ceefd9ab3d20 | run | audit_on | 0.851422 | 0.858402 | 0.006979 | 1.011944 |
| 007-query-engine-refactor | form-4322f88a13c7bc79 | build | audit_on | 1.596389 | 3.849960 | 2.253571 | 2.702632 |
| 007-query-engine-refactor | form-76b207f2e5ea05d5 | run | audit_on | 0.899720 | 0.923356 | 0.023636 | 1.028174 |
| 007-query-engine-refactor | form-829bfa98a73e6646 | run | audit_on | 1.692472 | 4.444898 | 2.752426 | 2.634382 |
| 007-query-engine-refactor | form-85c96331412e9f8c | restore | audit_off | 1.372654 | 1.979407 | 0.606754 | 1.441143 |
| 007-query-engine-refactor | form-85c96331412e9f8c | restore | audit_on | 1.349545 | 7.648341 | 6.298795 | 5.675016 |
| 007-query-engine-refactor | form-99b4e9461d620e05 | build | audit_off | 1.930644 | 5.379968 | 3.449324 | 2.787076 |
| 007-query-engine-refactor | form-99b4e9461d620e05 | build | audit_on | 1.881525 | 11.662761 | 9.781236 | 6.202899 |
| 007-query-engine-refactor | form-cc6f7230ce3280a8 | run | audit_on | 0.934521 | 0.926609 | -0.007912 | 0.991730 |
| 007-query-engine-refactor | form-f135b0b833548d26 | build | audit_off | 1.902832 | 5.604861 | 3.702029 | 2.942658 |
| 007-query-engine-refactor | form-f135b0b833548d26 | build | audit_on | 1.955395 | 11.749975 | 9.794580 | 6.007516 |
| 008-summary-api | form-0e61b927152ad4aa | restore | audit_off | 1.391155 | 2.172160 | 0.781005 | 1.552411 |
| 008-summary-api | form-0e61b927152ad4aa | restore | audit_on | 1.377485 | 7.770369 | 6.392883 | 5.645102 |
| 008-summary-api | form-3318ac702e2a2303 | run | audit_on | 0.887569 | 0.899649 | 0.012080 | 1.018833 |
| 008-summary-api | form-4173ceefd9ab3d20 | run | audit_on | 0.928504 | 0.945111 | 0.016607 | 1.019902 |
| 008-summary-api | form-4322f88a13c7bc79 | build | audit_on | 1.171905 | 3.973454 | 2.801548 | 3.390782 |
| 008-summary-api | form-4dbeb44293358931 | run | audit_on | 0.917562 | 0.915051 | -0.002511 | 1.002536 |
| 008-summary-api | form-4e6ce4fa80260684 | test | audit_on | 0.639693 | 0.657256 | 0.017563 | 1.027604 |
| 008-summary-api | form-76b207f2e5ea05d5 | run | audit_on | 0.949050 | 0.925149 | -0.023902 | 0.975700 |
| 008-summary-api | form-a73adc0f545210e8 | test | audit_on | 0.696263 | 0.662065 | -0.034198 | 0.954773 |
| 008-summary-api | form-cc6f7230ce3280a8 | run | audit_on | 0.944082 | 0.910458 | -0.033624 | 0.964136 |
| 008-summary-api | form-f135b0b833548d26 | build | audit_off | 1.929959 | 5.837079 | 3.907120 | 3.018073 |
| 008-summary-api | form-f135b0b833548d26 | build | audit_on | 1.957871 | 11.920351 | 9.962480 | 6.086170 |

## Audit-on versus audit-off control

| Task | Form | Language | Audit-on mean s | Audit-off mean s | On−off mean s | On/off geometric mean | NU1900 on/off |
|---|---|---|---:|---:|---:|---:|---:|
| 001-priority | form-0e61b927152ad4aa | csharp | 1.394903 | 1.357124 | 0.037779 | 1.028836 | 0/0 |
| 001-priority | form-0e61b927152ad4aa | fsharp | 7.809989 | 2.022863 | 5.787126 | 3.861084 | 5/0 |
| 001-priority | form-95c252f778b70638 | csharp | 1.905704 | 1.917586 | -0.011882 | 0.993751 | 0/0 |
| 001-priority | form-95c252f778b70638 | fsharp | 11.336434 | 5.241566 | 6.094868 | 2.164878 | 20/0 |
| 001-priority | form-f135b0b833548d26 | csharp | 1.901487 | 1.914367 | -0.012881 | 0.993080 | 0/0 |
| 001-priority | form-f135b0b833548d26 | fsharp | 11.406452 | 5.181126 | 6.225326 | 2.201722 | 20/0 |
| 002-overdue | form-0e61b927152ad4aa | csharp | 1.348228 | 1.364823 | -0.016594 | 0.987739 | 0/0 |
| 002-overdue | form-0e61b927152ad4aa | fsharp | 8.073004 | 2.280831 | 5.792174 | 3.633188 | 5/0 |
| 002-overdue | form-95c252f778b70638 | csharp | 1.851404 | 1.923776 | -0.072371 | 0.960271 | 0/0 |
| 002-overdue | form-95c252f778b70638 | fsharp | 11.450708 | 5.209907 | 6.240801 | 2.198313 | 20/0 |
| 002-overdue | form-f135b0b833548d26 | csharp | 1.849007 | 1.887253 | -0.038246 | 0.979185 | 0/0 |
| 002-overdue | form-f135b0b833548d26 | fsharp | 11.189381 | 5.205424 | 5.983957 | 2.149113 | 20/0 |
| 003-at-risk-window | form-0e61b927152ad4aa | csharp | 1.384385 | 1.405905 | -0.021520 | 0.984590 | 0/0 |
| 003-at-risk-window | form-0e61b927152ad4aa | fsharp | 7.634090 | 1.983414 | 5.650676 | 3.849517 | 5/0 |
| 003-at-risk-window | form-f135b0b833548d26 | csharp | 1.930731 | 1.933739 | -0.003007 | 0.998259 | 0/0 |
| 003-at-risk-window | form-f135b0b833548d26 | fsharp | 11.388450 | 5.545802 | 5.842648 | 2.063938 | 20/0 |
| 004-vip-ready | form-1291d1adebaf93d1 | csharp | 1.395549 | 1.395724 | -0.000175 | 0.999783 | 0/0 |
| 004-vip-ready | form-1291d1adebaf93d1 | fsharp | 7.865147 | 2.019275 | 5.845872 | 3.894519 | 5/0 |
| 004-vip-ready | form-f135b0b833548d26 | csharp | 1.926621 | 1.939981 | -0.013360 | 0.993142 | 0/0 |
| 004-vip-ready | form-f135b0b833548d26 | fsharp | 12.513419 | 5.507084 | 7.006335 | 2.264531 | 20/0 |
| 005-null-order-robustness | form-6311f3089a3fe56f | csharp | 2.513968 | 2.518277 | -0.004309 | 0.998391 | 0/0 |
| 005-null-order-robustness | form-6311f3089a3fe56f | fsharp | 12.251910 | 6.371033 | 5.880878 | 1.927881 | 10/0 |
| 005-null-order-robustness | form-95c252f778b70638 | csharp | 1.957519 | 1.933924 | 0.023595 | 1.012003 | 0/0 |
| 005-null-order-robustness | form-95c252f778b70638 | fsharp | 11.571405 | 5.718232 | 5.853173 | 2.029727 | 20/0 |
| 005-null-order-robustness | form-f135b0b833548d26 | csharp | 1.821953 | 1.856239 | -0.034286 | 0.978398 | 0/0 |
| 005-null-order-robustness | form-f135b0b833548d26 | fsharp | 11.359049 | 5.171618 | 6.187430 | 2.201617 | 20/0 |
| 006-transition-validation | form-0e61b927152ad4aa | csharp | 1.368559 | 1.380873 | -0.012314 | 0.991212 | 0/0 |
| 006-transition-validation | form-0e61b927152ad4aa | fsharp | 7.726038 | 2.009731 | 5.716307 | 3.844919 | 5/0 |
| 006-transition-validation | form-95c252f778b70638 | csharp | 1.905677 | 1.875609 | 0.030069 | 1.017418 | 0/0 |
| 006-transition-validation | form-95c252f778b70638 | fsharp | 11.999350 | 5.500866 | 6.498484 | 2.183521 | 20/0 |
| 006-transition-validation | form-f135b0b833548d26 | csharp | 1.923016 | 1.927705 | -0.004689 | 0.997614 | 0/0 |
| 006-transition-validation | form-f135b0b833548d26 | fsharp | 11.615236 | 5.492244 | 6.122992 | 2.119815 | 20/0 |
| 007-query-engine-refactor | form-0e61b927152ad4aa | csharp | 1.397646 | 1.393939 | 0.003706 | 1.002780 | 0/0 |
| 007-query-engine-refactor | form-0e61b927152ad4aa | fsharp | 7.879177 | 2.137676 | 5.741502 | 3.694442 | 5/0 |
| 007-query-engine-refactor | form-85c96331412e9f8c | csharp | 1.349545 | 1.372654 | -0.023108 | 0.982014 | 0/0 |
| 007-query-engine-refactor | form-85c96331412e9f8c | fsharp | 7.648341 | 1.979407 | 5.668933 | 3.867031 | 5/0 |
| 007-query-engine-refactor | form-99b4e9461d620e05 | csharp | 1.881525 | 1.930644 | -0.049119 | 0.973684 | 0/0 |
| 007-query-engine-refactor | form-99b4e9461d620e05 | fsharp | 11.662761 | 5.379968 | 6.282793 | 2.167025 | 20/0 |
| 007-query-engine-refactor | form-f135b0b833548d26 | csharp | 1.955395 | 1.902832 | 0.052562 | 1.028071 | 0/0 |
| 007-query-engine-refactor | form-f135b0b833548d26 | fsharp | 11.749975 | 5.604861 | 6.145114 | 2.098834 | 20/0 |
| 008-summary-api | form-0e61b927152ad4aa | csharp | 1.377485 | 1.391155 | -0.013670 | 0.989870 | 0/0 |
| 008-summary-api | form-0e61b927152ad4aa | fsharp | 7.770369 | 2.172160 | 5.598209 | 3.599511 | 5/0 |
| 008-summary-api | form-f135b0b833548d26 | csharp | 1.957871 | 1.929959 | 0.027912 | 1.014468 | 0/0 |
| 008-summary-api | form-f135b0b833548d26 | fsharp | 11.920351 | 5.837079 | 6.083272 | 2.045751 | 20/0 |

## Mechanical tool-exposure envelope

| Configuration | Language | Observed invocations | Mechanical seconds | Observed E1 agent seconds |
|---|---|---:|---:|---:|
| H | csharp | 16 | 20.574652 | 502.360195 |
| H | fsharp | 29 | 133.657722 | 633.568369 |
| L | csharp | 41 | 48.096664 | 955.773346 |
| L | fsharp | 72 | 334.819610 | 1349.070607 |
| M | csharp | 38 | 48.933156 | 1150.283944 |
| M | fsharp | 62 | 258.745164 | 1623.435852 |

This is a mechanical invocation-count × matched-duration timing counterfactual. It is not subtracted from agent cost, is not a mediation estimate, and does not identify behavioral feedback effects.

## NU1900 and output-volume boundary

The authenticated v3 streams contained 197 F# NU1900 lines and zero C# NU1900 lines. They are repeated emitted diagnostic lines, not independent defects. Absolute stdout, stderr, total output bytes, diagnostic occurrences, and descriptive uncertainty are retained in the JSON report.

## Remaining mismatches

- `candidate-process` — deliberately-absent: model-free E2a measures tool commands only; no Codex or model request is made
- `authentication-home` — deliberately-absent: fresh HOME reproduces cache freshness but contains no Codex authentication material
- `workspace-state` — standardized-successor: each task/form uses its matched canonical gold successor, not an intermediate candidate edit
- `within-task-cache-history` — unavailable: each sample has a fresh HOME/cache; the exact cache history at each E1 command is not retained
- `host-load` — observed-not-controlled: per-sample load is retained, but machine-cold state and unrelated host work are not controlled
- `shell-plumbing` — semantic-replay: fixed argv uses shell=False; pipe versus file-backed stdin semantics are retained without incidental shell text

Any difference outside the mechanical envelope remains inseparable from model interaction, repair behavior, unavailable within-task cache history, and other trajectory effects.
The envelope is not subtracted from agent cost and is not a mediation or causal decomposition.
