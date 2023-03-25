import datetime


# Information
def i():
    return '\033[37mI \033[0m' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# Warning
def w():
    return '\033[33mW \033[0m' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# Error
def e():
    return '\033[31mE \033[0m' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# Success
def s():
    return '\033[32mS \033[0m' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
