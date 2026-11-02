# handlers/blacklist.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import aiosqlite
from config import DB_NAME

router = Router()

class BlacklistState(StatesGroup):
    waiting_for_query = State()

@router.callback_query(F.data == "check_blacklist")
async def ask_blacklist(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🕵️‍♂️ **Qora ro'yxatdan qidirish**\n\n"
        "Tekshirmoqchi bo'lgan **karta raqamini** (16 xonali) yoki **telefon raqamini** yuboring:"
    )
    await state.set_state(BlacklistState.waiting_for_query)
    await callback.answer()

@router.message(BlacklistState.waiting_for_query)
async def process_blacklist_search(message: Message, state: FSMContext):
    query = message.text.strip()
    
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT created_at FROM blacklist WHERE identifier = ?;", (query,)) as cursor:
            result = await cursor.fetchone()

    if result:
        await message.answer(
            f"⚠️ **DIQQAT! BU RAQAM QORA RO'YXATDA BOR!** 🔴\n\n"
            f"Kiritilgan raqam: `{query}`\n"
            f"Ro'yxatga kiritilgan vaqti: `{result[0]}`\n\n"
            "Bu raqam egasi oldin firibgarlikda gumon qilingan. Ehtiyot bo'ling!",
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            f"✅ **Toza.**\n\n"
            f"`{query}` raqami bo'yicha qora ro'yxatda shikoyatlar topilmadi. Lekin har doim hushyor bo'ling!",
            parse_mode="Markdown"
        )
    await state.clear()