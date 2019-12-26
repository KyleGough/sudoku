class tCol:
    # ANSII Colours.
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    # Returns a colour formatted string.
    @staticmethod
    def header(m):  return tCol.HEADER + m + tCol.ENDC
    @staticmethod
    def okblue(m):  return tCol.OKBLUE + m + tCol.ENDC
    @staticmethod
    def okgreen(m): return tCol.OKGREEN + m + tCol.ENDC
    @staticmethod
    def warning(m): return tCol.WARNING + m + tCol.ENDC
    @staticmethod
    def fail(m):    return tCol.FAIL + m + tCol.ENDC 
