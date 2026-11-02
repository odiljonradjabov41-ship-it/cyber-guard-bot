# handlers/report.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import aiosqlite
from database import DB_NAME

router = Router()

class ReportScamState(StatesGroup):
    waiting_for_details = State()

@router.callback_query(F.data == "report_scam")
async def ask_for_scam_details(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🚨 **Firibgarlik haqida xabar berish**\n\n"
        "Iltimos, firibgarlar haqidagi ma'lumotlarni yuboring:\n"
        "• Soxta havolalar\n"
        "• Firibgarning bank karta raqami yoki telefon raqami\n"
        "• Yoki qanday aldashgani haqida qisqacha matn\n\n"
        "Ma'lumotlar boshqa vatandoshlarimizni ogohlantirish uchun bazaga kiritiladi:",
        parse_mode="Markdown"
    )
    await state.set_state(ReportScamState.waiting_for_details)
    await callback.answer()

@router.message(ReportScamState.waiting_for_details)
async def process_scam_report(message: Message, state: FSMContext):
    report_text = message.text.strip()
    user_id = message.from_user.id

    # Bazaga saqlash
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO scam_reports (user_id, report_text) VALUES (?, ?)",
            (user_id, report_text)
        )
        await db.commit()

    await message.answer(
        "✅ **Rahmat! Xabaringiz bazaga saqlandi.**\n\n"
        "Siz taqdim etgan ma'lumot boshqa vatandoshlarimizni ogohlantirish uchun qo'shildi. "
        "Birgalikda kiberxavfsizlikni ta'minlaymiz! 🛡",
        parse_mode="Markdown"
    )
    await state.clear()