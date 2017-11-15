"""Main module for compressing"""

import sys

from compression.arithmetic_coding.encode import Encoder
from compression.byte_io.buffered_out_stream import OutBuffer
from compression.symbols_frequency import FrequencyTable, compute_frequencies


def get_text_as_bytes(file_name):
    text = []
    with open(file_name, "rb") as inp:
        text = inp.read()
    return text


def main(in_file, out_file):

    text = get_text_as_bytes(in_file)

    # compute frequency table for input text
    frequencies = compute_frequencies(text)
    frequency_table = FrequencyTable(frequencies)

    out_buffer = OutBuffer(out_file)

    # append frequency to the compressed file
    frequency_table.append_compressed(out_buffer)

    encoder = Encoder(out_buffer)
    encoder.compress(text, frequency_table)


if __name__ == "__main__":
    args = sys.argv[1:]

    # Handle command line arguments
    if len(args) != 2:
        sys.exit("Usage: compress.py InputFile OutputFile")

    main(*args)
