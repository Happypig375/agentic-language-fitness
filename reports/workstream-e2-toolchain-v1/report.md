# Workstream E2 model-free baseline

Definition: `09d5669fd554e611b4df505454a40f06a0e9b2a23c4a16a28c9cc94d640067f7`
Runner: `b953dac54c03087ae46689bc62a3221c3c9d3f97`
Container: `sha256:a07394d59b0182a95c95cb82ad044fd777491cdf924f066f678238e3a09c4022`
Samples: 90 (five paired rounds; fresh and immediate repeat)

## Operation timing summaries

| Language | Stage | Regime | Operation | n | Mean seconds | Median seconds |
|---|---:|---|---|---:|---:|---:|
| csharp | 0 | fresh-workspace | build | 5 | 0.681606 | 0.668208 |
| csharp | 0 | fresh-workspace | restore | 5 | 0.765793 | 0.760189 |
| csharp | 0 | fresh-workspace | run | 5 | 0.525986 | 0.529081 |
| csharp | 0 | repeat-workspace | build | 5 | 0.671267 | 0.676482 |
| csharp | 0 | repeat-workspace | run | 5 | 0.559582 | 0.540748 |
| csharp | 1 | fresh-workspace | build | 5 | 0.663011 | 0.658477 |
| csharp | 1 | fresh-workspace | restore | 5 | 0.760362 | 0.759354 |
| csharp | 1 | fresh-workspace | run | 5 | 0.532858 | 0.533391 |
| csharp | 1 | repeat-workspace | build | 5 | 0.665381 | 0.666226 |
| csharp | 1 | repeat-workspace | run | 5 | 0.528949 | 0.528512 |
| csharp | 2 | fresh-workspace | build | 5 | 0.924141 | 0.682784 |
| csharp | 2 | fresh-workspace | restore | 5 | 0.760611 | 0.760165 |
| csharp | 2 | fresh-workspace | run | 5 | 0.538430 | 0.539370 |
| csharp | 2 | repeat-workspace | build | 5 | 0.675244 | 0.669964 |
| csharp | 2 | repeat-workspace | run | 5 | 0.543385 | 0.540522 |
| csharp | 3 | fresh-workspace | build | 5 | 0.675770 | 0.668014 |
| csharp | 3 | fresh-workspace | restore | 5 | 0.761847 | 0.759666 |
| csharp | 3 | fresh-workspace | run | 5 | 0.533050 | 0.537606 |
| csharp | 3 | repeat-workspace | build | 5 | 0.678602 | 0.681926 |
| csharp | 3 | repeat-workspace | run | 5 | 0.538184 | 0.541292 |
| csharp | 4 | fresh-workspace | build | 5 | 0.673289 | 0.677399 |
| csharp | 4 | fresh-workspace | restore | 5 | 0.760242 | 0.759739 |
| csharp | 4 | fresh-workspace | run | 5 | 0.541373 | 0.543046 |
| csharp | 4 | repeat-workspace | build | 5 | 0.674763 | 0.670422 |
| csharp | 4 | repeat-workspace | run | 5 | 0.539305 | 0.533078 |
| csharp | 5 | fresh-workspace | build | 5 | 0.711616 | 0.679685 |
| csharp | 5 | fresh-workspace | restore | 5 | 0.766984 | 0.770393 |
| csharp | 5 | fresh-workspace | run | 5 | 0.542370 | 0.541698 |
| csharp | 5 | repeat-workspace | build | 5 | 0.677338 | 0.675342 |
| csharp | 5 | repeat-workspace | run | 5 | 0.547073 | 0.547502 |
| csharp | 6 | fresh-workspace | build | 5 | 0.675134 | 0.671896 |
| csharp | 6 | fresh-workspace | restore | 5 | 0.758242 | 0.759218 |
| csharp | 6 | fresh-workspace | run | 5 | 0.545081 | 0.541413 |
| csharp | 6 | repeat-workspace | build | 5 | 0.664535 | 0.669002 |
| csharp | 6 | repeat-workspace | run | 5 | 0.541176 | 0.541198 |
| csharp | 7 | fresh-workspace | build | 5 | 0.669755 | 0.667605 |
| csharp | 7 | fresh-workspace | restore | 5 | 0.770443 | 0.763727 |
| csharp | 7 | fresh-workspace | run | 5 | 0.536798 | 0.536747 |
| csharp | 7 | repeat-workspace | build | 5 | 0.671662 | 0.672445 |
| csharp | 7 | repeat-workspace | run | 5 | 0.553942 | 0.546117 |
| csharp | 8 | fresh-workspace | build | 5 | 0.677213 | 0.673954 |
| csharp | 8 | fresh-workspace | restore | 5 | 0.759892 | 0.761084 |
| csharp | 8 | fresh-workspace | run | 5 | 0.611182 | 0.553190 |
| csharp | 8 | repeat-workspace | build | 5 | 0.688370 | 0.677368 |
| csharp | 8 | repeat-workspace | run | 5 | 0.559841 | 0.565360 |
| fsharp | 0 | fresh-workspace | build | 5 | 2.047742 | 2.032807 |
| fsharp | 0 | fresh-workspace | restore | 5 | 6.459274 | 6.439431 |
| fsharp | 0 | fresh-workspace | run | 5 | 0.523087 | 0.522332 |
| fsharp | 0 | repeat-workspace | build | 5 | 2.023228 | 1.997282 |
| fsharp | 0 | repeat-workspace | run | 5 | 0.530051 | 0.527082 |
| fsharp | 1 | fresh-workspace | build | 5 | 2.047413 | 2.052481 |
| fsharp | 1 | fresh-workspace | restore | 5 | 6.450801 | 6.528094 |
| fsharp | 1 | fresh-workspace | run | 5 | 0.523002 | 0.523299 |
| fsharp | 1 | repeat-workspace | build | 5 | 2.034325 | 2.009543 |
| fsharp | 1 | repeat-workspace | run | 5 | 0.543372 | 0.522481 |
| fsharp | 2 | fresh-workspace | build | 5 | 2.049000 | 2.042902 |
| fsharp | 2 | fresh-workspace | restore | 5 | 6.368409 | 6.347074 |
| fsharp | 2 | fresh-workspace | run | 5 | 0.529124 | 0.527043 |
| fsharp | 2 | repeat-workspace | build | 5 | 2.066817 | 2.077779 |
| fsharp | 2 | repeat-workspace | run | 5 | 0.535960 | 0.532779 |
| fsharp | 3 | fresh-workspace | build | 5 | 2.068212 | 2.065837 |
| fsharp | 3 | fresh-workspace | restore | 5 | 6.451004 | 6.451247 |
| fsharp | 3 | fresh-workspace | run | 5 | 0.531032 | 0.533689 |
| fsharp | 3 | repeat-workspace | build | 5 | 2.078973 | 2.066150 |
| fsharp | 3 | repeat-workspace | run | 5 | 0.536722 | 0.535655 |
| fsharp | 4 | fresh-workspace | build | 5 | 2.112219 | 2.111176 |
| fsharp | 4 | fresh-workspace | restore | 5 | 6.345075 | 6.327002 |
| fsharp | 4 | fresh-workspace | run | 5 | 0.532471 | 0.532213 |
| fsharp | 4 | repeat-workspace | build | 5 | 2.066954 | 2.062003 |
| fsharp | 4 | repeat-workspace | run | 5 | 0.535895 | 0.534453 |
| fsharp | 5 | fresh-workspace | build | 5 | 2.133863 | 2.123237 |
| fsharp | 5 | fresh-workspace | restore | 5 | 6.400755 | 6.407166 |
| fsharp | 5 | fresh-workspace | run | 5 | 0.536779 | 0.532413 |
| fsharp | 5 | repeat-workspace | build | 5 | 2.132302 | 2.122693 |
| fsharp | 5 | repeat-workspace | run | 5 | 0.532445 | 0.529349 |
| fsharp | 6 | fresh-workspace | build | 5 | 2.136339 | 2.112080 |
| fsharp | 6 | fresh-workspace | restore | 5 | 6.356924 | 6.397697 |
| fsharp | 6 | fresh-workspace | run | 5 | 0.564976 | 0.540069 |
| fsharp | 6 | repeat-workspace | build | 5 | 2.160496 | 2.157301 |
| fsharp | 6 | repeat-workspace | run | 5 | 0.533909 | 0.533632 |
| fsharp | 7 | fresh-workspace | build | 5 | 2.160895 | 2.171384 |
| fsharp | 7 | fresh-workspace | restore | 5 | 6.466040 | 6.461873 |
| fsharp | 7 | fresh-workspace | run | 5 | 0.558925 | 0.547518 |
| fsharp | 7 | repeat-workspace | build | 5 | 2.131910 | 2.131821 |
| fsharp | 7 | repeat-workspace | run | 5 | 0.540659 | 0.537871 |
| fsharp | 8 | fresh-workspace | build | 5 | 2.208910 | 2.212880 |
| fsharp | 8 | fresh-workspace | restore | 5 | 6.389569 | 6.443003 |
| fsharp | 8 | fresh-workspace | run | 5 | 0.541201 | 0.537727 |
| fsharp | 8 | repeat-workspace | build | 5 | 2.222741 | 2.219370 |
| fsharp | 8 | repeat-workspace | run | 5 | 0.543897 | 0.540476 |

Internal compiler phases and observed compiler inputs are unavailable; the report records static source/project obligations instead.
The OS page cache was neither cleared nor controlled, so the regimes are named fresh-workspace and repeat-workspace.
