"""Input buffer implementation"""


class InBuffer:
    def __init__(self, in_file=None, data=None):
        """Initialize in_buffer with either file content or bytes array"""
        self.buffer = None

        if in_file is not None:
            with open(in_file, "rb") as inp:
                self.buffer = inp.read().__iter__()

        if data is not None:
            self.buffer = data.__iter__()

        # buffer for current byte
        self.byte = 0
        self.pending_bits_in_byte = 0

        self.is_eof = False
        self.bytes_read = 0

    def take_next_bit(self):
        """Takes next bit from buffer. Returns -1 if there isn't any"""
        if self.is_eof:
            return -1
        if self.pending_bits_in_byte == 0:
            try:
                self.byte = self.buffer.__next__()
            except StopIteration:
                self.is_eof = True
                return -1
            self.pending_bits_in_byte = 8
            self.bytes_read += 1

        self.pending_bits_in_byte -= 1
        return (self.byte >> self.pending_bits_in_byte) & 1

    def take_next_bytes(self, number):
        value = bytearray()
        for i in range(number):
            value.append(self.take_next_int(8))
        return value

    def take_next_int(self, width_in_bits):
        """
        Reads width_in_bits bits from buffer
        Returns integer value of bits read
        """
        value = 0
        for i in range(width_in_bits):
            bit = self.take_next_bit()
            value = (value << 1) | bit
        return value

    def shift_to_next_byte(self):
        """Skip remain bits in current byte"""
        while self.pending_bits_in_byte != 0:
            self.take_next_bit()
