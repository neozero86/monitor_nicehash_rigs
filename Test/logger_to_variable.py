from Main.logger import Logger


class LoggerToVariable(Logger):

    def __init__(self, info_list, debug_list, error_list):
        self.info_list = info_list
        self.debug_list = debug_list
        self.error_list = error_list

    def info(self, msg):
        #print("info: {}".format(msg))
        self.info_list.append(msg)

    def debug(self, msg):
        #print("debug: {}".format(msg))
        self.debug_list.append(msg)

    def error(self, msg):
        #print("error: {}".format(msg))
        self.error_list.append(msg)