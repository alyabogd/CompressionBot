"""Main module for compressing"""
import sys

from symbols_frequency import FrequencyTable, compute_frequencies
from out_buffer import OutBuffer
from encode import Encoder

if __name__ == "__main__":
    args = sys.argv[1:]

    # Handle command line arguments
    if len(args) != 2:
        sys.exit("Usage: python arithmetic-compress.py InputFile OutputFile")

    in_file = args[0]
    out_file = args[1]

    out_buffer = OutBuffer()

    f_table = FrequencyTable(compute_frequencies(in_file))
    f_table.append_compressed(out_buffer)

    encoder = Encoder(out_buffer)
    encoder.compress(in_file, f_table)

    out_buffer.write_to_file(out_file)
