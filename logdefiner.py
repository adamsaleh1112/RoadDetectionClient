from datetime import datetime

now = datetime.now()
dt_string = str(now.strftime("%d_%m_%Y"))
filename = str(dt_string + ".txt")


def get_log_name():
    return filename
