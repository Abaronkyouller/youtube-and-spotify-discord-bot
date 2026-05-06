import aiosqlite

DB_NAME = "stocks.db"

async def setup_database():
    async with aiosqlite.connect(DB_NAME) as db:

        # Users table
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            balance INTEGER DEFAULT 10000
        )
        """)

        # Stocks table
        await db.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            stock_name TEXT PRIMARY KEY,
            price REAL
        )
        """)

        # Portfolio table
        await db.execute("""
        CREATE TABLE IF NOT EXISTS portfolio (
            user_id INTEGER,
            stock_name TEXT,
            shares INTEGER,
            PRIMARY KEY(user_id, stock_name)
        )
        """)

        await db.commit()

async def seed_stocks():
    stocks = [
        ("APPLE", 100),
        ("MEME", 50),
        ("DOGE", 25),
        ("SPACE", 75)
    ]

    async with aiosqlite.connect(DB_NAME) as db:
        for stock in stocks:
            await db.execute("""
            INSERT OR IGNORE INTO stocks(stock_name, price)
            VALUES (?, ?)
            """, stock)

        await db.commit()