import tiktoken
from IPython.display import clear_output


def tokenization(data):
    tokenizer = tiktoken.get_encoding("cl100k_base")
    color_codes = ['0;47', '0;42', '0;43', '0;44', '0;46', '0;45']

    user_input = data

    encoded = tokenizer.encode(user_input)
    decoded = tokenizer.decode_tokens_bytes(encoded)
    token_list = [token.decode() for token in decoded]

    character_count = sum(len(i) for i in token_list)

    for idx, token in enumerate(token_list):
        print(f'\x1b[{color_codes[idx % len(color_codes)]};1m{token}\x1b[0m', end='')

    color_sheme = ("\n\n" + str(token_list) + "\n")
    encoded = (str(encoded) + "\n")
    Token_Count =("Token Count: " + str(len(encoded)))
    Character_Count = ("Characters: " + str(character_count))
    return color_sheme,encoded,Token_Count,Character_Count



