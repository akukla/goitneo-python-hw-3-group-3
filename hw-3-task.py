from model import *


def input_error(msg):
    def actual_decorator(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (KeyError, ValueError, IndexError):
                return msg
        return inner
    return actual_decorator


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error("Give me name and phone please")
def add_contact(args, book: AddressBook):
    name, phone = args
    record = Record(name)
    if not record.add_phone(phone):
        return "Contact not added"
    book.add_record(record)
    return "Contact added."


@input_error("Give me name and phone please")
def change_contact(args, book: AddressBook):
    name, phone = args
    record = book.find(name)
    if not record:
        return "Contact not found"
    if not record.edit_phone(phone):
        return "Contact not updated."
    return "Contact updated."


@input_error("Enter user name")
def get_contact(args, book: AddressBook):
    name, = args
    contact = book.find(name)

    if not contact:
        return "Contact not found"
    return contact.phone.value


def get_all_contact(args, book: AddressBook):
    if len(book) == 0:
        return 'Address book is empty'
    ret = []
    for item in book.enumerate():
        ret.append(str(item))
    return '\n'.join(ret)


def print_birthdays(args, book):
    birthdays = book.get_birthdays_per_week()
    if len(birthdays):
        return str('\n'.join(birthdays))
    else:
        return 'You don\'t have any birthdays next week'


@input_error("Incorect parameters. Correct format parameters is: add-birthday name birthday")
def add_birthday(args, book: AddressBook):
    name, bithday = args
    record = book.find(name)
    if record is None:
        return 'Contact not found'
    
    if not record.add_birthday(bithday):
        return "Birthday not added"

    return 'Birthday added'


@input_error("Incorect parameters. Correct format parameters is: show-birthday name")
def show_birthday(args, book: AddressBook):
    name, = args
    record = book.find(name)
    if record is None:
        return 'Contact not found'
    
    if record.birthday is None:
        return 'Birthday is not defined'

    return str(record.birthday)


def main():
    book: AddressBook = AddressBook.load_or_create()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        should_save = False

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
            should_save = True
        elif command == "change":
            print(change_contact(args, book))
            should_save = True
        elif command == "phone":
            print(get_contact(args, book))
        elif command == "all":
            print(get_all_contact(args, book))
        elif command == "birthdays":
            print(print_birthdays(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
            should_save = True
        elif command == "show-birthday":
            print(show_birthday(args, book))
            should_save = True
        else:
            print("Invalid command.")

        if should_save:
            book.save()


if __name__ == "__main__":
    main()