import hashlib
from scndrfunctions import *
from dict import *


# АВТОРИЗАЦІЯ
def login(cursor):
    print("\tВхід у систему")
    login = input('Введіть, будь ласка, свій емейл або телефон: ')
    passw = input('Введіть свій пароль: ')
    is_numb_ph = False
    if (login[0] == '+' and login[1:].isnumeric()) or login.isnumeric():
        if len(login) > 13:
            print('Номер телефону введено некоректно')
            return 0, 0
        else:
            is_numb_ph = True
    elif login[0] == '+' and not login[1:].isnumeric():
        print(unf_error_2)
        return 0, 0
    if is_numb_ph:
        cursor.execute(f"SELECT user_phone, user_password FROM users WHERE user_phone = ('{login}')")
    else:
        cursor.execute(f"SELECT user_email, user_password FROM users WHERE user_email = ('{login}')")
    result = cursor.fetchall()
    try:
        if result[0][0] == login and result[0][1] == hashlib.md5(passw.encode()).hexdigest():
            if is_numb_ph:
                cursor.execute(f"SELECT user_id FROM users WHERE user_phone = '{login}'")
            else:
                cursor.execute(f"SELECT user_id FROM users WHERE user_email = '{login}'")
            result = cursor.fetchall()
            return 1, result[0][0]
        else:
            print(unf_error_4)
    except IndexError:
        print(unf_error_4)
    except:
        print(unf_error)
    return 0, 0


# РЕГІСТРАЦІЯ
def registration(cursor):
    print("\tРеєстрація")
    name = input("Введіть, будь ласка, своє ім'я: ")
    surname = input("Введіть своє прізвище: ")
    email = input("Введіть свій емейл: ")
    phone = input("Введіть свій номер телефону: ")
    if len(phone) > 13:
        print("Схоже, ви ввели некоректний номер телефону. Спробуйте ще раз.")
        return 0, 0
    password = input("Введіть пароль: ")
    password_1 = input("Введіть пароль ще раз: ")
    if password != password_1:
        print("Ви ввели різні паролі. Спробуйте ще раз.")
        return registration(cursor)
    hash_password = hashlib.md5(password.encode()).hexdigest()
    try:
        cursor.execute(
            f"INSERT INTO users (user_name, user_surname, user_email, user_phone, user_password) VALUES ('{name}', '{surname}', '{email}', '{phone}', '{hash_password}')")
        mydb.commit()
        cursor.execute(f"SELECT user_id FROM users WHERE user_email = '{email}'")
        result = cursor.fetchall()
        return 1, result[0][0]
    except mysql.connector.errors.IntegrityError:
        print("Схоже, ви вже зареєстровані. Спробуйте увійти в акаунт або зареєструватися ще раз.")
    except mysql.connector.errors.DataError:
        print("Схоже, ви ввели неприпустимі дані (або занадто довгі). Спробуйте ще раз.")
    except:
        print(unf_error)
    return 0, 0


# ПІСЛЯ ВХОДУ У СИСТЕМУ (ВИЗНАЧАЄТЬСЯ РОЛЬ)
def mngm(userID):
    cursor = mydb.cursor()
    cursor.execute(f"SELECT role_id FROM user_role WHERE user_id ='{userID}'")
    userRole = cursor.fetchall()
    if userRole[0][0] == 1:
        user(userID)
    elif userRole[0][0] == 2:
        manager(userID)
    else:
        admin()
    cursor.close()


#ВХІД ДЛЯ USERів
def user(user_id):
    cursor = mydb.cursor()
    choice = help_usr()
    while choice != "5":
        if choice == "1":
            cursor.execute(f"SELECT b.book_id, b.title, b.amount_of_pages, b.genre, b.price, a.author_name FROM book "
                           f"b, author a WHERE b.author_id = a.author_id ORDER BY b.book_id")
            books = cursor.fetchall()
            print_books(books)
            print("\n\tЦе всі наявні книжки в магазині.")
        elif choice == "2":
            cursor.execute("SELECT b.book_id, b.title, b.amount_of_pages, b.genre, b.price, a.author_name FROM book "
                           "b, author a WHERE b.author_id = a.author_id ORDER BY b.price")
            books = cursor.fetchall()
            print_books(books)
        elif choice == "3":
            cursor.execute("SELECT b.book_id, b.title, b.amount_of_pages, b.genre, b.price, a.author_name FROM book "
                           "b, author a WHERE b.author_id = a.author_id ORDER BY b.amount_of_pages")
            books = cursor.fetchall()
            print_books(books)
        elif choice == "4":
            make_order(user_id, cursor)
        else:
            print(opt_er)
        choice = help_usr()
    cursor.close()
    print(gdb)


# ВХІД ДЛЯ АДМІНІВ
def admin():
    cursor = mydb.cursor()
    choice = help_adm()
    while choice != "3":
        if choice == "1":
            cursor.execute("SELECT u.user_id, CONCAT(u.user_name,' ',u.user_surname), u.user_email, u.user_phone, "
                           "COALESCE(r.role_name, 'невідомо (не призначено)') FROM user_role ur RIGHT OUTER JOIN "
                           "users u ON (ur.user_id = u.user_id) LEFT OUTER JOIN rolee r ON (r.id = ur.role_id);")
            result = cursor.fetchall()
            print_users(result)
        elif choice == "2":
            id_ass = input("Введіть, будь ласка, ID користувача, якому бажаєте призначити нову роль: ")
            cursor.execute(f"SELECT u.user_id, CONCAT(u.user_name,' ',u.user_surname), u.user_email, u.user_phone, "
                           f"COALESCE(r.role_name, 'невідомо (не призначено)') FROM user_role ur RIGHT OUTER JOIN "
                           f"users u ON (ur.user_id = u.user_id) LEFT OUTER JOIN rolee r ON (r.id = ur.role_id) WHERE "
                           f"u.user_id = '{id_ass}';")
            result = cursor.fetchall()
            if not cursor.rowcount:
                print("Схоже, ви ввели ID кориистувача, якого не існує або немає в системі. Спробуйте ще раз.")
            else:
                print(" Ви обрали:")
                print_users(result)
                choice_role = input("Оберіть нову роль користувачеві:\n 1 - Звичайний користувач(user)\n 2 - "
                                    "Менеджер\n 3 - Адмін\n")
                if choice_role == "1" or choice_role == "2" or choice_role == "3":
                    cursor.execute(f"UPDATE user_role SET role_id = '{choice_role}' WHERE user_id = '{id_ass}'")
                    cursor.fetchall()
                    mydb.commit()
                    print("Готово! Нову роль призначено.")
                else:
                    print(unf_error_2)
        else:
            print("Перепрошуємо, можливі опції: '1', '2', '3'. Спробуйте ще раз.")
        choice = help_adm()
    cursor.close()
    print(gdb)


# ВХІД ДЛЯ МЕНЕДЖЕРІВ
def manager(managerID):
    cursor = mydb.cursor()
    choice = help_mngr()
    while choice != "5":
        if choice == "1":
            ac_order(cursor, managerID)
        elif choice == "2":
            add_new_book(cursor)
        elif choice == "3":
            cursor.execute("SELECT b.book_id, b.title, b.amount_of_pages, b.genre, b.price, a.author_name FROM book "
                           "b, author a WHERE b.author_id = a.author_id")
            books = cursor.fetchall()
            print_books(books)
            update_book(cursor)
        elif choice == "4":
            add_new_publisher(cursor)
        else:
            print(opt_er)
        choice = help_mngr()
    cursor.close()
    print(gdb)


def p1_0():
    choice = input(" Оберіть:\n1 - Зареєструватися\n2 - Увійти в систему\n")
    cursor = mydb.cursor()
    if choice == "1":
        succs, id = registration(cursor)
        if succs == 1:
            print(wlcm_1)
            mk_user_role(cursor, id)
            user(id)
        else:
            p1_0()
    elif choice == "2":
        succs, id = login(cursor)
        if succs == 1:
            print(wlcm_2)
            mngm(id)
        else:
            p1_0()
    else:
        print(unf_error_3)
        p1_0()
    cursor.close()
    mydb.close()

