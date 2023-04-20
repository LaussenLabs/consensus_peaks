import numpy as np

from consensus_peaks.constants import INVERSION_BOOL_LIST


def get_consensus_signal(rpeak_result):
    # Create a dictionary to store consensus R-peak times for inverted and non-inverted signals
    consensus_time_dict = {is_inversion: [] for is_inversion in INVERSION_BOOL_LIST}

    # Iterate through the R-peak results
    for is_inversion, cleaning_result in rpeak_result.items():
        for method_result in cleaning_result.values():
            for r_peak_list in method_result.values():
                consensus_time_dict[is_inversion].append(r_peak_list)

    # Find the unique R-peak times for inverted and non-inverted signals
    for is_inversion in INVERSION_BOOL_LIST:
        if len(consensus_time_dict[is_inversion]) == 0:
            assert False
        consensus_time_dict[is_inversion] = np.unique(np.concatenate(consensus_time_dict[is_inversion]))

    # Create a dictionary to store the R-peak counts for inverted and non-inverted signals
    consensus_value_dict = \
        {is_inversion: np.zeros(consensus_time_dict[is_inversion].size, dtype=np.uint16)
         for is_inversion in INVERSION_BOOL_LIST}

    # Count the occurrences of each R-peak in the results
    for is_inversion, cleaning_result in rpeak_result.items():
        for method_result in cleaning_result.values():
            for r_peak_list in method_result.values():
                match_indices = consensus_time_dict[is_inversion].searchsorted(r_peak_list)
                consensus_value_dict[is_inversion][match_indices] += 1

    return consensus_time_dict, consensus_value_dict
