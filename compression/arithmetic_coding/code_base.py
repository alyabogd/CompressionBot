"""Module contains common functional for encoder and decoder"""


class CodeBase:
    # Maximum number of bits in state
    STATE_SIZE_IN_BITS = 32

    # Mask of STATE_SIZE_IN_BITS ones: 1111... (also the highest value of state)
    STATE_MASK = (1 << STATE_SIZE_IN_BITS) - 1

    # Mask to get top bit of state (10000... width=STATE_SIZE_IN_BITS )
    TOP_BIT = 1 << (STATE_SIZE_IN_BITS - 1)

    # Mask to get second top bit of state (01000... width=STATE_SIZE_IN_BITS )
    SECOND_BIT = TOP_BIT >> 1

    def __init__(self):
        # define state
        self.low = 0
        self.high = CodeBase.STATE_MASK

    def update_state(self, symbol_ord, frequency_table):
        """
        Update state of codebase by processing
        given symbol based on given frequency_table
        """

        symbol_low_bound, symbol_high_bound = frequency_table.get_probability_bounds(symbol_ord)
        if symbol_high_bound == symbol_low_bound:
            raise ValueError("Got symbol with 0 probability in update. ord=" + symbol_ord)

        # compute new low and high
        low = self.low
        high = self.high

        range_for_old = high - low + 1

        self.low = low + symbol_low_bound * range_for_old // frequency_table.total_symbols
        self.high = low + symbol_high_bound * range_for_old // frequency_table.total_symbols - 1

        # check if top bits are equal
        self._check_most_significant_bits()

        # check if values of low and high are close but top bits are different
        self._check_converging()

    def reset_range(self):
        self.low = 0
        self.high = CodeBase.STATE_MASK

    def _check_most_significant_bits(self):
        """
        Since low bound only increases and high bound only decreases
        if most significant bit of high and low are equal - it won't change
        and can be written to output
        """

        while (self.low ^ self.high) & CodeBase.TOP_BIT == 0:
            self._process_top_bit()

            # update range
            self.low = (self.low << 1) & CodeBase.STATE_MASK
            self.high = ((self.high << 1) & CodeBase.STATE_MASK) | 1

    def _check_converging(self):
        """
        Called to handle situation when values of low and
        high are close but top bits are different
        E.g. low = 01... high = 10...
        """

        while self.low & ~self.high & CodeBase.SECOND_BIT != 0:
            self._process_pending_bit()

            # update range
            self.low = (self.low << 1) & (CodeBase.STATE_MASK >> 1)
            self.high = ((self.high << 1) & (CodeBase.STATE_MASK >> 1)) | CodeBase.TOP_BIT | 1

    def _process_top_bit(self):
        raise NotImplementedError()

    def _process_pending_bit(self):
        raise NotImplementedError()
