from pathlib import Path
from collections import UserDict
from collections.abc import Iterator
from datetime import datetime
import pickle

import re


class Field:
    def __init__(self):
        self.__value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self):
        super().__init__()
        self.__value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Phone(Field):
    def __init__(self, value):
        super().__init__()
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if len(new_value) != 10 or not new_value.isdigit():
            raise ValueError
        self.__value = new_value


class Birthday(Field):
    def __init__(self):
        super().__init__()
        self.__value = "unknown"

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value: datetime):
        if type(new_value) != datetime:
            raise ValueError
        else:
            self.__value = new_value.date()


class Email(Field):
    def __init__(self):
        super().__init__()
        self.__value = "no email"

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value: str):
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', new_value):
            raise ValueError("Check mail format")
        self.__value = new_value


class Address(Field):
    def __init__(self):
        super().__init__()
        self.__value = "no address"

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value: str):
        self.__value = new_value


class Record:
    def __init__(self, name: Name):
        new_name = Name()
        new_name.value = name
        self.name = new_name
        self.phones = []
        self.birthday = Birthday()
        self.email = Email()
        self.address = Address()

    def add_phone(self, phone):
        new_phone = Phone(phone)
        if not phone in "".join(p.value for p in self.phones):
            new_phone.value = phone
            self.phones.append(new_phone)

    def remove_phone(self, phone: str):
        self.phones.remove(self.find_phone(phone))

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        new_ph = Phone(new_phone)
        new_ph.value = new_phone
        self.phones.append(new_ph)

    def find_phone(self, phone: str):
        for x in self.phones:
            if x.value == phone:
                return x

    def add_birthday(self, birthday):
        self.birthday.value = birthday

    def add_email(self, email):
        self.email.value = email

    def add_address(self, address):
        self.address.value = address

    def days_to_birthday(self):
        today = datetime.now().date()
        if today <= self.birthday.value.replace(year=today.year):
            next_bd = self.birthday.value.replace(year=today.year)
            days_to_bd = next_bd - today
            return days_to_bd.days
        else:
            next_bd = self.birthday.value.replace(year=today.year + 1)
            days_to_bd = next_bd - today
            return days_to_bd.days

    def __str__(self):
        if self.birthday.value != "unknown":
            return "Contact name: {:<5}| phones: {:<12}| birthday: {} ({} days to birthday), email: {}, address: {}".format(
                self.name.value,
                "; ".join(p.value for p in self.phones),
                self.birthday.value,
                self.days_to_birthday(),
                self.email.value,
                self.address.value,
            )

        else:
            return "Contact name: {:<5}| phones: {:<12}| email: {}| address: {}".format(
                self.name.value,
                "; ".join(p.value for p in self.phones),
                self.email,
                self.address,
            )


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self[str(record.name)] = record

    def find(self, name) -> Record:
        if name in self.keys():
            found_rec = self.get(name)
            return found_rec

    def delete(self, name):
        if name in self.keys():
            self.pop(name)

    def iterator(self, max_records=2) -> Iterator:
        indx = 0
        page = 1
        print_page = f"\n Page {page}\n"
        for rec in self.data.values():
            print_page += f"{rec}\n"
            indx += 1
            if indx >= max_records:
                yield print_page
                print_page = ""
                print_page = f"\n Page {page + 1}\n"
                indx = 0
                page += 1
        if indx > 0:
            yield print_page

    def load(self):
        file_name = "book.bin"
        try:
            load_dir = Path(__file__).resolve().parent
            file_path = load_dir.joinpath(file_name) 
            with open(file_path, "rb") as fb:
                self.data = pickle.load(fb)
                print(
                    f"AddressBook with {len(self.data)} contacts is succesfuly uploaded"
                )
                return self.data
        except FileNotFoundError:
            book = AddressBook()

    def save(self):
        file_name = "book.bin"
        save_dir = Path(__file__).resolve().parent
        file_path = save_dir.joinpath(file_name) 
        with open(file_path, "wb") as fb:
            pickle.dump(self.data, fb)
            print("AddressBook is saved as book.bin")
        return None
