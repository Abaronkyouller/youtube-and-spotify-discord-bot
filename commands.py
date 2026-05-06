import aiosqlite
from database import DB_NAME

async def buy_stock(user_id, stock_name, amount):

    async with aiosqlite.connect(DB_NAME) as db:

        # Get stock price
        cursor = await db.execute(
            "SELECT price FROM stocks WHERE stock_name = ?",
            (stock_name,)
        )

        stock = await cursor.fetchone()

        if not stock:
            return "Stock does not exist."

        price = stock[0]
        total_cost = price * amount

        # Get user balance
        cursor = await db.execute(
            "SELECT balance FROM users WHERE user_id = ?",
            (user_id,)
        )

        user = await cursor.fetchone()

        if not user:
            await db.execute(
                "INSERT INTO users(user_id, balance) VALUES (?, ?)",
                (user_id, 10000)
            )

            balance = 10000
        else:
            balance = user[0]

        if balance < total_cost:
            return "Not enough money."

        # Deduct money
        await db.execute(
            "UPDATE users SET balance = balance - ? WHERE user_id = ?",
            (total_cost, user_id)
        )

        # Add shares
        await db.execute("""
        INSERT INTO portfolio(user_id, stock_name, shares)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, stock_name)
        DO UPDATE SET shares = shares + ?
        """, (user_id, stock_name, amount, amount))

        await db.commit()

        return f"Bought {amount} shares of {stock_name}"