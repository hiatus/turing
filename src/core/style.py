import colorama
from colorama import Fore, Style


# Messages
def print_msg(msg: str):
    print(f'{Fore.LIGHTBLACK_EX}[{Style.RESET_ALL}.{Fore.LIGHTBLACK_EX}]{Style.RESET_ALL} {msg}')


# Successes
def print_scs(err: str):
    print(f'{Fore.LIGHTBLACK_EX}[{Fore.GREEN}+{Fore.LIGHTBLACK_EX}]{Style.RESET_ALL} {err}')


# Errors
def print_err(err: str):
    print(f'{Fore.LIGHTBLACK_EX}[{Fore.RED}-{Fore.LIGHTBLACK_EX}]{Style.RESET_ALL} {err}')


# Exceptions
def print_exc(exc: Exception):
    print(f'{Fore.LIGHTBLACK_EX}[{Fore.RED}!{Fore.LIGHTBLACK_EX}]{Style.RESET_ALL} {exc}')


colorama.init()