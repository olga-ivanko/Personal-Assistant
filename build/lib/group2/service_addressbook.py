from datetime import datetime
from .birthday_functions import func_birthdays_within_days
from .addressbook import AddressBook, Record
from pathlib import Path
from .servicenote import note_book
from . import help_func
from . import sort
import re


book = AddressBook()
book.load()


def user_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough params. Use help."
        except KeyError:
            return "Unknown rec_id. Try another or use help."
        except ValueError:
            return "Unknown or wrong format. Try again"
        except AttributeError:
            return "Contacts was not found"
        except TypeError: 
            return "Use command help"

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


def unknown(*args):
    return "Unknown command. Try again or use help."


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

    if len(args) >= 2:
        while True:
            user_input = input(
                f"type field to add: \n  email / address / birthday \n type back to save\n"
            ).lower()
            if user_input == "back":
                break
            if user_input == "birthday":
                user = input("Enter birthday: ")
                new_birthday = datetime(
                    year=int(user[6:]), month=int(user[3:5]), day=int(user[:2])
                )
                contact_birthday = new_birthday.date().strftime("%d %B %Y")
                new_record.add_birthday(new_birthday)
                print(
                    f"Birthday {contact_birthday} added to user {new_record.name.value}"
                )
            elif user_input == "email":
                user = input("Enter email: ")
                new_email = user
                new_record.add_email(new_email)
                print(f"Email {new_email} added to user {new_record.name.value}")
            elif user_input == "address":
                user = input("Enter address: ")
                new_address = user
                new_record.add_address(new_address)
                print(f"Address {new_address} added to user {new_record.name.value}")

        book[rec_id] = new_record

    book[rec_id] = new_record
    return f"Record added: \n {new_record}"


@user_error
def func_edit_record(*args):
    rec_id = args[0].lower()
    if not rec_id in book.keys():
        return f"Record do not exist"

    record = book.find(rec_id)
    print(record)
    print(f"type what needs to be changed:\n  phone / email / address / birthday")
    user_input = input("").lower()
    if user_input == "phone":
        print(
            "type next command:\n add phone <new number>\n change <old number> <new number>"
        )
        user_input2 = input("").lower().split()
        if user_input2[0] == "change":
            record.edit_phone(user_input2[1], user_input2[2])
            return f"Record updated as:\n {record}"
        elif " ".join(user_input2[:2]) == "add phone":
            record.add_phone(user_input2[2])
            return f"Record updated as:\n {record}"
        else:
            return unknown()
    elif user_input == "email":
        if record.email.value != "no email":
            print(f"current email is {record.email.value}.")
        user_input2 = input("Print new email:\n").lower().strip()
        record.email.value = user_input2
        return f"Record updated as:\n {record}"
    elif user_input == "address":
        print(f"current addess is {record.address.value}.")
        user_input2 = input("Print new address:\n").lower().strip()
        record.address.value = user_input2
        return f"Record updated as:\n {record}"
    elif user_input == "birthday":
        if record.birthday.value:
            print(f"current birthday is {record.birthday.value}.")
            user_input2 = input("Print new birthday:\n")
            new_birthday = datetime(
                year=int(user_input2[6:]),
                month=int(user_input2[3:5]),
                day=int(user_input2[:2]),
            )
            record.add_birthday(new_birthday)
            return f"Record updated as:\n {record}"
    else:
        return unknown()


@user_error
def add_birthday(*args):
    rec_id = args[0]
    birth = args[1]
    if not rec_id in book:
        return "Not user"
    new_birthday = datetime(
        year=int(birth[6:]), month=int(birth[3:5]), day=int(birth[:2])
    )
    book.find(rec_id).add_birthday(new_birthday)
    return f"Birthday { book.find(rec_id).birthday.value} added to record {rec_id}"


@user_error
def add_email(*args):
    rec_id = args[0]
    email = args[1]
    if not rec_id in book:
        return "Not user"
    book.find(rec_id).add_email(email)
    return f"Email { book.find(rec_id).email.value} added to record {rec_id}"


@user_error
def func_address(*args):
    rec_id = args[0]
    address = args[1]
    if not rec_id in book:
        return "Not user"
    book.find(rec_id).add_address(address)
    return f"Address { book.find(rec_id).address.value} added to record {rec_id}"


@user_error
def func_change_phone(*args):
    rec_id = args[0].lower()
    old_phone = func_normalize_phone(args[1])
    new_phone = func_normalize_phone(args[2])

    if old_phone == None:
        return f"Check the phone: {args[1]}. Wrong format."
    if new_phone == None:
        return f"Check the phone: {args[2]}. Wrong format."

    book.find(rec_id).edit_phone(old_phone, new_phone)
    return f"Record {rec_id} is updated with new phone: {new_phone}"


@user_error
def func_phone(*args):
    rec_id = args[0]
    phones_str = "; ".join(p.value for p in book.get(rec_id).phones)
    return f"Phone(s) of {rec_id}: {phones_str}"


def func_hello(*args):
    return f"How can I help you?"


@user_error
def func_show_all(*args):
    if len(book) == 0:
        return f"Your contacts list is empty"
    line = ""
    for record in book.values():
        line += f"{record}\n"
    return line


@user_error
def func_show(*args):
    if len(book) == 0:
        return f"Your contacts list is empty"
    stop = int(args[0])
    line = ""
    for rec in book.iterator(stop):
        line += rec
    return line


@user_error
def func_find(args):
    if len(args) > 2:
        keyword = "".join(args)
        line = ""
        for record in book.values():
            str_rec = str(record.name)
            str_rec += record.address.value
            str_rec += record.email.value
            for ph in record.phones:
                str_rec += str(ph)
            found_rec = re.findall(keyword, str_rec)
            if len(found_rec) != 0:
                line += f"{record}\n"
        if len(line) == 0:
            return f'the search for key "{keyword}" gave no results. Try other key.'
        print(f'result for "{keyword}" search:')
        return line
    return "Please enter 3 or more symbols for search"


@user_error
def func_remove(*args):
    rec_id = args[0]
    book.delete(rec_id)
    return f"Contact {rec_id} succesfully removed"


def func_sort_folder(*args):
    user_input = input("Enter directory path: ")
    path = Path(user_input)
    if path.exists():
        return sort.main(path)
    else:
        return f"The path {path} does not exist."


def func_good_bye():
    book.save()
    note_book.save_data()
    print(f"Good bye!")
    exit()


exit_commands = ["good bye", "close", "exit"]
EXIT = {command: func_good_bye for command in exit_commands}


FUNCTIONS = {
    "hello": func_hello,
    "add record": func_add,
    "add address": func_address,
    "add birthday": add_birthday,
    "add email": add_email,
    "edit record": func_edit_record,
    "change phone": func_change_phone,
    "phone of": func_phone,
    "show all records": func_show_all,
    "show records": func_show,
    "find record": func_find,
    "remove record": func_remove,
    "sort folder": func_sort_folder,
    "birthdays within days": func_birthdays_within_days,
    "help": help_func.func_help,
    "": unknown,
}

if __name__ == "__main__":
    help()
