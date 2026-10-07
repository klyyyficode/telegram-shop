from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_slider_kb(current_index: int, max_index: int, item_id: int):
    prev_index = current_index - 1
    next_index = current_index + 1

    nav_buttons = []
    if prev_index >= 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"page_{prev_index}"))
    if next_index <= max_index:
        nav_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"page_{next_index}"))

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            nav_buttons,
            [InlineKeyboardButton(text="🛒 В корзину", callback_data=f"buy_{item_id}")]
        ]
    )
    return keyboard