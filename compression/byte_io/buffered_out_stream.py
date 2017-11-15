class OutBuffer:
    def __init__(self, out_name):
        self.out_name = out_name
        # will hold current bits that is not enough to form a byte
        self.byte = 0
        self.bits_in_byte = 0

        self.to_write = bytearray()

    def append_int(self, value, width_in_bits):
        """
        Appends int value to buffer
        Uses big endian byte order (higher bytes first)
        """
        for i in reversed(range(width_in_bits)):
            self.append_bit((value >> i) & 1)

    def append_bit(self, bit):
        """
        Adds bit to temporary holder
        Write to file if there's enough bits to form a byte
        """
        self.byte = (self.byte << 1) | bit
        self.bits_in_byte += 1

        if self.bits_in_byte == 8:
            self._flush_byte()

    def _flush_byte(self):
        """Add byte to output and clean up"""
        self.to_write.append(self.byte)

        self.byte = 0
        self.bits_in_byte = 0

    def _append_remain_bits(self):
        while self.bits_in_byte != 0:
            self.append_bit(0)

    def perform_write(self):
        self._append_remain_bits()

        with open(self.out_name, "wb") as out_stream:
            for byte in self.to_write:
                out_stream.write(bytes((byte,)))
