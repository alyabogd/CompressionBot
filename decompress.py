"""Main module for decompressing"""

import sys

from compression.arithmetic_coding.decode import Decoder
from compression.byte_io.buffered_in_stream import InBuffer
from compression.symbols_frequency import FrequencyTable


def read_frequencies(in_buffer):
    freqs = []
    for _ in range(256):
        f = in_buffer.take_next_int(32)
        freqs.append(f)
    # add EOF symbol
    freqs.append(1)

    return freqs


def main(in_file):
    """
    Structure of compressed file:
    16 bits: number of files compressed - n
    n times (mapping):
          8 bits: len of file_name
          file_name
    n compressed files:
        256 * 32 bits: frequencies
        compressed content
    """

    in_buffer = InBuffer(in_file)
    in_buffer.read()

    num_of_files = in_buffer.take_next_int(16)

    mapping = []
    for i in range(num_of_files):
        name_len = in_buffer.take_next_int(8)
        out_name = in_buffer.take_next_bytes(name_len).decode("utf-8")
        mapping.append(out_name)

    decoder = Decoder()

    for name in mapping:
        # read and build frequency table from compressed file
        frequencies = read_frequencies(in_buffer)
        frequency_table = FrequencyTable(frequencies)

        decoder.decode(in_buffer, "1" + name, frequency_table)


if __name__ == "__main__":
    args = sys.argv[1:]
    main(*args)
