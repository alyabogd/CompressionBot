"""Main module for compressing"""

import sys

from arithmetic_coding.encode import Encoder
from byte_io.buffered_out_stream import OutBuffer
from symbols_frequency import FrequencyTable, compute_frequencies


def main(args):
    # Handle command line arguments
    if len(args) != 2:
        sys.exit("Usage: compress.py InputFile OutputFile")
    in_file = args[0]
    out_file = args[1]
    # compute frequency table for input file
    frequencies = compute_frequencies(in_file)
    frequency_table = FrequencyTable(frequencies)
    out_buffer = OutBuffer(out_file)
    # append frequency to the compressed file
    frequency_table.append_compressed(out_buffer)
    encoder = Encoder(out_buffer)
    encoder.compress(in_file, frequency_table)


if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)
