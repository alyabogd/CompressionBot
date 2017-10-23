class OutBuffer:
    def __init__(self):
        self.buffer = []
        # will hold current bits that is not enough to form a byte
        self.byte = 0
        self.bits_in_byte = 0

    def append_int(self, value, width_in_bits):
        """
        Appends int value to buffer
        Uses big endian byte order (higher bytes first)
        """
        for i in reversed(range(width_in_bits)):
            self.append_bit((value >> i) & 1)

    def append_bit(self, bit):
        # add new bit to the end
        self.byte = (self.byte << 1) | bit
        self.bits_in_byte += 1

        if self.bits_in_byte == 8:
            self._flush_byte()

    def write_to_file(self, file_name):
        while self.bits_in_byte != 0:
            self.append_bit(0)

        with open(file_name, "wb") as out:
            # out.write(bytes(self.buffer))
            for n in self.buffer:
                out.write(n)

    def _flush_byte(self):
        """Add byte to buffer and clean up"""
        self.buffer.append(bytes((self.byte,)))

        self.byte = 0
        self.bits_in_byte = 0
