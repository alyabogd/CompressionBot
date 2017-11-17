"""Main module for compressing"""

import sys
import os

from compression.arithmetic_coding.encode import Encoder
from compression.byte_io.buffered_out_stream import OutBuffer
from compression.symbols_frequency import FrequencyTable, compute_frequencies


def get_text_as_bytes(file_name):
    text = []
    with open(file_name, "rb") as inp:
        text = inp.read()
    return text


def main(in_file, *files, out_file="compressed.txt"):
    """
    Structure of compressed file:
    16 bits: number of files compressed - n
    n times (mapping):
          8 bits: len of file_name
          file_name
          32 bits: size of compressed file (in bytes)
    n compressed files:
        256 * 32 bits: frequencies
        compressed content
    """

    out_buffer = OutBuffer()

    num_of_files = len(files) + 1
    out_buffer.append_int(num_of_files, 16)

    mapping = []

    content_out_buffer = OutBuffer()

    for file in (in_file, *files):
        if len(file) == 0:
            continue

        text = get_text_as_bytes(file)

        content_out_buffer.set_bytes_counter(0)

        # compute frequency table for input text
        frequencies = compute_frequencies(text)
        frequency_table = FrequencyTable(frequencies)

        # append frequency to the compressed file
        frequency_table.append_compressed(content_out_buffer)
        content_encoder = Encoder(content_out_buffer)
        content_encoder.compress(text, frequency_table)

        file_size_in_bytes = content_out_buffer.get_bytes_counter()

        mapping.append((file, file_size_in_bytes))

    for name, length in mapping:
        out_buffer.append_int(len(name), 8)
        out_buffer.append_bytes(bytes(name, "utf-8"))
        out_buffer.append_int(length, 32)
    out_buffer.append_remain_bits()

    out_buffer.append_bytes(content_out_buffer.get_buffered_bytes())
    out_buffer.perform_write(out_file)


if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) == 0:
        sys.exit("Usage: InputFile [, files]")

    if len(args) == 1:
        out_name = ".".join(args[0].split(".")[:-1]) + ".in"
        main(args[0], out_file=out_name)
        print("Compressed: {}".format(out_name))
        sys.exit()

    folder_path = os.path.dirname(os.path.realpath(__file__))
    folder_name = os.path.basename(folder_path)
    out_name = os.path.join(folder_path, folder_name) + ".in"
    main(*args, out_file=out_name)
    print("Compressed: {}".format(folder_name + ".in"))
