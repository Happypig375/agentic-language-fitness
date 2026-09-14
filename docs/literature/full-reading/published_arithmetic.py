"""Small calculations from cited printed cells; never a paper/experiment rerun.

Run from any directory with Python 3. Outputs original derived values only.
The accompanying notes identify editions, locators and interpretive limits.
"""

import json
from statistics import mean


def compatible_counts(percent, denominator):
    """Integers whose percentages round to a printed one-decimal cell."""
    return [n for n in range(denominator + 1)
            if abs(100 * n / denominator - percent) < 0.05 - 1e-10]


def results():
    # P01 PDF table II, p. 8, and token examples p. 10.
    p01_llm = [27.33, 87.83, 61.16, 20.16, 24.14, 44.21]
    p01_tool = [51.41, 65.11, 62.93, 31.19, 34.84, 39.56]
    # P04 appendix A1 counts; these are not the main shared subset.
    p04_ns = [215, 186, 207, 233, 38, 36, 58, 86,
              313, 280, 397, 395, 17, 17, 42, 40]
    # P06 table 2, p. 7; row order model then configuration.
    p06 = {
        "oracle": [69.1, 68.1, 62.5, 61.8, 61.8, 36.2, 64.8, 62.8, 37.8,
                   64.5, 65.5, 63.5, 64.0, 66.5, 62.5, 42.8, 50.3, 48.4,
                   61.8, 61.5, 61.5],
        "seq": [49.0, 42.4, 35.2, 41.8, 39.8, 21.7, 45.1, 33.9, 23.0,
                40.5, 39.5, 38.0, 43.0, 40.5, 38.5, 29.6, 27.3, 25.0,
                36.5, 39.5, 37.2],
        "memory": [47.4, 49.7, 43.4, 41.8, 37.8, 22.0, 44.1, 35.5, 18.1,
                   39.5, 41.5, 40.0, 37.5, 40.0, 40.0, 28.6, 26.0, 28.0,
                   37.5, 39.8, 37.2],
    }
    return {
        "scope": "Printed-cell arithmetic; no raw-trial reconstruction, p-values or causal verification.",
        "P01_table_II_llm_minus_tool": [round(a-b, 2) for a, b in zip(p01_llm, p01_tool)],
        "P01_hierarchical_token_ratios": [736/x for x in [226, 188, 184]],
        "P02_table_1_partial_modified_LOC": .0345*5000 + .0023*4750,
        "P02_table_1_partial_added_LOC": .0345*5000,
        "P03_trials": 33*2*10,
        "P03_rounded_hidden_test_fraction_delta_pp": (.913-.921)*100,
        "P04_appendix_A1_listed_N_sum": sum(p04_ns),
        "P04_minimax_multilingual_54_and_52_of_86": [100*54/86, 100*52/86],
        "P04_minimax_pro_171_and_150_of_395": [100*171/395, 100*150/395],
        "P04_selected_causal_and_survival_percent": [100*54/262, 100*225/262],
        "P05_best_strict_compatible_n_of_196": compatible_counts(14.8, 196),
        "P05_quality_level_ratios": [.44/.19, .68/.34],
        "P05_quality_slope_ratios": [.0144/.0022, .0264/.0053],
        "P05_cost_start_to_final_ratio": 1.67/.77,
        "P05_potential_main_checkpoints": 15*196,
        "P05_observed_quality_checkpoints": 2869,
        "P05_human_growth_fractions": [256/378, 103/196],
        "P06_chain_tasks": 97*3 + 2*4 + 5,
        "P06_printed_table_2_cell_means": {k: mean(v) for k, v in p06.items()},
        "P06_narrative_relative_accuracy_loss": (58.9-36.5)/58.9,
        "P06_chain_error_fraction": 318/663,
        "P06_selected_cell_64_percent_compatible_n_of_304": compatible_counts(64.0, 304),
        "P06_table_2_cells_incompatible_with_single_304_denominator": {
            k: [x for x in v if not compatible_counts(x, 304)] for k, v in p06.items()
        },
        # P07 table 2 and results, PDF pp. 6-8. Disputed S cells remain disputed.
        "P07_all_micro_multi_success_percent": [100*175/483, 100*123/230, 100*52/253],
        "P07_agent_api_success_percent": [100*104/231, 100*71/252],
        "P07_model_case_cells": 23*21,
        # P08 table 1; each reporting mode has 60 chaffs x 10 runs.
        "P08_success_percent_untyped_min_prox_all": [100*n/600 for n in [201, 250, 287, 317]],
        "P08_all_minus_untyped_pp": 100*(317-201)/600,
        "P08_selected_type_correct_semantic_success_percent": 100*854/872,
        "P08_three_experiment_trials": 60*4*10*3,
        # P09 tables 1, 2, 4 and figure 5; no paired raw-trial test inferred.
        "P09_mask_raw_relative_gain_percent": 100*(274-267)/267,
        "P09_mask_raw_absolute_gain_pp": 100*(274-267)/500,
        "P09_rounded_mask_cost_saving_percent": 100*(1.29-.61)/1.29,
        "P09_rounded_summary_mask_cost_difference_500": (.64-.61)*500,
        "P09_rounded_52_vs_44_turn_increase_percent": 100*(52-44)/44,
        "P09_summary_cost_share_percent": 100*.0439/.64,
        "P09_hybrid_N43_vs_full500_raw_unmatched_pp": 100*28/50-100*267/500,
        # P10 tables 1, 5, 6. Ratio of aggregate means is not mean per-paper recovery.
        "P10_requests_per_paper": 1148/20,
        "P10_committed_recoverable_percent": 100*358/371,
        "P10_Claude_aggregate_MCF_gap_recovery_percent": 100*(3.000-2.718)/(3.031-2.718),
        "P10_faithful_increase_percent": 100*(181-118)/118,
        "P10_severe_failure_reduction_percent": 100*(72-49)/72,
        # P11 figure 9 (v2): 13 displayed configurations, despite prose saying 12.
        "P11_solved_counts_over_110_percent": [100*n/110 for n in [61,32,26,21,20,14,11,10,9,8,4,3,3]],
        "P11_union_percent": 100*79/110,
        # P12 tables 1, 3-5, 7-8. Rounded cells, not estimated model effects.
        "P12_edge_totals": {"all": 70+84+70, "typed": 150+39+16+19},
        "P12_passive_full_minus_active": [.457-.676, .696-.469],
        "P12_oracle_minus_active": [.737-.676, .641-.469],
        "P12_active_minus_replay_table_sign": [.676-.665, .469-.561],
        "P12_scratchpad_minus_no_probe_dependency": [.676-.538, .469-.480],
        "P12_scratchpad_minus_no_probe_invariant": [.739-.570, .516-.273],
        "P12_table_8_prompt_deltas": [.469-.328, .676-.564, .664-.639],
        "P12_budget10_config_random_ratio": .175/.056,
        "P13_validity_fraction": 5/7,
        "P13_Int1_historical_price_estimate": 399*.06 + 66*.12,
        "P13_Ext1_displayed_token_sum_k": 100+17,
    }


if __name__ == "__main__":
    print(json.dumps(results(), indent=2))
