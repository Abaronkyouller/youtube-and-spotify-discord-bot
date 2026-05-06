import random
import aiosqlite
from database import DB_NAME

async def update_market():

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            "SELECT stock_name, price FROM stocks"
        )

        stocks = await cursor.fetchall()

        for stock_name, price in stocks:

            # Random change between -10% and +10%
            change_percent = random.uniform(-0.10, 0.10)

            new_price = round(
                price * (1 + change_percent),
                2
            )

            # Prevent stock going below 1
            new_price = max(new_price, 1)

            await db.execute("""
            UPDATE stocks
            SET price = ?
            WHERE stock_name = ?
            """, (new_price, stock_name))

        await db.commit()