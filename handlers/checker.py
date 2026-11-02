# handlers/checker.py
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import aiohttp
import base64
import re
from config import VIRUSTOTAL_API_KEY

router = Router()

class CheckLinkState(StatesGroup):
    waiting_for_link = State()

@router.callback_query(F.data == "check_link")
async def ask_for_link(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🔗 Iltimos, tekshirmoqchi bo‘lgan **havolani (sayt manzilini)** yuboring:\n\n"
        "*(Masalan: https://example.com)*"
    )
    await state.set_state(CheckLinkState.waiting_for_link)
    await callback.answer()

@router.message(CheckLinkState.waiting_for_link)
async def process_link(message: Message, state: FSMContext):
    url = message.text.strip()
    
    url_pattern = re.compile(r'https?://[^\s]+')
    if not url_pattern.match(url):
        await message.answer("❌ Bu haqiqiy havola (URL) formatiga o'xshamaydi. Iltimos, `https://` bilan boshlanuvchi to'g'ri manzil yuboring:")
        return

    wait_msg = await message.answer("🔍 Havola xalqaro kiberxavfsizlik bazalari (VirusTotal) orqali tekshirilmoqda, iltimos kuting...")

    try:
        # VirusTotal v3 API orqali URL'ni tekshirish
        headers = {
            "x-apikey": VIRUSTOTAL_API_KEY,
            "accept": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            # 1. URL'ni base64 ga o'tkazib tekshiruvga yuboramiz
            url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
            async with session.get(f"https://www.virustotal.com/api/v3/urls/{url_id}", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    stats = data["data"]["attributes"]["last_analysis_stats"]
                    malicious = stats.get("malicious", 0)
                    suspicious = stats.get("suspicious", 0)
                    
                    if malicious > 0 or suspicious > 0:
                        result_text = (
                            f"⚠️ **DIQQAT! XAVFLI SAYT ANIQLANDI!** 🔴\n\n"
                            f"Siz yuborgan havola: `{url}`\n\n"
                            f"• Xavfsizlik kompaniyalari xavfli deb topdi: `{malicious}` ta\n"
                            f"• Shubhali deb topildi: `{suspicious}` ta\n\n"
                            "Bu fishing yoki virusli sayt bo'lishi mumkin. Unga kirmang!"
                        )
                    else:
                        result_text = (
                            f"✅ **Tahlil natijasi (Xavfsiz):**\n\n"
                            f"Siz yuborgan havola: `{url}`\n\n"
                            "VirusTotal bazasida hech qanday tahdid yoki qoidabuzarlik topilmadi."
                        )
                else:
                    result_text = (
                        f"✅ **Tahlil natijasi:**\n\n"
                        f"Siz yuborgan havola: `{url}`\n\n"
                        "Havola format bo'yicha to'g'ri, lekin tizimda chuqur ma'lumot topilmadi. Ehtiyotkor bo'ling!"
                    )
        
        await wait_msg.edit_text(result_text, parse_mode="Markdown")
    except Exception as e:
        await wait_msg.edit_text(f"⚠️ Tekshirish vaqtida xatolik yuz berdi. Iltimos keyinroq urinib ko'ring.")
    
    await state.clear()