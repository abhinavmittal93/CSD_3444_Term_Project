import logging


class LogConfig:

    def __init__(self):
        self.filename = 'app.log'
        self.filemode = 'w'
        self.format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.datefmt = '%d-%b-%y %H:%M:%S'
        self.level = logging.DEBUG

    def logger_config(self):
        # Create and configure logger
        logging.basicConfig(filename=self.filename,
                            filemode=self.filemode,
                            format=self.format,
                            datefmt=self.datefmt,
                            level=self.level)

        # Creating an object
        logger = logging.getLogger()

        return logger
