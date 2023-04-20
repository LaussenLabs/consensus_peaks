import random
import numpy as np
import matplotlib.pyplot as plt


def plot_individual_rpeaks(signal, rpeaks_results, freq_hz):
    time = np.arange(0, len(signal)) / freq_hz
    plt.figure(figsize=(20, 5))
    plt.plot(time, signal, label='ECG Signal')

    # Define a function to apply random perturbations to the 'x' marker positions

    # Iterate through the rpeaks_results dictionary and plot the R-peaks
    marker_perturbation_range = 0.005 * np.max(signal)  # Define the range of the random perturbations
    for is_inverted, cleaning_dict in rpeaks_results.items():
        for cleaning_str, method_dict in cleaning_dict.items():
            for (method_str, setting_str), rpeaks in method_dict.items():
                perturbed_signal = [apply_perturbation(signal[r], marker_perturbation_range) for r in rpeaks]
                plt.scatter(time[rpeaks], perturbed_signal, marker='x', label=f'{method_str}-{setting_str}')

    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.legend(loc='upper right')
    plt.show()


def apply_perturbation(value, perturbation_range):
    return value + random.uniform(-perturbation_range, perturbation_range)