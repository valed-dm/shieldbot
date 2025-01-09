"""
Example of running a blocking function call in asyncio.
This highlights that a blocking function call in a coroutine or task
will not suspend and will block the entire event loop:

1. task is running
2. task is done
3. >background task running


1. >background task running
2. task is running
3. >background task running
4. >background task running
5. >background task running
6. task is done
"""

import asyncio
import logging
import time

logger = logging.getLogger(__name__)


# blocking function
def blocking_task():
    # report a message
    logger.info("task is running")
    # block
    time.sleep(2)
    # report a message
    logger.info("task is done")


# background coroutine task
async def background():
    # loop forever
    while True:
        # report a message
        logger.info(">background task running")
        # sleep for a moment
        await asyncio.sleep(0.5)


# main coroutine
async def main_blocking():
    # run the background task
    _ = asyncio.create_task(background())  # noqa: RUF006
    # execute the blocking call
    blocking_task()


async def main():
    # run the background task
    _ = asyncio.create_task(background())  # noqa: RUF006
    # create a coroutine for the blocking function call
    coro = asyncio.to_thread(blocking_task)
    # execute the call in a new thread and await the result
    await coro


if __name__ == "__main__":
    asyncio.run(main())
