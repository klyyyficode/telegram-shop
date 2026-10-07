from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from os import getenv

from keyboards.inline import get_slider_kb
from handlers.shop import items
from forms.state import CheckoutState
 
router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message):
    first_item = items[0]
    max_index = len(items) - 1

    await message.answer(
        f"{first_item['name']}, - {first_item['price']}$",
        reply_markup=get_slider_kb(current_index=0, max_index=max_index, item_id=first_item['id'])
)


@router.callback_query(F.data.startswith("page_"))
async def slider_handler(callback: CallbackQuery):
    new_index = int(callback.data.split("_")[1])
    item = items[new_index]
    max_index = len(items) - 1

    await callback.message.edit_text(
        text=f"{item['name']} - {item['price']}$",
        reply_markup=get_slider_kb(current_index=new_index, max_index=max_index, item_id=item['id'])
    )
    await callback.answer()

@router.callback_query(F.data.startswith("buy_"))
async def buy_item_handler(callback: CallbackQuery, state: FSMContext):
    item_id = int(callback.data.split("_")[1])

    for buy in items:
        if buy['id'] == item_id:
            await state.update_data(item_name=buy['name'], item_price=buy['price'])

            await callback.message.answer(f"🛒Вы выбрали {buy['name']}. \nВведите ваш адрес доставки:")
            await state.set_state(CheckoutState.address)

            await callback.answer()
            break

@router.message(CheckoutState.address)
async def check_address_cmd(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("Отлично! Теперь введите ваш телефон:")

    await state.set_state(CheckoutState.phone)

@router.message(CheckoutState.phone)
async def check_all_cmd(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()

    await message.answer(f"✅Заказ оформлен!\nТовар: {data['item_name']},\nК оплате: {data['item_price']}, \nАдрес: {data['address']}, \nТелефон: {message.text}")

    admin_id = getenv("ADMIN_ID")
    admin_text = f"🚨НОВЫЙ ЗАКАЗ!\n\nПокупатель:{message.from_user.username}\nТовар: {data['item_name']},\nСумма: {data['item_price']}$,\nАдрес: {data['address']}"

    await bot.send_message(chat_id=admin_id, text=admin_text)

    await state.clear()