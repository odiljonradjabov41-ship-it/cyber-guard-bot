# bot.py
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database import create_pool, init_db

# Handlerlarni to'g'ridan-to'g'ri o'z papkasidan alohida import qilamiz
from handlers.start import router as start_router
from handlers.ai_consultant import router as ai_router
from handlers.checker import router as checker_router
from handlers.scam_scanner import router as scam_router
from handlers.premium_tools import router as premium_router
from handlers.security_tools import router as security_router
from handlers.leaderboard import router as leaderboard_router
from handlers.report import router as report_router
from handlers.password import router as password_router
from handlers.blacklist import router as blacklist_router
from handlers.school import router as school_router
from handlers.admin import router as admin_router
from handlers.help import router as help_router

async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    try:
        db_path = await create_pool()
        await init_db(db_path)
        dp["db_path"] = db_path
    except Exception as e:
        print(f"⚠️ Ma'lumotlar bazasiga ulanishda xatolik: {e}")

    # Barcha routerlarni ulaymiz
    dp.include_router(start_router)
    dp.include_router(ai_router)
    dp.include_router(checker_router)
    dp.include_router(scam_router)
    dp.include_router(premium_router)
    dp.include_router(security_router)
    dp.include_router(leaderboard_router)
    dp.include_router(report_router)
    dp.include_router(password_router)
    dp.include_router(blacklist_router)
    dp.include_router(school_router)
    dp.include_router(admin_router)
    dp.include_router(help_router)

    await bot.delete_webhook(drop_pending_updates=True)
    print("🤖 CyberGuard Uzbekistan muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())