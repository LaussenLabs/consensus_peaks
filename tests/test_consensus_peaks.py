import pytest

from consensus_peaks.consensus_peaks import get_consensus_peaks
from consensus_peaks.consensus_signal import get_consensus_signal
from consensus_peaks.individual_rpeaks import get_individual_rpeaks
from tests.generate_wfdb import get_records


def test_get_consensus_peaks():
    # Set up input data
    records = get_records()
    record = next(records)
    signal = record.p_signal[:, 0]  # Assuming the first channel is the ECG signal
    freq_hz = record.fs
    signal = signal[:10_000]

    # Call get_individual_rpeaks
    rpeaks_results = get_individual_rpeaks(signal, freq_hz)

    # print(rpeaks_results)

    consensus_results = get_consensus_signal(rpeaks_results)

    consensus_peaks = get_consensus_peaks(consensus_results)

    print(consensus_peaks)
