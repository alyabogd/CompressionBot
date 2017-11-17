class OutBuffer:
    def __init__(self):
        # will hold current bits that is not enough to form a byte
        self.byte = 0
        self.bits_in_byte = 0
        self.to_write = bytearray()
        self.bytes_counter = 0

    def append_int(self, value, width_in_bits):
        """
        Appends int value to buffer
        Uses big endian byte order (higher bytes first)
        """
        for i in reversed(range(width_in_bits)):
            self.append_bit((value >> i) & 1)

    def append_bytes(self, byte_sequence):
        for byte in byte_sequence:
            for i in reversed(range(8)):
                self.append_bit((byte >> i) & 1)

    def append_bit(self, bit):
        """
        Adds bit to temporary holder
        Write to file if there's enough bits to form a byte
        """
        self.byte = (self.byte << 1) | bit
        self.bits_in_byte += 1

        if self.bits_in_byte == 8:
            self._flush_byte()

    def get_buffered_bytes(self):
        self.append_remain_bits()
        return self.to_write

    def get_bytes_counter(self):
        return self.bytes_counter

    def set_bytes_counter(self, n):
        self.bytes_counter = n

    def _flush_byte(self):
        """Add byte to output and clean up"""
        self.to_write.append(self.byte)
        self.bytes_counter += 1

        self.byte = 0
        self.bits_in_byte = 0

    def append_remain_bits(self):
        while self.bits_in_byte != 0:
            self.append_bit(0)

    def perform_write(self, out_name):
        self.append_remain_bits()

        with open(out_name, "wb") as out_stream:
            for byte in self.to_write:
                out_stream.write(bytes((byte,)))
