import pytest

from consensus_peaks.individual_rpeaks import get_individual_rpeaks
from tests.generate_wfdb import get_records


def test_get_individual_rpeaks():
    # Set up input data
    records = get_records()
    record = next(records)
    signal = record.p_signal[:, 0]  # Assuming the first channel is the ECG signal
    freq_hz = record.fs

    # Call get_individual_rpeaks
    rpeaks_results = get_individual_rpeaks(signal, freq_hz)

    print(rpeaks_results)
