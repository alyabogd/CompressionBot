"""Input buffer implementation"""


class InBuffer:
    def __init__(self, in_file):
        # read stream to compressed file
        self.in_stream = open(in_file, "rb")

        # byte buffer
        self.byte = 0
        self.pending_bits_in_byte = 0

        self.is_eof = False
        self.buffer = None

    def read(self, bytes_num=-1):
        """Reads bytes_num bytes from file into buffer"""
        self.buffer = self.in_stream.read(bytes_num).__iter__()

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

        self.pending_bits_in_byte -= 1
        return (self.byte >> self.pending_bits_in_byte) & 1

    def read_int(self, width_in_bits):
        """
        Reads width_in_bits bits from buffer
        Returns integer value of bits read
        """
        value = 0
        for i in range(width_in_bits):
            bit = self.take_next_bit()
            value = (value << 1) | bit
        return value

    def close(self):
        self.in_stream.close()
