# database.py
import aiosqlite

DB_NAME = "cyber_guard.db"

async def create_pool():
    return DB_NAME

async def init_db(db_path):
    async with aiosqlite.connect(db_path) as db:
        # Foydalanuvchilar (Xavfsizlik bali va til sozlamasi bilan)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                full_name TEXT,
                username TEXT,
                language TEXT DEFAULT 'uz',
                points INTEGER DEFAULT 0,
                security_score INTEGER DEFAULT 50,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Firibgarlik xabarlari
        await db.execute("""
            CREATE TABLE IF NOT EXISTS scam_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                report_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Qora ro'yxat
        await db.execute("""
            CREATE TABLE IF NOT EXISTS blacklist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                identifier TEXT UNIQUE,
                category TEXT, 
                status TEXT DEFAULT 'approved',
                reported_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Kiber-yangiliklar
        await db.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        await db.commit()
    print("📊 Barcha Premium jadvallar va Security Score bazaga qo'shildi!")