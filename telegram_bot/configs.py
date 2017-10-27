class Config:
    BOT_TOKEN = "455939843:AAE6SpHm2aQzm6sSMMdyuBhpVyqL8YFDbww"

    compressed_types = ["in"]

    HELLO_MESSAGE = "Hi! I can compress your files. I can even compress you. Ha-ha."
    HOW_TO_USE = """
    Just send me any txt file and I will compress it. 
    But if you send me an \'in\' file, I will decompress it. That's how I work.
    /scan web-address - will scan given url and compress all txt files found
     """

    UNKNOWN_COMMAND_MESSAGE = "Sorry, I don't understand this command"
    FILE_UPLOADED_MESSAGE = "File successfully uploaded"
    FILE_DOWNLOADING_MESSAGE = "Downloading {}"

    DECOMPRESS_STARTED_MESSAGE = "Decompressing {file_name}..."
    COMPRESS_STARTED_MESSAGE = "Compressing {file_name}..."

    DONE_MASSAGE = "Done"

    NO_WEB_ADDRESS_FOUND = "Give me web address to scan"

    WEB_SCAN_RESULT = "{} links found"
