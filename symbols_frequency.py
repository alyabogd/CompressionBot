"""Statistical methods for analysing symbols frequency in a file"""


class FrequencyTable:
    """
    self.frequencies - list of frequencies for each input byte
                    Keys are int numbers for corresponding bytes
                    Since byte's range is [0, 255] => max_length = 256

    self.scale -
    """

    def __init__(self, symbols_frequencies):
        # copy given list
        self.frequencies = list(symbols_frequencies)

        self.total_symbols = 0
        self.scale = None

        self._compute_total()
        self._compute_scale()

    def _compute_total(self):
        """
        Computes total number of symbols
        Also checks all frequencies must be >= 0
        """
        for i, f in enumerate(self.frequencies):
            if f < 0:
                raise ValueError("Frequency must be >= 0. Got frequency[{}]={}".format(i, f))
            self.total_symbols += f

    def _compute_scale(self):
        """
        Computes cumulative frequency for each symbol
        """
        self.scale = [0 for _ in range(len(self.frequencies))]
        freqs_sum = 0
        for i, freq in enumerate(self.frequencies):
            freqs_sum += freq
            self.scale[i] = freqs_sum

    def get_frequency(self, symbol_ord):
        self.check_if_present(symbol_ord)
        return self.frequencies[symbol_ord]

    def get_probability_bounds(self, symbol_ord):
        self.check_if_present(symbol_ord)

        # the last symbol is emulated and it's frequency == 0
        low_bound = self.scale[symbol_ord - 1]
        high_bound = self.scale[symbol_ord]

        return low_bound, high_bound

    def get_symbol_by_frequency_value(self, value):
        """
        Uses binary search to find symbol
        to which bounds given value belongs
        """

        l = 0
        r = len(self.frequencies)
        while r - l > 1:
            middle = (r + l) // 2
            low, high = self.get_probability_bounds(middle)
            if value < low:
                r = middle
            else:
                l = middle
        return l

    def check_if_present(self, symbol_ord):
        if symbol_ord < 0 or symbol_ord >= len(self.frequencies):
            raise ValueError("Symbol ord out of range: 0 <= {} < {}"
                             .format(symbol_ord, len(self.frequencies)))

    def append_compressed(self, out_buffer):
        width = 32
        for i in range(256):
            out_buffer.append_int(self.frequencies[i], width)


def compute_frequencies(file_name):
    """
    Reads input file per bytes
    Computes frequencies of each input byte
    """
    frequencies = [0 for _ in range(257)]

    with open(file_name, "rb") as inp:
        b = inp.read(1)
        while len(b) != 0:
            b_ord = ord(b)
            frequencies[b_ord] += 1
            b = inp.read(1)
    # EOF symbol
    frequencies[256] += 1
    return frequencies
