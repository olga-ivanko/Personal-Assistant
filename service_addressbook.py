from datetime import datetime
from addressbook import AddressBook, Record
from pathlib import Path
import sort
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


def unknown(*args):
    return "Unknown command. Try again."


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
        new_email = None
        new_address = None
        contact_birtday = None
        while True:
            user_input = input("Enter your choice: ").lower()
            if user_input == "back":
                break
            if user_input == "birthday":
                user = input("Enter birthday: ")
                new_birthday = datetime(
                    year=int(user[6:]), month=int(user[3:5]), day=int(user[:2])
                )
                contact_birtday = new_birthday.date().strftime("%d %B %Y")
                new_record.add_birthday(new_birthday)
                print("Birthday added")
            elif user_input == "email":
                user = input("Enter email: ")
                new_email = user
                new_record.add_email(new_email)
                print(f"main {new_email} added to user {new_record.name.value}")
            elif user_input == "address":
                user = input("Enter address: ")
                new_address = user
                new_record.add_address(new_address)
                print("Address added")

        book[rec_id] = new_record
        if new_address:
            return f"Record {rec_id = }, {new_phone = }, {contact_birtday = }, {new_email = }, {new_address = } added"
        elif new_email:
            return f"Record {rec_id = }, {new_phone = }, {contact_birtday = }, {new_email = } added"
        return f"Record {rec_id = }, {new_phone = }, {contact_birtday = } added"

    book[rec_id] = new_record
    return f"Record {rec_id = }, {new_phone = } added"


def func_edit_record(*args):
    rec_id = args[0].lower()
    if not rec_id in book.keys():
        return f"Record do not exist"

    record = book.find(rec_id)
    print(record)
    print(f"type what needs to be changed:\n phone \n email\n address \n birthday")
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
        user_input2 = input("Print new email:\n")
        record.email.value = user_input2.strip()
        return f"Record updated as:\n {record}"
    elif user_input == "address":
        print(f"current addess is {record.address.value}.")
        user_input2 = input("Print new address:\n")
        record.address.value = user_input2.strip()
        return f"Record updated as:\n {record}"
    elif user_input == "birthday":
        if record.birthday.value:
            print(f"current addess is {record.birthday.value}.")
            user_input2 = input("Print new birthday:\n")
            record.a
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
    return f"Add Birthday completed: {birth = }"


@user_error
def add_email(*args):
    rec_id = args[0]
    email = args[1]
    if not rec_id in book:
        return "Not user"
    book.find(rec_id).add_email(email)
    return f"Add email completed: {email = }"


def func_address(*args):
    rec_id = args[0]
    address = args[1]
    if not rec_id in book:
        return "Not user"
    book.find(rec_id).add_address(address)
    return f"Add address completed: {address =}"


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
    return f"Record {rec_id} is updated with new phone: {new_phone}"


# @user_error
# def func_phone(*args):
#    rec_id = args[0]
#    return f"Phone(s) of {rec_id} is {book.get(rec_id).phones[0]}"


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


FUNCTIONS = {
    "hello": func_hello,
    "add": func_add,
    "edit record": func_edit_record,
    "change": func_change,
    # "phone": func_phone,
    "show all": func_show_all,
    "show": func_show,
    "find": func_find,
    "email_add": add_email,
    "adress_add": func_address,
    "birthday_add": add_birthday,
    "remove": func_remove,
    "sort folder": func_sort_folder,
    "": unknown,
}
