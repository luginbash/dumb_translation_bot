#!/usr/bin/env python3

from functools import partial
import threading
import asyncio

import typer
from polyglot.detect import Detector
import deepl
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler

import logging

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ /start is the default command to receive from a user at first interaction => should be handled."""
    await update.message.reply_text("Hey! You started this.")


async def translate_inline_result_article(translator: deepl.Translator, text: str, source_lang: str, target_lang: str):
    """ translate a text to target language"""
    log = logging.getLogger(__name__)
    log.info(f"translating from {source_lang} to {target_lang}")
    result = translator.translate_text(text, target_lang=target_lang)
    return_text = f"""{result.text}
<tg-spoiler><i>original text: {text} 
translated by a stupid translation bot.</i></tg-spoiler>"""
    return InlineQueryResultArticle(id=str(uuid4()),
                                    title=f"{result.detected_source_lang} => {target_lang}",
                                    description=result.text,
                                    input_message_content=InputTextMessageContent(message_text=return_text,
                                                                                  parse_mode=ParseMode.HTML))


async def inline_translate(update: Update, ctx: ContextTypes.DEFAULT_TYPE, translator: deepl.Translator, target_langs: list[str]) -> None:
    """ inline handler """
    log = logging.getLogger(__name__)
    query = update.inline_query.query
    if len(query) > 3:
        # determine the languages in the query, then remove it from the target langs
        query_langs = Detector(query, quiet=True)
        query_lang = str(query_langs.language.code).split("_")[0].upper()
        log.debug(f"detected query_lang={query_lang}")
        target_langs = [l for l in target_langs if not l.startswith(query_lang)]
        log.debug(f"removed detected lang:{query_lang} from target_langs list")
        tasks = set()
        for lang in target_langs:
            tasks.add(asyncio.create_task(translate_inline_result_article(
                translator=translator,
                text=query,
                source_lang=query_lang,
                target_lang=lang,
            )))

        results = await asyncio.gather(*tasks)
        await update.inline_query.answer(results)


def main(telegram_token: str = typer.Option("", envvar="TELEGRAM_TOKEN"),
         telegram_api: str = typer.Option("https://api.telegram.org/bot", envvar="TELEGRAM_API"),
         deepl_auth_key: str = typer.Option("", envvar="DEEPL_AUTH_KEY"),
         target_languages: list[str] = typer.Option(["JA", "EN-US", "EN-GB", "ZH"], envvar="TARGET_LANGS"),
         log_level: str = typer.Option("INFO", envvar="LOG_LEVEL")) -> None:
    """ entry point """
    logging.getLogger().setLevel(log_level)
    log = logging.getLogger(__name__)
    log.info(f"using telegram api: telegram_api");
    log.debug("debug enabled")

    app = Application.builder().token(telegram_token).base_url(telegram_api).build()
    app.add_handler(CommandHandler("start", start))

    translator = deepl.Translator(deepl_auth_key)
    app.add_handler(InlineQueryHandler(partial(inline_translate, translator=translator, target_langs=target_languages)))

    app.run_polling()


if __name__ == "__main__":
    typer.run(main)
