"""Main module for decompressing"""

import sys

from compression.arithmetic_coding.decode import Decoder
from compression.byte_io.buffered_in_stream import InBuffer
from compression.symbols_frequency import FrequencyTable


def read_frequencies(in_buffer):
    freqs = []
    for _ in range(256):
        f = in_buffer.read_int(32)
        freqs.append(f)
    # add EOF symbol
    freqs.append(1)

    return freqs


def main(in_file, out_file):
    in_buffer = InBuffer(in_file)
    in_buffer.read()

    # read and build frequency table from compressed file
    frequencies = read_frequencies(in_buffer)
    frequency_table = FrequencyTable(frequencies)

    decoder = Decoder()
    decoder.decode(in_buffer, out_file, frequency_table)


if __name__ == "__main__":
    args = sys.argv[1:]

    # Handle command line arguments
    if len(args) != 2:
        sys.exit("Usage: decompress.py InputFile OutputFile")

    main(*args)
