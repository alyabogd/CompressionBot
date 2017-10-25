"""Main module for decompressing"""

import sys

from in_buffer import InBuffer
from symbols_frequency import FrequencyTable
from decode import Decoder


def read_frequencies(in_buffer):
    freqs = []
    for _ in range(256):
        f = in_buffer.read_int(32)
        freqs.append(f)
    # add EOF symbol
    freqs.append(1)

    return freqs


if __name__ == "__main__":
    args = sys.argv[1:]

    # Handle command line arguments
    if len(args) != 2:
        sys.exit("Usage: python arithmetic-decompress.py InputFile OutputFile")

    in_file = args[0]
    out_file = args[1]

    in_buffer = InBuffer(in_file)

    # read and build frequency table from compressed file
    frequencies = read_frequencies(in_buffer)
    frequency_table = FrequencyTable(frequencies)

    decoder = Decoder()
    decoder.decode(in_buffer, out_file, frequency_table)
