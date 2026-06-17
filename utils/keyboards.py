from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

primary = "primary" # синяя
success = "success" # зеленая
danger = "danger" # красная



TONKEEPER: str = '5294333888594745603'
TONKEEPER2: str = '5293996089416920903'
MYTONWALLET: str = '5294519010275139511'
GRAM: str = '5294018882808357195'
TONHUB: str = '5294154784163534709'
CHECK: str = '5294289594597022399'



def ib(
    text: str,
    callback_data: str = None,
    url: str = None,
    emoji_id: str = None,
    style: str = None,
) -> InlineKeyboardButton:
    """Создаёт InlineKeyboardButton с опциональным premium emoji и style."""
    kwargs = dict(text=text)
    if callback_data:
        kwargs["callback_data"] = callback_data
    if url:
        kwargs["url"] = url
    if emoji_id:
        kwargs["icon_custom_emoji_id"] = emoji_id
    if style:
        kwargs["style"] = style
    return InlineKeyboardButton(**kwargs)



DEV = InlineKeyboardMarkup(inline_keyboard=[[ib(text='Dev', url="https://t.me/TheAnotherOneUsername", style=success)]])



def inline_query(address: str, uid: str = None, amount: float = None, jetton: str = None) -> InlineKeyboardMarkup:
    if amount:
        amount = int(amount*1_000_000_000)

    markup = InlineKeyboardBuilder()
    markup.row(ib(text='Tonkeeper', url=f"https://app.tonkeeper.com/transfer/{address}?{f'amount={amount}' if amount else ''}{f'&text={uid}' if uid else ''}{f'&jetton={jetton}' if jetton else ''}", emoji_id=TONKEEPER, style=primary), ib(text='MyTonWallet', url=f"https://my.tt/transfer/{address}?{f'amount={amount}' if amount else ''}{f'&text={uid}' if uid else ''}{f'&jetton={jetton}' if jetton else ''}", emoji_id=MYTONWALLET, style=primary))
    markup.row(ib(text='Tonhub', url=f"https://tonhub.com/transfer/{address}?{f'amount={amount}' if amount else ''}{f'&text={uid}' if uid else ''}{f'&jetton={jetton}' if jetton else ''}", emoji_id=TONHUB, style=primary), ib(text='Другие', url=f"ton://transfer/{address}?{f'amount={amount}' if amount else ''}{f'&text={uid}' if uid else ''}{f'&jetton={jetton}' if jetton else ''}", emoji_id=GRAM, style=primary))
    if amount:
        markup.row(ib(text='Проверить', callback_data=f"check_{uid}_{amount}", style=success, emoji_id=CHECK))

    return markup.as_markup()


def optimize(uid: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    markup.row(ib(text='Долго не создается🤔', callback_data=f"optimize_{uid}", style=success))
    return markup.as_markup()


def get_final_kbs(transaction_hash: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    markup.row(ib(text='TON Scan', url=f"https://tonscan.org/tx/by-msg-hash/{transaction_hash}", style=primary), ib(text='TON Viewer', url=f"https://tonviewer.com/transaction/{transaction_hash}", style=primary))
    return markup.as_markup()



def main_menu() -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    markup.row(ib(text='Настроить адреса', callback_data='manage_addresses', style=primary))
    markup.row(ib(text='Премиум', callback_data='premium', style=success))
    markup.row(ib(text='Верификация', callback_data='verification', style=danger))

    return markup.as_markup()


def manage_addresses():
    pass


def deal_end(reviews: str):
    markup = InlineKeyboardBuilder()
    markup.row(ib(text='Оставить отзыв', url=reviews, style=success))

    return markup.as_markup()