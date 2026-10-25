from info import Record, AddressBook
import pickle


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "This contact doesn't exist."
        except AttributeError:
            return "This contact doesn't exist."
        except IndexError:
            return "Enter the argument for the command."
        

    return inner


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message



@input_error
def change_contact(args, book: AddressBook ):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record.find_phone(old_phone) is None:
        return "Phone not found."
    record.edit_phone(old_phone, new_phone)
    return "Phone updated."

@input_error    
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    return "; ".join(phone.value for phone in record.phones)

@input_error
def show_all(book: AddressBook):
    return str(book)


@input_error
def add_birthday(args, book):
    if len(args) != 2:
        return "Usage: add-birthday <name> <DD.MM.YYYY>"
    record = book.find(args[0])
    record.add_birthday(args[1])
    return "Birthday added."

@input_error
def show_birthday(args, book):
    if len(args) != 1:
        return "Usage: show-birthday <name>"
    record = book.find(args[0])
    if record.birthday is None:
        return "Birthday is not set."
    return record.birthday.value

@input_error
def birthdays(args, book):
    if args:
        return "Usage: birthdays"
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    return "\n".join(
        f"{contact['name']}: {contact['birthday']}" for contact in upcoming
    )



def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено


def main():
    book = load_data()
    print("Welcome to the assistant bot!")

    try:
        while True:
            try:
                user_input = input("Enter a command: ")
            except (EOFError, KeyboardInterrupt):
                print("\nGood bye!")
                break

            if not user_input.strip():
                print("Imput cannot be empty.")
                continue

            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
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
                print("Invalid command.")
    finally:
        save_data(book)


if __name__ == "__main__":
    main()