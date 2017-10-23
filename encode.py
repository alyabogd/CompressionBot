"""Module with basic encoding algorithm implementation"""

from symbols_frequency import FrequencyTable
from out_buffer import OutBuffer


class Encoder:
    # Maximum number of bits in state
    STATE_BITS = 32

    # Mask of STATE_BITS ones: 1111... (also the highest value of state)
    STATE_MASK = (1 << STATE_BITS) - 1

    # Mask to get top bit of state (10000... width=STATE_BITS )
    TOP_BIT = 1 << (STATE_BITS - 1)

    # Mask to get second top bit of state (01000... width=STATE_BITS )
    SECOND_BIT = TOP_BIT >> 1

    def __init__(self, out_buffer):
        self.out_buffer = out_buffer
        self.frequencies_table = None

        # define state
        self.low = None
        self.high = None

        self.bits_pending = 0

    def compress(self, file_name, frequencies_table):
        """
        Performs compression of text in file_name
        in out_buffer based on given frequencies_table
        """
        self.frequencies_table = frequencies_table

        self.low = 0
        self.high = Encoder.STATE_MASK

        with open(file_name, "rb") as inp:
            b = inp.read(1)
            while len(b) != 0:
                self._process_next_byte(ord(b))
                b = inp.read(1)
            # add EOF
            self._process_next_byte(256)

    def _process_next_byte(self, b_ord):

        byte_low_bound, byte_high_bound = self.frequencies_table.get_probability_bounds(b_ord)
        if byte_low_bound == byte_high_bound:
            raise ValueError("Symbol that has 0 frequency got in encoder: ord={}".format(b_ord))

        self._update_state(byte_low_bound, byte_high_bound)

        self._check_top_bits()

        self._check_converging()

    def _update_state(self, byte_low_bound, byte_high_bound):
        """Updates low and high bounds of encoder"""

        # make state copy
        low = self.low
        high = self.high

        range_for_old = low - high

        self.low = low + byte_low_bound * range_for_old // self.frequencies_table.total_symbols
        self.high = low + byte_high_bound * range_for_old // self.frequencies_table.total_symbols + 1

    def _check_top_bits(self):
        # while top bits are equal
        while ((self.low ^ self.high) & Encoder.TOP_BIT) == 0:
            # push top bit into out_buffer
            top_bit = (self.low & Encoder.TOP_BIT) >> Encoder.STATE_BITS - 1
            assert top_bit in (0, 1)

            self.out_buffer.append_bit(top_bit)
            while self.bits_pending != 0:
                self.out_buffer.append_bit(top_bit)
                self.bits_pending -= 1

            # shift bounds
            self.low = (self.low << 1) & Encoder.STATE_MASK
            self.high = ((self.high << 1) & Encoder.STATE_MASK) | 1

    def _check_converging(self):
        # while low = 01... and high=10...
        while ((self.low & ~self.high) & Encoder.SECOND_BIT) != 0:
            self.bits_pending += 1

            self.low = (self.low << 1) & (Encoder.STATE_MASK >> 1)

            self.high = ((self.high << 1) & (Encoder.STATE_MASK >> 1))
            self.high |= Encoder.TOP_BIT
            self.high |= 1
