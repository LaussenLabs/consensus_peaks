from consensus_peaks.consensus_signal import get_consensus_signal
from consensus_peaks.constants import CONSENSUS_THRESHOLD
from consensus_peaks.individual_rpeaks import get_individual_rpeaks


def consensus_detect(signal, freq_hz, correction_tolerance=None, consensus_threshold=None, inversion=None):
    inversion = False if inversion is None else inversion
    rpeaks_results = get_individual_rpeaks(signal, freq_hz, correction_tolerance=correction_tolerance)
    consensus_data = get_consensus_signal(rpeaks_results)
    consensus_peaks = get_consensus_peaks(consensus_data, consensus_threshold=consensus_threshold)

    return consensus_peaks[inversion][0]


def get_consensus_peaks(consensus_data, consensus_threshold=None):
    consensus_threshold = CONSENSUS_THRESHOLD if consensus_threshold is None else consensus_threshold
    consensus_time_dict, consensus_value_dict = consensus_data

    consensus_peak_result = {}

    for is_inversion in [False, True]:
        threshold_indices = consensus_value_dict[is_inversion] > consensus_threshold
        consensus_peak_result[is_inversion] = \
            [consensus_time_dict[is_inversion][threshold_indices],
             consensus_value_dict[is_inversion][threshold_indices]]

    return consensus_peak_result
