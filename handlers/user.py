import aiohttp

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineQuery, ChosenInlineResult, InlineQueryResultArticle, InputTextMessageContent

from database.db import mdb

import utils.keyboards as kb

from utils.emoji import *

from uuid import uuid4

import os
from dotenv import load_dotenv


load_dotenv()


router = Router()

LOGS = os.getenv("LOGS")




def generate_uid():
    uid = str(uuid4()).split('-')
    return uid[0] + uid[1]


def normalize_addresses(addresses: list[str]) -> str:
    text = ""
    for i, address in enumerate(addresses, start=1):
        text += f"{i}) <code>{address}</code>\n"
    return text



def is_num(num: str) -> float | bool:
    try:
        return float(num)
    except:
        return False



async def get_last_lime(address):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://tonapi.io/v2/blockchain/accounts/{address}/transactions?limit=1"
        ) as response:
            if response.status == 200:
                data = await response.json()
                transactions = data.get("transactions", [])
                if transactions:
                    last_txn = transactions[0]
                    return last_txn.get("lt")
                else:
                    return 0
            else:
                return 0



async def check_transaction(address: str, last_time: str, amount: int, uid: str) -> None | str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://tonapi.io/v2/blockchain/accounts/{address}/transactions?after_lt={last_time}"
        ) as response:
            dates = await response.json()
            try:
                if len(dates.get("transactions")) != 0:
                    for transaction in dates.get("transactions"):
                        if transaction.get("in_msg").get("value") == amount and transaction.get("in_msg").get("decoded_body").get("text") == uid:
                            hash =  transaction.get("in_msg").get("hash")
                            if hash:
                                return hash
                            else: return None
                        else: continue
                else: return None
            except:
                return None



@router.inline_query()
async def inline_query(query: InlineQuery):
    query_query = query.query

    if is_num(query_query):
        amount = is_num(query_query)

        amount0 = round(amount, 2)
        amount2 = round(amount*1.02, 2)

        uid0 = "num_" + generate_uid()
        uid2 = "num_" + generate_uid()

        kb0 = kb.optimize(uid0)
        kb2 = kb.optimize(uid2)

        result0 = InlineQueryResultArticle(
            id=uid0,
            title="Отправить адрес +0%",
            description=f"{amount0} TON",
            input_message_content=InputTextMessageContent(
                message_text="Создаю...",
                parse_mode='HTML'
            ),
            reply_markup=kb0
        )

        result2 = InlineQueryResultArticle(
            id=uid2,
            title="Отправить адрес +2%",
            description=f"{amount2} TON",
            input_message_content=InputTextMessageContent(
                message_text="Создаю..",
                parse_mode='HTML'
            ),
            reply_markup=kb2
        )

        await query.answer(results=[result0, result2], cache_time=0, is_personal=True)

    else:
        reviews = mdb.get_user_reviews(user_id=query.from_user.id)

        if not query.query:
            uid1 = "without_" + generate_uid()
            kb1 = kb.optimize("1")

            result1 = InlineQueryResultArticle(
                id=uid1,
                title="Отправить адрес",
                description=f"Все адреса TON",
                input_message_content=InputTextMessageContent(
                    message_text="Создаю...",
                    parse_mode='HTML'
                ),
                reply_markup=kb1
            )

            if reviews:
                kb2 = kb.deal_end(reviews)
                result2 = InlineQueryResultArticle(
                    id="None",
                    title="Сделка завершена",
                    description=f"Сделка завершена",
                    input_message_content=InputTextMessageContent(
                        message_text="Сделка завершена!\nСпасибо за сделку, можете оставить отзыв по кнопке снизу",
                        parse_mode='HTML'
                    ),
                    reply_markup=kb2
                )
            else:
                result2 = InlineQueryResultArticle(
                    id="None",
                    title="Отзывы не найдены",
                    description=f"Чат отзывов не настроен",
                    input_message_content=InputTextMessageContent(
                        message_text="<b>Пожалуйста, попросите настроить чат отзывов</b>",
                        parse_mode='HTML'
                    ),
                    reply_markup=kb.DEV
                )


            await query.answer(results=[result1, result2], cache_time=0, is_personal=True)

        else:
            if reviews:
                kb2 = kb.deal_end(reviews)
                result = InlineQueryResultArticle(
                    id="None",
                    title=f"Сделка завершена с {query.query}",
                    description=f"Сделка завершена с {query.query}",
                    input_message_content=InputTextMessageContent(
                        message_text=f"Сделка завершена!\nСпасибо за сделку, можете оставить отзыв по кнопке снизу\n\n{query.query}",
                        parse_mode='HTML'
                    ),
                    reply_markup=kb2
                )
            else:
                result = InlineQueryResultArticle(
                    id="None",
                    title="Отзывы не найдены",
                    description=f"Чат отзывов не настроен",
                    input_message_content=InputTextMessageContent(
                        message_text="<b>Пожалуйста, попросите настроить чат отзывов</b>",
                        parse_mode='HTML'
                    ),
                    reply_markup=kb.DEV
                )

            await query.answer(results=[result], cache_time=0, is_personal=True)


@router.chosen_inline_result()
async def chosen_inline_result(result: ChosenInlineResult, bot: Bot):
    if result.result_id.startswith("num_"):
        uid = result.result_id.split("_")[1]

        verification = mdb.get_user_verification(user_id=result.from_user.id)
        addresses = mdb.get_user_addresses(user_id=result.from_user.id)
        norm_addresses = normalize_addresses(addresses=addresses)

        last_time = await get_last_lime(address=addresses[0])

        text = (f"<tg-emoji emoji-id='5195322003225057603'>😀</tg-emoji> Верификация: {verification}\n\n"
                 f"Сумма: <code>{float(result.query)}</code> TON\n\n"
                 f"<tg-emoji emoji-id={EXCLAMATION_MARK}>❗️</tg-emoji>ID платежа: <code>{uid}</code>\n"
                 f"Просьба указать ID Платежа в комментарии платежа (автоматически через кнопки ниже)\n\n"
                f"<b>Мои адреса:\n\n</b>"
                f"{norm_addresses}\n\n"
                f"Также можете отправить деньги быстро через кнопку ниже:")

        markup = kb.inline_query(uid=uid, address=addresses[0], amount=float(result.query))

        await bot.edit_message_text(text=text, inline_message_id=result.inline_message_id, reply_markup=markup)

        mdb.write_invoice(uid, float(result.query), last_time=last_time, address=addresses[0], username=result.from_user.username)

    elif result.result_id.startswith("without_"):
        verification = mdb.get_user_verification(user_id=result.from_user.id)
        addresses = mdb.get_user_addresses(user_id=result.from_user.id)
        norm_addresses = normalize_addresses(addresses=addresses)

        text = (f"<tg-emoji emoji-id='5195322003225057603'>😀</tg-emoji> Верификация: {verification}\n\n"
                f"<b>Мои адреса:\n\n</b>"
                f"{norm_addresses}\n\n"
                f"Также можете отправить деньги быстро через кнопку ниже:")

        markup = kb.inline_query(address=addresses[0])

        await bot.edit_message_text(text=text, inline_message_id=result.inline_message_id, reply_markup=markup)



@router.callback_query(F.data.startswith("optimize_"))
async def optimize_(call: CallbackQuery):
    await call.answer('Странно🤔')
    return


@router.callback_query(F.data.startswith("check_"))
async def call_check_(call: CallbackQuery, bot: Bot):
    call_data = call.data.split("_")
    uid = call_data[1]
    amount = int(float(call_data[2]))

    dates = mdb.get_invoice_dates(uid) # (invoice_id, amount, last_time, address, username)

    transaction_hash = await check_transaction(dates[3], last_time=dates[2], amount=dates[1], uid=dates[0])

    if not transaction_hash:
        await call.answer("Ничего не найдено")
        return

    text = (f"<tg-emoji emoji-id='5206607081334906820'>✅</tg-emoji>{amount/1_000_000_000} TON <a href='https://tonscan.org/tx/{transaction_hash}'>получено</a>!\n\n"
            f"ID платежа: <code>{uid}</code>")

    markup = kb.get_final_kbs(transaction_hash)

    await bot.edit_message_text(text=text, reply_markup=markup, inline_message_id=call.inline_message_id)

    text = f"Кому: {dates.get('username')}\n\n" + text

    log_message = await bot.send_message(chat_id=LOGS, text=text, reply_markup=markup)

    if amount/1_000_000_000 >= 100.0:
        await bot.pin_chat_message(chat_id=LOGS, message_id=log_message.message_id)




@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    text = ("Привет\n"
            "Выберите действие:")

    markup = kb.main_menu()

    await message.answer(text="Бот создается...", reply_markup=kb.DEV)


@router.callback_query(F.data == "manage_addresses")
async def call_manage_addresses(call: CallbackQuery, state: FSMContext):
    addresses = mdb.get_user_addresses_all(call.from_user.id)

    text = (f"Лимит: {len(addresses)}/1"
            f"Ваши адреса:")

