"""Module with basic decoding algorithm implementation"""

from compression.arithmetic_coding.code_base import CodeBase


class Decoder(CodeBase):
    def __init__(self):
        super().__init__()
        self.in_buffer = None
        # buffer for bytes read from in_buffer
        self.current_symbol_code = None

    def decode(self, in_buffer, out_file, frequency_table):
        """
        Decode text from in_buffer to out_file based on frequency_table
        in_buffer is considered to be in right place (skip freq table)
        """

        self.in_buffer = in_buffer

        self.reset_range()
        self._read_buffer_initially()

        with open(out_file, "wb") as out:
            symbol = self._decode_next_symbol(frequency_table)
            while symbol != 256:
                out.write(bytes((symbol,)))
                symbol = self._decode_next_symbol(frequency_table)

        self.in_buffer.take_next_bit()
        self.in_buffer.shift_to_next_byte()

    def _decode_next_symbol(self, frequency_table):
        """
        Get new symbol and update state based on given frequency table
        """
        old_range = self.high - self.low + 1
        offset = self.current_symbol_code - self.low
        value = ((offset + 1) * frequency_table.total_symbols - 1) // old_range

        symbol = frequency_table.get_symbol_by_frequency_value(value)

        self.update_state(symbol, frequency_table)

        return symbol

    def _read_buffer_initially(self):
        """Reads STATE_SIZE_IN_BITS bits in buffer"""
        self.current_symbol_code = 0
        for _ in range(CodeBase.STATE_SIZE_IN_BITS):
            bit = self.in_buffer.take_next_bit()
            self.current_symbol_code = (self.current_symbol_code << 1) | bit

    def _process_top_bit(self):
        """Shift existing symbol_code and read one more bit"""
        bit = self.in_buffer.take_next_bit()
        if bit == -1:
            bit = 0
        self.current_symbol_code = ((self.current_symbol_code << 1) & self.STATE_MASK) | bit

    def _process_pending_bit(self):
        """Handle case when range bound were too close"""
        bit = self.in_buffer.take_next_bit()
        if bit == -1:
            bit = 0
        self.current_symbol_code = ((self.current_symbol_code & CodeBase.TOP_BIT) |
                                    ((self.current_symbol_code << 1) & (CodeBase.STATE_MASK >> 1)) | bit)
