"""
When the call_api is running, you can run other tasks. For example,
the following program displays a message every second while waiting
for the call_api tasks:
"""

import asyncio
import logging
import time


async def call_api(message, result=1000, delay=6):
    logging.info(message)
    await asyncio.sleep(delay)
    return result


async def show_message():
    for _ in range(5):
        await asyncio.sleep(1)
        logging.info("API call is in progress...")


async def main():
    start = time.perf_counter()

    message_task = asyncio.create_task(
        show_message(),
    )

    task_1 = asyncio.create_task(
        call_api("Get stock price of GOOG...", 300),
    )

    task_2 = asyncio.create_task(
        call_api("Get stock price of APPL...", 700),
    )

    price = await task_1
    logging.info(price)

    price = await task_2
    logging.info(price)

    await message_task

    end = time.perf_counter()
    msg = f"It took {round(end-start,0)} second(s) to complete."
    logging.info(msg)


if __name__ == "__main__":
    asyncio.run(main())
