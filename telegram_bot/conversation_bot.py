import logging
import os

from telegram import ChatAction
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

import compress
import decompress
from telegram_bot.checker import files_equal
from telegram_bot.configs import Config
from telegram_bot.web_parser import get_links_to_text_files, download_text_file

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=Config.HELLO_MESSAGE)
    bot.send_message(chat_id=update.message.chat_id, text=Config.HOW_TO_USE)
    logging.info("Bot started with {}".format(update.message['chat']))


def _download_file(bot, document):
    file_name = document.file_name
    file = bot.getFile(document.file_id)
    file.download(file_name)
    logging.debug("downloaded {}".format(file_name))
    return file_name


def _send_files(bot, chat_id, file_name, *names):
    for name in (file_name, *names):
        logging.info("Sending {}".format(name))
        bot.send_document(chat_id=chat_id, document=open(name, "rb"))


def _decompress(from_file):
    logging.debug("decompressing {}".format(from_file))
    return decompress.main(from_file)


def _compress(from_file, *files, to_file=None):
    if not to_file:
        to_file = "{}.in".format(".".join(from_file.split(".")[:-1]))

    logging.debug("compressing started")
    compress.main(from_file, *files, out_file=to_file)

    from_size = 0
    for file in (from_file, *files):
        from_size += os.path.getsize(file)
    to_size = os.path.getsize(to_file)
    logging.info("compressed: {} -> {} : {}%".format(from_size, to_size, (1.0 * to_size / from_size)))
    return [to_file]


def files_handler(bot, update):
    logging.info("Start processing file {}".format(update.message.document))
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
    in_file = _download_file(bot, update.message.document)
    update.message.reply_text(Config.FILE_UPLOADED_MESSAGE)

    file_type = in_file.split(".")[-1]
    if file_type in Config.compressed_types:
        update.message.reply_text(Config.DECOMPRESS_STARTED_MESSAGE.format(file_name=in_file))
        out_names = _decompress(in_file)
    else:
        update.message.reply_text(Config.COMPRESS_STARTED_MESSAGE.format(file_name=in_file))
        out_names = _compress(in_file)

    update.message.reply_text(Config.DONE_MASSAGE)
    logging.info("processed {}".format(in_file))

    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
    _send_files(bot, update.message.chat_id, *out_names)

    os.remove(in_file)
    for file in out_names:
        os.remove(file)


def _check_compression(full_files, compressed_file):
    logging.info("Checking  -> {}".format(compressed_file))

    for file in full_files:
        os.rename(file, "i" + file)
    decompressed_names = _decompress(compressed_file)

    for decoded in decompressed_names:
        if files_equal(decoded, "i" + decoded):
            logging.info("correct")
        else:
            logging.error("error found {} -> {}".format("i" + decoded, decoded))

        os.remove("i" + decoded)


def web_page_handler(bot, update, args):
    if len(args) < 1:
        update.message.reply_text(Config.NO_WEB_ADDRESS_FOUND)
        return

    web_address = args[0]

    debug = False
    if len(args) > 1 and args[1] == "debug":
        debug = True
        logging.info("-- scan with debug --")

    logging.info("Start parsing {}".format(web_address))
    text_links = get_links_to_text_files(web_address)

    logging.debug("Got {} links from {}".format(len(text_links), web_address))
    update.message.reply_text(Config.WEB_SCAN_RESULT.format(len(text_links)))

    file_names = download_files(text_links, web_address)
    update.message.reply_text(Config.FILES_DOWNLOADED_STATUS)

    compressed_file_name = "archive.in"
    _compress(*file_names, to_file=compressed_file_name)

    update.message.reply_text(Config.DONE_MASSAGE)

    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
    _send_files(bot, update.message.chat_id, compressed_file_name)

    if debug:
        _check_compression(file_names, compressed_file_name)

    logging.info("Done processing {}".format(compressed_file_name))

    for file in file_names:
        os.remove(file)
    os.remove(compressed_file_name)

    logging.info("Removed all temp files")


def download_files(text_links, web_address):
    file_names = []
    for file in text_links:
        file_name = download_text_file(web_address, file)
        file_names.append(file_name)
        logging.info("downloaded: {}".format(file_name))
    return file_names


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=Config.UNKNOWN_COMMAND_MESSAGE)


def help_handler(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=Config.HOW_TO_USE)


def main():
    updater = Updater(token=Config.BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.document, files_handler))
    dispatcher.add_handler(CommandHandler('scan', web_page_handler, pass_args=True))
    dispatcher.add_handler(CommandHandler('help', help_handler))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()


if __name__ == "__main__":
    main()
