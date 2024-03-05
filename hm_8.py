import pickle
from datetime import datetime, timedelta

class Field:
    pass

class Name(Field):
    def __init__(self, value):
        self.value = value

class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Неправильний формат номера телефону. Введіть 10 цифр.")
        self.value = value

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Неправильний формат дати. Введіть у форматі ДД.ММ.РРРР")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def upcoming_birthday(self):
        if self.birthday:
            today = datetime.today().date()
            next_week = today + timedelta(days=7)
            if self.birthday.value.date() <= next_week:
                return True
        return False

class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_record(self, record):
        self.contacts.append(record)

    def find(self, name):
        for contact in self.contacts:
            if contact.name.value == name:
                return contact
        return None

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        for contact in self.contacts:
            if contact.upcoming_birthday():
                upcoming_birthdays.append(contact.name.value)
        return upcoming_birthdays

def parse_input(user_input):
    return user_input.split(maxsplit=2)

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def add_contact(args, book: AddressBook):
    if len(args) < 2:
        return "Неправильний формат команди. Будь ласка, введіть ім'я та номер телефону для додавання контакту."
    name, phone, *_ = args
    try:
        record = book.find(name)
        if record:
            record.add_phone(phone)
            return "Телефонний номер оновлено."
        else:
            record = Record(name)
            record.add_phone(phone)
            book.add_record(record)
            return "Контакт додано."
    except ValueError as e:
        return str(e)

def change_contact(args, book: AddressBook):
    name, new_phone, *_ = args
    try:
        record = book.find(name)
        if record:
            record.add_phone(new_phone)
            return "Телефонний номер оновлено."
        else:
            return "Контакт не знайдено."
    except ValueError as e:
        return str(e)

def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record:
        if record.phones:
            phones = ", ".join([str(phone.value) for phone in record.phones])
            return phones
        else:
            return "Номер телефону не вказаний для цього контакту."
    else:
        return "Контакт не знайдено."

def show_all(book: AddressBook):
    if book.contacts:
        all_contacts = []
        for contact in book.contacts:
            phones = ", ".join([phone.value for phone in contact.phones]) if contact.phones else "Номер телефону не вказаний"
            all_contacts.append(f"{contact.name.value}: {phones}")
        return "\n".join(all_contacts)
    else:
        return "Адресна книга порожня."

def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    try:
        record = book.find(name)
        if record:
            record.add_birthday(birthday)
            return "День народження додано."
        else:
            return "Контакт не знайдено."
    except ValueError as e:
        return str(e)

def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record:
        if record.birthday:
            return f"День народження {name}: {record.birthday.value.strftime('%d.%m.%Y')}"
        else:
            return f"День народження для {name} не вказано."
    else:
        return "Контакт не знайдено."

def birthdays(args, book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "Користувачі, яких потрібно привітати на наступному тижні:\n" + "\n".join(upcoming_birthdays)
    else:
        return "На наступному тижні немає днів народження."

def main():
    book = load_data()
    print("Ласкаво просимо до бота-асистента!")
    while True:
        user_input = input("Введіть команду: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book) 
            print("До побачення!")
            break

        elif command == "hello":
            print("Як я можу вам допомогти?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Невірна команда.")

if __name__ == "__main__":
    main()