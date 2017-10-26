"""Input buffer implementation"""


class InBuffer:
    def __init__(self, in_file):
        # read stream to compressed file
        self.in_stream = open(in_file, "rb")

        # byte buffer
        self.byte = 0
        self.pending_bits_in_byte = 0

        self.is_eof = False

    def read_bit(self):
        if self.is_eof:
            return -1
        if self.pending_bits_in_byte == 0:
            # need to read one more byte
            self.byte = self.in_stream.read(1)
            if len(self.byte) == 0:
                self.is_eof = True
                return -1
            self.byte = ord(self.byte)
            self.pending_bits_in_byte = 8

        self.pending_bits_in_byte -= 1
        return (self.byte >> self.pending_bits_in_byte) & 1

    def read_int(self, width_in_bits):
        """
        Reads width_in_bits bits from in_stream
        Returns integer value of bits read
        """
        value = 0
        for i in range(width_in_bits):
            bit = self.read_bit()
            value = (value << 1) | bit
        return value

    def close(self):
        self.in_stream.close()
