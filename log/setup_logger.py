import logging

logging.basicConfig(level=logging.DEBUG)
handler = logging.FileHandler(filename="./logfile.log")
format = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")

handler.setFormatter(format)

logger = logging.getLogger("WP")
logger.addHandler(handler)




