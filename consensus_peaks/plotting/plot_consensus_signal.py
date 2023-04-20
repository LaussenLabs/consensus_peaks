import numpy as np
import matplotlib.pyplot as plt


def plot_consensus_signals(signal, consensus_data, freq_hz):
    consensus_time_dict, consensus_value_dict = consensus_data
    time = np.arange(0, len(signal)) / freq_hz

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 10), sharex=True)

    # Plot the raw ECG signal on the first subplot
    ax1.plot(time, signal, label='ECG Signal')
    ax1.set_ylabel('Amplitude')
    ax1.legend(loc='upper right')
    ax1.set_title('Raw ECG Signal')

    # Plot the consensus signals on the second subplot
    for is_inverted, consensus_times in consensus_time_dict.items():
        inversion_label = "Inverted" if is_inverted else "Non-inverted"
        consensus_values = consensus_value_dict[is_inverted]
        ax2.plot(consensus_times / freq_hz, consensus_values, label=f'{inversion_label} Consensus Signal')

    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('R-peak Counts')
    ax2.legend(loc='upper right')
    ax2.set_title('Consensus Signals')

    plt.tight_layout()
    plt.show()

# Example usage:
# plot_consensus_signals(signal, consensus_data, freq_hz)
