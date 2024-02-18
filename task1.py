from collections import UserDict
import re

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "No such name found"
        except IndexError:
            return "Not found"
        except Exception as e:
            return f"Error: {e}"

    return inner

#@input_error
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

@input_error
class Name(Field):
    # реалізація класу
    def __init__(self, value):
        super().__init__(value)

@input_error
class Phone(Field):
    # Реалізовано валідацію номера телефону (має бути перевірка на 10 цифр)
    def __init__(self, value):
        if re.fullmatch(r"\d{10}",value)==None:
            raise Exception(f'The phone number must consist of 10 digits, received: \'{value}\'')
        super().__init__(value)
		
@input_error
class Record:
    #Реалізовано зберігання об'єкта Name в окремому атрибуті.
    #Реалізовано зберігання списку об'єктів Phone в окремому атрибуті (phones).
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    # реалізація класу

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone):
        #додавання телефону
        self.phones.append(Phone(phone))
        return "Contact added."
    def remove_phone(self, phone):
        #видалення телефону
        self.phones.remove(Phone(phone))
        return "Contact removed."
    
    def find_phone(self, phone):
        # пошук об'єкта Phone
        for phone_i in self.phones:
            if phone_i.value == phone:
                return phone_i
        return None
    
    def edit_phone(self, phone,new_phone):
        #редагування номеру телефону
        #повертаємо відредагований об'єкт Phone, якщо його знайшли за значенням phone
        for phone_i in self.phones:
            if phone_i.value == phone:
                phone_i.value = new_phone
                return phone_i
        return None

@input_error    
class AddressBook(UserDict):
    # реалізація класу
    def __init__(self, value=None):
        if type(value)==type(UserDict):
            self.data = value
        elif type(value)==type(dict):
            self.data = UserDict(value)
        elif type(value)==type(None):
            self.data = UserDict({})
        else:
            self.data = UserDict({})

    def add_record(self,r:Record):
        #додає запис до self.data.
        if r not in self.data:
            self.data [r.name]=r
    def __str__(self):
        #перетворює у зручний для виведення формат збережені значення
        book_string = ""
        for KeyValue in self.data.values():
            book_string+=str(KeyValue)+'\n'
        return book_string
    def find(self,name):
        #знаходить запис за ім'ям
        for key in self.data.keys():
            if key.value == name:
                return self.data[key]
        return None    

    def delete(self,name):
        #видаляє запис за ім'ям
        for key in self.data.keys():
            if key.value == name:
                return self.data.pop(key)
        return None


def main():

    # Створення нової адресної книги
    book = AddressBook()
    
    print(book)
    print()
    
    p1=Phone('1234567890')
    print(p1)
    p2=Phone('fdlkfjsldkjf')
    print(p2)
    n1=Name('n1: fdsfsdfsd')
    print(n1)
    print()
    
    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")


    
    print(john_record)
    # Додавання запису John до адресної книги
    book.add_record(john_record)

    print(book)
    print()
    
    
    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    
    print(book)
    print()
    
    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)
    
    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555
    
    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
    print(book)

if __name__ == "__main__":
    main()