from .servicenote import OPERATORS
from .service_addressbook import FUNCTIONS, EXIT
from .terminal_tips import completer
from prompt_toolkit import prompt


COMMANDS = {}
COMMANDS.update(EXIT)
COMMANDS.update(OPERATORS)
COMMANDS.update(FUNCTIONS)
COMMANDS = dict(sorted(COMMANDS.items(), reverse=True))


def parser(text: str):
    for func in COMMANDS.keys():
        if text.startswith(func):
            return func, text[len(func) :].strip().split()


def main():
    while True:
        user_input = prompt(">>>", completer=completer, mouse_support=True)
        func, data = parser(user_input.lower())
        current_func = COMMANDS.get(func)
        print(current_func(*data))


if __name__ == "__main__":
    main()
