import random
import string

def generate_transaction_linking_code(first_char: str, second_char: str) -> str:
    '''INPUT DESCRIPTION:
    first_char: [B, S] where B stands for BUY and S stands for SELL
    second_char: [I, S] where I stands for INVESTMENT and S stands for STANDARD
    '''

    return first_char + second_char + '#' + ''.join(random.choices(string.digits, k = 10))