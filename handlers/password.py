# handlers/password.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import re

router = Router()

class PasswordCheckState(StatesGroup):
    waiting_for_password = State()

@router.callback_query(F.data == "check_password")
async def ask_password(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🔐 **Parol mustahkamligini tekshirish**\n\n"
        "Tekshirmoqchi bo'lgan parolingizni yuboring:\n"
        "*(Eslatma: Shaxsiy asosiy parollaringizni yubormang, shunchaki o'xshash namuna yuboring!)*"
    )
    await state.set_state(PasswordCheckState.waiting_for_password)
    await callback.answer()

@router.message(PasswordCheckState.waiting_for_password)
async def process_password(message: Message, state: FSMContext):
    pwd = message.text.strip()
    score = 0
    feedback = []

    if len(pwd) >= 8: score += 1
    else: feedback.append("❌ Uzunligi kamida 8 ta belgidan iborat bo'lishi kerak.")

    if re.search(r"[A-Z]", pwd) and re.search(r"[a-z]", pwd): score += 1
    else: feedback.append("❌ Katta va kichik harflar qatnashishi kerak.")

    if re.search(r"\d", pwd): score += 1
    else: feedback.append("❌ Raqamlar qatnashishi kerak.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd): score += 1
    else: feedback.append("❌ Maxsus belgilar (!@#$...) qatnashishi kerak.")

    if score == 4:
        result = "🟢 **Juda kuchli parol!** Superkompyuterlar ham buni topishi juda qiyin."
    elif score >= 2:
        result = "🟡 **O'rtacha darajadagi parol.** Xavfsizlikni oshirish uchun maxsus belgilar qo'shing."
    else:
        result = "🔴 **Juda zaif parol!** Uni bir necha soniyada buzib ochish mumkin."

    response = f"{result}\n\n" + ("\n".join(feedback) if feedback else "✅ Barcha talablar bajarilgan!")
    await message.answer(response, parse_mode="Markdown")
    await state.clear()