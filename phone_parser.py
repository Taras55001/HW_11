from collections import UserDict
from datetime import datetime
from itertools import islice
import re


input_line = "-" * 50 + "\n"\
    "Input command \n"\
    "(example: 'add name phone_number')"


class AddressBook(UserDict):
    def add_record(self, record) -> str:
        self.data[record.name.value] = record
        return f'Contact {record.name} create successful'

    def add_phone(self, name, phone) -> str:
        if phone not in self.data[name]:
            self.data[name].phones.append(phone)
            return f'Phone {phone} added to contact {name} numbers'
        return f'Contact {name} with phone {phone} are already exist'

    def change_phone(self, name, phone, new_phone):
        if phone in self.data[name]:
            self.data[name].phones.remove(phone)
        return self.data[name].phones.append(new_phone)

    def delete_record(self, name) -> str:
        self.data.pop(name)
        return f'Contact {name} deleted successful'

    def iterator(self, start=None, stop=None):
        keys = islice(self.data.keys(), start, stop)
        result = '\n'.join(
            f'{i}: +{", +".join(p.value for p in self.data.get(i).phones)}, birthday {self.data.get(i).birthday}' for i in keys)

        yield result


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        try:
            if len(value) > 2:
                self._value = value
        except ValueError:
            raise ValueError(
                "Value must be a string of length of at least 2")

    def __repr__(self) -> str:
        return self._value

    def __str__(self) -> str:
        return str(self._value)


class Birthday:
    def __init__(self, value="13 October 1990"):
        self._value = None
        self.value = value

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value):
        try:
            self._value = datetime.strptime(value, '%d-%m-%Y').date()
        except ValueError:
            raise ValueError(
                "Invalid date format. Please use format: DD-MM-YYYY")

    def __str__(self) -> str:
        return self._value.strftime('%d %B %Y')


class Name(Field):

    @Field.value.setter
    def value(self, value):
        try:
            if value.isalpha():
                super(Name, Name).value.__set__(self, value)
        except ValueError:
            raise ValueError(
                "Value must be a string of alphabetical characters")


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phones = [phone] if phone else []
        self.birthday = birthday

    def add_phone(self, phone):
        self.phones.append(self.phone)

    def change_phone(self, old_phone, new_phone) -> str:
        if old_phone in book.data[self.name]:
            book.change_phone(self.name, old_phone, new_phone)
            return f'Phone {old_phone} change to {new_phone}'
        return f'No phone {old_phone}'

    def delet_phone(self, phone):
        self.phones.remove(phone)

    def days_to_birthday(self) -> int:
        if self.birthday:
            today = datetime.now().date()
            target_day = self.birthday.value.replace(year=today.year)
            if target_day < today:
                target_day = self.birthday.value.replace(year=today.year+1)
            difference = (target_day - today).days
            return difference


class Phone(Field):
    @Field.value.setter
    def value(self, value):
        try:
            if re.match(r'^\d{12}$', value):
                super(Phone, Phone).value.__set__(self, value)
        except ValueError:
            raise ValueError("Phone must be in 123456789876 format")

    def __eq__(self, __value: object) -> bool:
        return self.value == __value.phone


book = AddressBook()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            print("Контакт не знайдено")
        except ValueError as error:
            print(error)
        except TypeError:
            print("Недостатньо аргументів")
    return wrapper


def iter_book(command=None):
    stop = int(input("Input step "))
    start = 0
    step = stop
    while True:
        text = next(book.iterator(start, stop))
        if not text:
            break
        print(text)
        input("Press enter to continue ")
        start += step
        stop += step
    return f"End of list"


@ input_error
def add_record(command):
    splitting_arguments = command.strip().split()
    if len(splitting_arguments) >= 2:
        key, name, phone, birthday = splitting_arguments
        rec = book.data.get(name)
        if rec:
            rec = book.add_phone
            return rec(name, Phone(phone))
        contact_name = Name(name)
        contact_phone = Phone(phone)
        rec = Record(contact_name, contact_phone, Birthday(birthday))
        if contact_name:
            # for Name(None) does not create dict
            result = book.add_record(rec)
            rec.days_to_birthday()
            return result


@ input_error
def birthday(command):
    splitting_arguments = command.strip().split()
    key, name = splitting_arguments
    record = book.data.get(name)
    print(record.birthday)
    return record.days_to_birthday()


@ input_error
def change_record(command):
    arguments = command.strip().split()
    if len(arguments) == 4:
        key, name, phone, new_phone = arguments
        record = Record(Name(name))
        return record.change_phone(Phone(phone), Phone(new_phone))


@ input_error
def delete(command):
    argument = command.strip().split()[1]
    if argument:
        return book.delete_record(argument)


def get_func(command):
    arg_list = command.strip().split()
    for key in command_dict.keys():
        if arg_list[0].lower() == 'hello':
            return command_dict[key]
        elif arg_list[0].lower() == key:
            func = command_dict.get(key)
            return func(command)
        elif arg_list[0].lower() in key:
            return command_dict[key]
    raise KeyError("This command doesn't exist")


command_dict = {"hello": "How can I help you?", "add": add_record, "birthday": birthday, "change": change_record, "delete": delete,
                "show": iter_book, ("good", "bye", "close", "exit"): "Good bye!"}


def main():

    while True:

        command = input(input_line).lower()
        command = "add test 123456789876 10-02-1990"  # test func
        func = get_func(command)
        print(func)
        iter_book()  # test func
        print(birthday("birthday test"))  # test func
        if command.split()[0] in ["good", "bye", "close", "exit"]:
            break


if __name__ == '__main__':
    main()
