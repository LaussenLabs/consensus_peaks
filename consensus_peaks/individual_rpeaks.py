from consensus_peaks.constants import REG_R_PEAK_METHODS, CORRECTION_TOLERANCE

import numpy as np
import pandas as pd
import neurokit2 as nk
import heartpy as hp
from pathlib import Path
from biosppy.signals import ecg
import time

from consensus_peaks.detectors.cleaning import neurokit_clean_method_str_list
from consensus_peaks.detectors.detection import original_peak_detection_fn_dict, neurokit_detect_method_str_list, \
    biosppy_detect_method_fn_dict


def get_individual_rpeaks(signal, freq_hz, correction_tolerance=None):
    correction_tolerance = CORRECTION_TOLERANCE if correction_tolerance is None else correction_tolerance

    r_peak_methods = REG_R_PEAK_METHODS
    r_peak_method_setting_list = get_method_list(r_peak_methods)
    cleaning_string_list = neurokit_clean_method_str_list
    inversion_list = [False, True]

    result = initialize_individual_rpeak_results(signal, inversion_list,
                                                 r_peak_method_setting_list, cleaning_string_list)

    rolling_window = int(0.3 * freq_hz)

    for is_inverted in inversion_list:
        if is_inverted:
            # Invert Signal
            post_inversion_signal = invert_signal(signal)

            if post_inversion_signal is None:
                continue
        else:
            post_inversion_signal = signal

        # Normalize Signal
        norm_signal = normalize_signal(post_inversion_signal, rolling_window)

        if norm_signal is None:
            continue

        for cleaning_str in cleaning_string_list:
            # Clean the Signal
            cleaned_signal = clean_signal(norm_signal, freq_hz, cleaning_str)

            if cleaned_signal is None:
                continue

            for method_str, setting_str in r_peak_method_setting_list:
                # Detect Peaks
                peak_inds = detect_signal(cleaned_signal, method_str, setting_str, freq_hz)

                if peak_inds is None:
                    continue

                # Correct Peaks
                peak_inds = correct_signal(post_inversion_signal, peak_inds, correction_tolerance, freq_hz)

                if peak_inds is None:
                    continue

                # Record Result
                result[is_inverted][cleaning_str][(method_str, setting_str)] = peak_inds

    return result


def initialize_individual_rpeak_results(signal, inversion_list, r_peak_method_setting_list,
                                        cleaning_list):
    result = {}
    num_measure_vals = len(signal)

    if num_measure_vals < 100:
        raise ValueError("Signal length is less than 100.")

    for is_inverted in inversion_list:
        result[is_inverted] = {}
        for cleaning_string in cleaning_list:
            result[is_inverted][cleaning_string] = {}
            for method_str, setting_str in r_peak_method_setting_list:
                result[is_inverted][cleaning_string][(method_str, setting_str)] = []

    return result


def correct_signal(cleaned_window, peak_inds, correction_tolerance, freq_hz):
    try:
        (peak_inds,) = ecg.correct_rpeaks(
            signal=cleaned_window, rpeaks=peak_inds,
            sampling_rate=freq_hz, tol=correction_tolerance)

    except (ValueError, IndexError) as e:
        print(e)
        peak_inds = None
    return peak_inds


def detect_signal(cleaned_window, method_str, setting_str, freq_hz):
    kwargs = {}
    if setting_str:
        kwargs['method'] = setting_str
    try:
        peak_inds = original_peak_detection_fn_dict[method_str](
            cleaned_window, freq_hz, **kwargs)
    except (ValueError, IndexError) as e:
        print(e)
        peak_inds = None
    return peak_inds


def normalize_signal(value_window, rolling_window):
    try:
        value_window = value_window - pd.Series(value_window).rolling(
            window=rolling_window, min_periods=1, center=True).mean()
        value_window = (value_window - np.mean(value_window)) - np.std(value_window)
    except (ValueError, IndexError) as e:
        print(e)
        value_window = None
    return value_window


def clean_signal(value_window, freq_hz, cleaning_str):
    try:
        v_copy = nk.ecg_clean(value_window, sampling_rate=freq_hz, method=cleaning_str)
    except (ValueError, IndexError) as e:
        print(e)
        v_copy = None
    return v_copy


def invert_signal(value_window):
    try:
        return hp.flip_signal(value_window)
    except (ValueError, IndexError) as e:
        print(e)
        return None


def get_method_list(r_peak_methods):
    r_peak_method_setting_list = []
    for method_str in r_peak_methods:
        if method_str in ['neurokit', 'i_neurokit']:
            for setting_str in neurokit_detect_method_str_list:
                r_peak_method_setting_list.append((method_str, setting_str))
        elif method_str in ['biosppy', 'i_biosppy']:
            for setting_str in biosppy_detect_method_fn_dict.keys():
                r_peak_method_setting_list.append((method_str, setting_str))
        else:
            r_peak_method_setting_list.append((method_str, ""))
    return r_peak_method_setting_list
