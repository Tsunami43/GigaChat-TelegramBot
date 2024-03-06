if __name__ == "__main__":
    import logging
    import data
    data.init()

    # logging.basicConfig(level=logging.INFO, filename='main.log', filemode="w",
    #                   format="%(asctime)s - [%(levelname)s] -  %(name)s - " +
    #                           "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s \n")
    logging.basicConfig(level=logging.INFO)

    import asyncio
    from bot import bot

    asyncio.run(bot.run())