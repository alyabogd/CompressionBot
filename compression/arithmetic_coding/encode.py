"""Module with basic encoding algorithm implementation"""

from compression.arithmetic_coding.code_base import CodeBase


class Encoder(CodeBase):
    def __init__(self, out_buffer):
        super().__init__()
        self.out_buffer = out_buffer
        self.frequencies_table = None

        self.bits_pending = 0

    def compress(self, text, frequencies_table):
        """
        Performs compression of given text in
        out_buffer based on given frequencies_table
        Text is considered to be a byte array
        """
        self.frequencies_table = frequencies_table

        for byte in text:
            self.update_state(byte, self.frequencies_table)

        # write EOF
        self.update_state(256, self.frequencies_table)
        self.out_buffer.append_bit(1)
        self.out_buffer.finish()

    def _process_pending_bit(self):
        self.bits_pending += 1

    def _process_top_bit(self):
        bit = (self.low >> (CodeBase.STATE_SIZE_IN_BITS - 1)) & 1
        self.out_buffer.append_bit(bit)

        # Write pending bits
        while self.bits_pending != 0:
            self.out_buffer.append_bit(bit ^ 1)
            self.bits_pending -= 1
