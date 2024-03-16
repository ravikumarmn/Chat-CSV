import pandas as pd

# Local imports
from .log import logger

def read_excel(file):
    df = pd.read_excel(file)
    logger.info("Loaded {} file.".format(file))
    return df