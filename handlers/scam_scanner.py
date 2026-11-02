# handlers/scam_scanner.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()

class ScamTextState(StatesGroup):
    waiting_for_text = State()

@router.callback_query(F.data == "scan_text")
async def ask_scam_text(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "📝 **Shubhali SMS / Matn Analizatori**\n\n"
        "Sizga kelgan shubhali SMS, Telegram xabari yoki va'dani shu yerga nusxalab yuboring. Men uni firibgarlikka tekshirib beraman:"
    )
    await state.set_state(ScamTextState.waiting_for_text)
    await callback.answer()

@router.message(ScamTextState.waiting_for_text)
async def process_scam_text(message: Message, state: FSMContext):
    text = message.text.lower()
    
    # Firibgarlikka xos kalit so'zlar
    danger_keywords = ["yutuq", "karta raqami", "sms kod", "sovg'a", "aksiyada yutdingiz", "shoshiling", "tasdiqlang", "olg'", "100%", "bonus"]
    found_matches = [kw for kw in danger_keywords if kw in text]

    if len(found_matches) >= 2:
        response = (
            "🚨 **YUQORI XAVF! BU FIRIBGARLIK (SCAM) BO'LISH EHTIMOLI 95%!** 🔴\n\n"
            f"Matnda topilgan xavfli so'zlar: `{' , '.join(found_matches)}`\n\n"
            "⚠️ **Tavsiya:** Hech qachon shaxsiy ma'lumotlaringiz yoki kodlarni bermang!"
        )
    elif len(found_matches) == 1:
        response = (
            "⚠️ **DIQQAT! Shubhali belgi aniqlandi.** 🟡\n\n"
            f"Matnda ehtiyotkorlikni talab qiluvchi so'z topildi: `{found_matches[0]}`.\n"
            "Hushyor bo'ling va noma'lum havolalarga kirmang."
        )
    else:
        response = (
            "✅ **Toza ko'rinadi.**\n\n"
            "Bu matnda aniq firibgarlik belgilari topilmadi. Shunda ham har doim ehtiyotkor bo'ling!"
        )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_main")]]
    )
    await message.answer(response, reply_markup=keyboard, parse_mode="Markdown")
    await state.clear()