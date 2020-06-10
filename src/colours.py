class tCol:
    # ANSII Colours.
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod # Returns a colour formatted string (PURPLE).
    def header(m):  return tCol.HEADER + m + tCol.ENDC

    @staticmethod # Returns a colour formatted string (BLUE).
    def okblue(m):  return tCol.OKBLUE + m + tCol.ENDC

    @staticmethod # Returns a colour formatted string (GREEN).
    def okgreen(m): return tCol.OKGREEN + m + tCol.ENDC

    @staticmethod # Returns a colour formatted string (YELLOW).
    def warning(m): return tCol.WARNING + m + tCol.ENDC

    @staticmethod # Returns a colour formatted string (RED).
    def fail(m):    return tCol.FAIL + m + tCol.ENDC 
