from addressbook import Record, AddressBook
from datetime import datetime
import re
from mainnote import OPERATORS
file_name = "book.bin"
book = AddressBook()
book.load(file_name)


def user_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough params. Use help."
        except KeyError:
            return "Unknown rec_id. Try another or use help."
        except ValueError:
            return "Unknown or wrong format. Check phone and/or birthday"
        except AttributeError:
            return "Contacts was not found"

    return inner


def func_normalize_phone(phone):
    new_phone = (
        phone.strip()
        .removeprefix("+38")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace(" ", "")
    )

    return new_phone


@user_error
def func_add(*args):
    rec_id = args[0].lower()
    phone = args[1]
    new_phone = func_normalize_phone(phone)
    new_record = Record(rec_id)
    new_record.add_phone(new_phone)

    if rec_id in book.keys():
        return f"Record alredy exist"
    elif new_phone == None:
        return f"Check the phone: {phone}. Wrong format."

    if len(args) == 3:
        new_birthday = datetime(
            year=int(args[2][6:]), month=int(args[2][3:5]), day=int(args[2][:2])
        )
        contact_birtday = new_birthday.date().strftime("%d %B %Y")
        new_record.add_birthday(new_birthday)
        book[rec_id] = new_record
        return f"Add record {rec_id = }, {new_phone = }, {contact_birtday = }"

    book[rec_id] = new_record
    return f"Add record {rec_id = }, {new_phone = }"


@user_error
def func_change(*args):
    rec_id = args[0].lower()
    old_phone = func_normalize_phone(args[1])
    new_phone = func_normalize_phone(args[2])

    if old_phone == None:
        return f"Check the phone: {args[1]}. Wrong format."
    if new_phone == None:
        return f"Check the phone: {args[2]}. Wrong format."

    book.find(rec_id).edit_phone(old_phone, new_phone)
    return f"Record {rec_id} is updated with nes phone: {book.get(rec_id).phones[0]}"


@user_error
def func_phone(*args):
    rec_id = args[0]
    return f"Phone of {rec_id} is {book.get(rec_id).phones[0]}"


def func_hello(*args):
    return f"How can I help you?"


def func_show_all(*args):
    if len(book) == 0:
        return f"Your contacts list is empty"
    line = ""
    for record in book.values():
        line += f"{record}\n"
    return line


def func_show(*args):
    if len(book) == 0:
        return f"Your contacts list is empty"
    stop = int(args[0])
    line = ""
    for rec in book.iterator(stop):
        line += rec
    return line


def func_find(*args):
    line = ""
    for record in book.values():
        str_rec = str(record.name)
        for ph in record.phones:
            str_rec += str(ph)
        found_rec = re.findall(args[0], str_rec)
        if len(found_rec) != 0:
            line += f"{record}\n"

    if len(line) == 0:
        return f'the search for key "{args[0]}" gave no results. Try other key.'
    print(f'result for "{args[0]}" search:')
    return line


def func_remove(*args):
    rec_id = args[0]
    book.delete(rec_id)
    return f"Contact {rec_id} succesfully removed"


def unknown(*args):
    return "Unknown command. Try again."


def func_good_bye(*args):
    book.save(file_name)
    print(f"Good bye!")
    exit()


FUNCTIONS = {
    "hello": func_hello,
    "add": func_add,
    "change": func_change,
    "phone": func_phone,
    "show all": func_show_all,
    "show": func_show,
    "find": func_find,
    "good bye": func_good_bye,
    "close": func_good_bye,
    "exit": func_good_bye,
    "remove": func_remove,
    "": func_good_bye,
}


def parser(text: str):
    for func in OPERATORS.keys():
        if text.startswith(func):
            return func, text[len(func) :].strip().split()
        
    for func in FUNCTIONS.keys():
        if text.startswith(func):
            return func, text[len(func) :].strip().split()
    

def main():
    while True:
        user_input = input(">>>")
        func, data = parser(user_input.lower())
        if func in FUNCTIONS:
            current_func = FUNCTIONS.get(func)
            print(current_func(*data))
        elif func in OPERATORS:
            current_func = OPERATORS.get(func)
            print(current_func(*data))

if __name__ == "__main__":
    main()
