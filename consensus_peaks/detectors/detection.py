import neurokit2 as nk

from biosppy.signals.ecg import christov_segmenter, engzee_segmenter, gamboa_segmenter, \
    hamilton_segmenter, ssf_segmenter


biosppy_detect_method_fn_dict = \
    {
        # 'christov_segmenter': christov_segmenter,
        'engzee_segmenter': engzee_segmenter,
        # 'gamboa_segmenter': gamboa_segmenter,
        'hamilton_segmenter': hamilton_segmenter,
        # 'ssf_segmenter': ssf_segmenter
    }

neurokit_detect_method_str_list = \
    ["neurokit",
     "pantompkins",
     # "gamboa2008",
     # "ssf",
     "hamilton",
     "elgendi",
     "kalidas2017",
     # "martinez2003",
     ]


def biosppy_detect(signal, freq, method=None, **kwargs):
    rpeaks, = biosppy_detect_method_fn_dict[method](signal=signal, sampling_rate=freq)
    return rpeaks


def neurokit_detect(signal, freq, correct_artifacts=False, method=None, **kwargs):
    if not method:
        method = "neurokit"

    signals, info = nk.ecg_peaks(signal, sampling_rate=freq, correct_artifacts=correct_artifacts,
                                 method=method)
    return info["ECG_R_Peaks"]


original_peak_detection_fn_dict = {'biosppy': biosppy_detect,
                                   'neurokit': neurokit_detect,
                                   }
