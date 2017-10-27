import logging
import os

from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from telegram import ChatAction

from compression import decompress, compress
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


def _send_file(bot, chat_id, file_name):
    bot.send_document(chat_id=chat_id, document=open(file_name, "rb"))


def _decompress(from_file):
    to_file = "{}.txt".format(".".join(from_file.split(".")[:-1]))
    decompress.main(from_file, to_file)
    return to_file


def _compress(from_file):
    to_file = "{}.in".format(".".join(from_file.split(".")[:-1]))
    compress.main(from_file, to_file)
    return to_file


def files_handler(bot, update):
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
    in_file = _download_file(bot, update.message.document)
    update.message.reply_text(Config.FILE_UPLOADED_MESSAGE)

    file_type = in_file.split(".")[-1]
    if file_type in Config.compressed_types:
        update.message.reply_text(Config.DECOMPRESS_STARTED_MESSAGE.format(file_name=in_file))
        logging.info("decompressing {}".format(in_file))
        out_file = _decompress(in_file)
    else:
        update.message.reply_text(Config.COMPRESS_STARTED_MESSAGE.format(file_name=in_file))
        logging.info("compressing {}".format(in_file))
        out_file = _compress(in_file)

    update.message.reply_text(Config.DONE_MASSAGE)
    logging.info("finish {}".format(in_file))
    bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
    _send_file(bot, update.message.chat_id, out_file)

    os.remove(in_file)
    os.remove(out_file)


def web_page_handler(bot, update, args):
    if len(args) < 1:
        update.message.reply_text(Config.NO_WEB_ADDRESS_FOUND)
        return

    web_address = args[0]
    logging.info("Start parsing {}".format(web_address))
    text_links = get_links_to_text_files(web_address)

    logging.info("Got {} links from {}".format(len(text_links), web_address))
    update.message.reply_text(Config.WEB_SCAN_RESULT.format(len(text_links)))

    for file in text_links:
        logging.info("start processing {}".format(file))
        update.message.reply_text(Config.FILE_DOWNLOADING_MESSAGE.format(file))
        in_file = download_text_file(web_address, file)

        update.message.reply_text(Config.COMPRESS_STARTED_MESSAGE.format(file_name=in_file))
        logging.info("compressing {}".format(in_file))
        out_file = _compress(in_file)

        update.message.reply_text(Config.DONE_MASSAGE)
        logging.info("finish {}".format(in_file))

        bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.UPLOAD_DOCUMENT)
        _send_file(bot, update.message.chat_id, out_file)

        os.remove(in_file)
        os.remove(out_file)


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=Config.UNKNOWN_COMMAND_MESSAGE)


def main():
    updater = Updater(token=Config.BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.document, files_handler))
    dispatcher.add_handler(CommandHandler('scan', web_page_handler, pass_args=True))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()


if __name__ == "__main__":
    main()
