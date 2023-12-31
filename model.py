from collections import UserDict
from typing import Optional, Self
from datetime import date
import pickle
import re


class IncorrectFormatException(Exception):
    pass


class Birthday:

    pattern = '^(\d{2})\.(\d{2})\.(\d{4})$'

    def __init__(self, value):
        match_result = re.match(Birthday.pattern, value)
        if match_result is None:
            raise IncorrectFormatException("Incorrect birthday format. Valid format is DD.MM.YYYY")
        day, month, year = match_result.groups()
        self.date = date(year=int(year), month=int(month), day=int(day))

    def __str__(self):
        if not self.date:
            return "No date"
        return self.date.strftime("%d.%m.%Y")


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):

    def __init__(self, value):
        if not Phone.is_valid(value):
            raise IncorrectFormatException("Incorrect phone format")
        super().__init__(value)

    @staticmethod
    def is_valid(phone: str) -> bool:
        return isinstance(phone, str) and phone.isdigit() and len(phone) == 10


class Record:

    def __init__(self, name):
        self.name = Name(name)
        self.phone:Optional[Phone] = None
        self.birthday: Optional[Birthday] = None

    def add_birthday(self, birthday: str)  -> bool:
        try:
            birthday_obj = Birthday(birthday)
        except IncorrectFormatException:
            print("Incorrect birthday format")
            return False
        self.birthday = birthday_obj
        return True

    def add_phone(self, phone: str) -> bool:
        try:
            phone_obj = Phone(phone)
        except IncorrectFormatException:
            print("Incorrect phone format")
            return False
        self.phone = phone_obj
        return True

    def edit_phone(self, new_phone: str) -> bool:
        if not Phone.is_valid(new_phone):
            print("Incorrect phone format")
            return False
        self.phone = Phone(new_phone)
        return True
    
    def __str__(self):
        ret = f"Contact name: {self.name.value}, phone: {self.phone}"
        if self.birthday is not None:
            ret += f", birthday: {self.birthday}"
        return ret


class AddressBook(UserDict):

    def __init__(self, filename = 'address_book.bin'):
        self.filename = filename
        UserDict.__init__(self)

    def add_record(self, record: Record) -> bool:
        self.data[record.name.value] = record
        return True

    def find(self, name: str) -> Optional[Record]:
        if name in self.data.keys():
            return self.data[name]
        return None
    
    def enumerate(self) -> Optional[Record]:
        for item in self.data:
            # print(type(item), item)
            yield self.data[item]

    def __len__(self) -> int:
        return len(self.data)

    def delete(self, name):
        if name in self.data.keys():
            del self.data[name]
            return True
        return False
    
    def save(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def load_or_create(filename = 'address_book.bin') -> Self:
        result = None
        try:
            with open(filename, "rb") as file:
                result = pickle.load(file)
        except Exception:
            print('Unable to load address book. Empty address book was created.')
        return result if result is not None else AddressBook()
    
    def get_birthdays_per_week(self) -> list[str]:
        return_list = []
        today = date.today()
        # Debug
        # today = today.replace(day=today.day + 4)
        # print(today)
        ret = {}
        week_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for key in self.data:
            user: Record = self.data[key]
            name = user.name.value
            if user.birthday is None or user.birthday.date is None:
                continue
            birthday = user.birthday.date
            birthday_this_year = birthday.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday.replace(year=today.year + 1)
            delta_days = (birthday_this_year - today).days
            if delta_days < 7:
                delta_days = birthday_this_year.weekday()
                if not delta_days in ret:
                    ret[delta_days] = []
                ret[delta_days].append(name)
        buff = []
        for day_index_from_today in range(today.weekday(), today.weekday() + 7):
            index = day_index_from_today % 7
            if index in ret:
                if index == 0:
                    buff.extend(ret[index])
                    if len(buff) > 0:
                        # print(f'{week_days[index]}: {", ".join(buff)}')
                        return_list.append(f'{week_days[index]}: {", ".join(buff)}')
                    buff.clear()
                elif index < 5:
                    return_list.append(f'{week_days[index]}: {", ".join(ret[index])}')
                    # print(f'{week_days[index]}: {", ".join(ret[index])}')
                else:
                    buff.extend(ret[index])
        if len(buff) > 0:
            return_list.append(f'{week_days[0]}: {", ".join(buff)}')
            # print(f'{week_days[0]}: {", ".join(buff)}')
        return return_list

