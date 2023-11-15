from prompt_toolkit.completion import NestedCompleter
from .service_addressbook import FUNCTIONS, EXIT
from .servicenote import OPERATORS


COMMANDS = {}
COMMANDS.update(EXIT)
COMMANDS.update(OPERATORS)
COMMANDS.update(FUNCTIONS)

def func_completer(COMMANDS: dict):
    comp_dict = {}
    sorted_comand = sorted(COMMANDS.keys())
    for key in sorted_comand[1:]:
        words = key.split()
        first_word = words[0]  
        rest_of_key = ' '.join(words[1:]) if len(words) > 1 else None
        if first_word not in comp_dict:
            comp_dict[first_word] = {rest_of_key} if rest_of_key else None
        else:
            if rest_of_key:
                if comp_dict[first_word] is None:
                    comp_dict[first_word] = {rest_of_key}
                else:
                    comp_dict[first_word].add(rest_of_key)
            else:
                comp_dict[first_word] = None
    return comp_dict



completer = NestedCompleter.from_nested_dict(func_completer(COMMANDS))

if __name__ == '__main__':
    print(func_completer(COMMANDS))

    