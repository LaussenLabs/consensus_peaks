CORRECTION_TOLERANCE = 0.10
CONSENSUS_THRESHOLD = 10

INVERSION_STR_LIST = ['reg', 'inv']
INVERSION_BOOL_LIST = [False, True]

REG_R_PEAK_METHODS = ['neurokit', 'biosppy']
INV_R_PEAK_METHODS = [f"i_{method_str}" for method_str in REG_R_PEAK_METHODS]
