from collections import UserDict
from datetime import datetime
from itertools import islice
import re


input_line = "-" * 50 + "\n"\
    "Input command \n"\
    "(example: 'add name phone_number')"


class AddressBook(UserDict):
    def add_record(self, record) -> str:
        self.data[record.name.value] = record.phones
        return f'Contact {record.name.value} create successful'

    def add_phone(self, name, phone) -> str:
        if phone not in self.data[name]:
            self.data[name].append(phone)
            return f'Phone {phone} added to contact {name} numbers'
        return f'Contact {name} whith phone {phone} are alredy exist'

    def change_phone(self, name, phone, new_phone):
        if phone in self.data[name]:
            self.data[name].remove(phone)
        return self.data[name].append(new_phone)

    def delete_record(self, name) -> str:
        self.data.pop(name)
        return f'Contact {name} deleted successful'

    def iterator(self, start, stop):
        key = islice(self.data, start, stop)
        result = '\n'.join(
            f'{i}: {", ".join(p.value for p in self.data.get(i))}' for i in key)
        yield result


class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if len(value) < 2:
            raise ValueError("Not enough symbols")
        self._value = value

    def __repr__(self) -> str:
        return self.value


class Birthday:
    def __init__(self, value="13 October 1990"):
        self.value = datetime.strptime(value, '%d %B %Y').date()

    def __str__(self) -> str:
        return self.value.strftime('%d %B %Y')

    def __repr__(self) -> str:
        return self.value

    # @property
    # def value(self):
    #     return self._value

    # @value.setter
    # def value(self, value):
    #     if not re.match(r'^\d{1,2}\s[a-zA-Z]+\s\d{4}$', value):
    #         print("Date have to be 'DD Month YYYY'")
    #     else:
    #         self.value = datetime.strptime(value, '%d %B %Y').date()
    #         print('12')


class Name(Field):

    @Field.value.setter
    def value(self, value):
        if not value.isalpha():
            raise ValueError(
                "Value must be a string of alphabetical characters")
        self.value = value


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phones = [phone] if phone else []
        self.birthday = birthday
        # print(self.birthday)
        # print(self.name, name)

    def add_phone(self, phone):
        self.phones.append(self.phone)

    def change_phone(self, old_phone, new_phone) -> str:
        if old_phone in book.data[self.name.value]:
            book.change_phone(self.name.value, old_phone, new_phone)
            return f'Phone {old_phone} change to {new_phone}'
        return f'No phone {old_phone}'

    def delet_phone(self, phone):
        self.phones.remove(phone)

    def days_to_birthday(self) -> int:
        if self.birthday:
            today = datetime.now().date()
            target_day = self.birthday.value.replace(year=today.year)
            difference = (target_day - today).days
            return difference


class Phone(Field):
    @Field.value.setter
    def phone(self, value):
        if not re.match(r'^\+\d{12}$', value):
            print("Phone must be in +123456789876 format")
        else:
            self.value = value

    def __eq__(self, __value: object) -> bool:
        return self.value == __value.phone


book = AddressBook()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            print("Контакт не знайдено")
        except ValueError:
            print("Номер телефону повинен містити тільки цифри")
        except TypeError:
            print("Недостатньо аргументів")
    return wrapper


@ input_error
def iter_book(command) -> str:
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
    spliting_arguments = command.strip().split()
    if len(spliting_arguments) == 3:
        key, name, phone = spliting_arguments
        rec = book.get(name)
        if rec:
            rec = book.add_phone
            return rec(name, Phone(phone))

        rec = Record(Name(name), Phone(phone),
                     Birthday("13 October 1990"))
        # дата за замовченням доки не розберусь з сеттерром
        result = book.add_record(rec)
        rec.days_to_birthday()
        return result


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


command_dict = {"hello": "How can I help you?", "add": add_record, "change": change_record, "delete": delete,
                "show": iter_book, ("good", "bye", "close", "exit"): "Good bye!"}


def main():

    while True:

        command = input(input_line).lower()
        # command = "add test +1234567898"
        func = get_func(command)
        print(func)
        if command.split()[0] in ["good", "bye", "close", "exit"]:
            break


if __name__ == '__main__':
    main()


...  # AddressBook реалізує метод iterator, який повертає генератор за записами AddressBook і за одну ітерацію повертає уявлення для N записів.
...  # Клас Record приймає ще один додатковий(опціональний) аргумент класу Birthday
...  # Клас Record реалізує метод days_to_birthday, який повертає кількість днів до наступного дня народження контакту, якщо день народження заданий.
# setter та getter логіку для атрибутів value спадкоємців Field.
# Перевірку на коректність веденого номера телефону setter для value класу Phone.
# Перевірку на коректність веденого дня народження setter для value класу Birthday.
