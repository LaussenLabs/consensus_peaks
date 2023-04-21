# consensus_peaks

`consensus_peaks` is a Python library for robust ECG R-peak detection using a consensus-based approach. It calculates R-peaks using a matrix of cleaning methods versus detection methods and selects R-peak locations based on the consensus of all individual cleaning-detection combinations.

## Motivation

This project aims to provide a more robust means of ECG R-peak detection than currently available Python libraries. It is designed to analyze all R-peak cleaning and detection options to further evaluate best practices and their behavior in different niche environments, such as pediatric patients, presence of arrhythmia, etc.

## Installation

To install the `consensus_peaks` library, navigate to the directory containing the `setup.py` file and run the following command:

```
pip install .
```

This will install the library and its dependencies.

## Usage

Here's a simple example demonstrating how to use `consensus_peaks` with the `wfdb` library:

```python
import wfdb
from consensus_peaks import consensus_detect

# Load a sample ECG record from the MIT-BIH Arrhythmia Database using the wfdb library
record = wfdb.rdrecord('100', pb_dir='mitdb', sampto=10000)
signal = record.p_signal[:, 0]
freq_hz = record.fs

# Detect R-peaks using the consensus_peaks library
peaks = consensus_detect(signal, freq_hz)

# `peaks` now contains the indices of R-peaks in the signal
```

## Features and Functionality

The main features of `consensus_peaks` include:

- Consensus-based R-peak detection using various cleaning and detection methods.
- Customizable consensus threshold.
- Signal inversion support.
- Plotting functions for visualizing consensus peaks, consensus signal, and individual R-peaks.

## Project Structure

- `consensus_peaks.ipynb`: Jupyter notebook showcasing the usage of the library.
- `consensus_peaks`: Main package containing the source code for the library.
  - `consensus_peaks.py`: Main R-peak detection function.
  - `consensus_signal.py`: Functions for calculating consensus signal.
  - `individual_rpeaks.py`: Functions for obtaining individual R-peaks.
  - `detectors`: Subpackage containing signal cleaning and R-peak detection methods.
  - `plotting`: Subpackage containing plotting functions.
- `tests`: Package containing test cases and utilities.
  - `generate_wfdb.py`: Utility for generating test records.
  - `test_consensus_peaks.py`: Test cases for consensus peaks.
  - `test_consensus_signal.py`: Test cases for consensus signal.
  - `test_individual_rpeaks.py`: Test cases for individual R-peaks.

## Testing

To run the tests for the project, simply install `pytest` and execute `pytest` in the project directory:

```
pip install pytest
pytest
```

## Contributing

If you want to contribute to the project, please submit an issue or a pull request on the [LaussenLabs/consensus_peaks](https://github.com/LaussenLabs/consensus_peaks) GitHub repository.

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for more information.

## Acknowledgments

William Dixon and Andrew Goodwin are responsible for developing the consensus technique used in this project.

We would like to extend our gratitude to the following libraries and their contributors for providing valuable resources and methods that were used in the development of the `consensus_peaks` library:

- **HeartPy**: For providing the `flip_signal` function, which is used to handle signal inversion.
- **NeuroKit2**: For their implementation of various cleaning and R-peak detection methods, which were incorporated into the consensus approach.
- **biosppy**: For their R-peak detection methods and R-peak correction algorithms, which contributed to the accuracy and robustness of the `consensus_peaks` library.

We appreciate the efforts of the developers and maintainers of these libraries for their contributions to the field of ECG analysis and open-source software.

## Contact

If you have any questions or feedback, please get in touch with us through the [LaussenLabs/consensus_peaks](https://github.com/LaussenLabs/consensus_peaks) GitHub repository.