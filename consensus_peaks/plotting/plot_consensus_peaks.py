import matplotlib.pyplot as plt
import numpy as np


def plot_consensus_peaks(signal, consensus_peak_result, freq_hz):
    time = np.arange(0, len(signal)) / freq_hz
    plt.figure(figsize=(20, 5))
    plt.plot(time, signal, label='ECG Signal')

    color_dict = {False: 'green', True: 'red'}

    for is_inverted, (peak_times, _) in consensus_peak_result.items():
        plt.vlines(x=peak_times / freq_hz, ymin=np.min(signal), ymax=np.max(signal), color=color_dict[is_inverted],
                   linestyle='--', linewidth=0.5, label=f'{"Inverted" if is_inverted else "Non-inverted"} Consensus Peaks')

    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend(loc='upper right')
    plt.show()
