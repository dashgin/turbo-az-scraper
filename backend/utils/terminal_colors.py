
class BColors:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    DARK_GRAY = '\033[90m'
    FAIL = '\033[91m'
    CYAN = '\033[36m'
    ORANGE = '\033[33m'
    END = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OK_BLUE = ''
        self.OK_GREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.END = ''
