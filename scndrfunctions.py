from dict import *


# ДРУК КНИГ
def print_books(books):
    for row in books:
        print(f"\tID книги - {row[0]}, назва - '{row[1]}'")
        print(f"ціна - {row[4]}, жанр - {row[3]}, кількість сторінок - {row[2]}, автор - {row[5]}")


# ДРУК ЗАМОВЛЕНЬ
def print_orders(orders):
    for row in orders:
        print(f"ID замовлення = {row[0]}, дата створення - {row[1]}")
        print("Статус - ", row[2])
        print(f"ID книги = {row[3]}, назва - {row[4]}, ціна = {row[5]}")
        print(
            f"ID покупця = {row[6]}, ім я покупця - {row[7]}, пошта покупця - {row[8]}, номер телефону покупця - {row[9]}")
        print("Менеджер  - ", row[10], "\n")


# ДРУК КОРИСТУВАЧІВ
def print_users(users):
    for row in users:
        print(f"\tUser ID = {row[0]}")
        print(f"Ім я користувача - {row[1]}, пошта користувача - {row[2]}, номер телефону - {row[3]}")
        print(f"РОЛЬ користувача - {row[4]}\n")


# 'Попрацювати із замовленнями' для MANAGER
def help_chc():
    print(questn)
    result = input("1) Подивитись архів замовлень (прийняті або скасовані)\n2) Повідомити про закінчення замовлення ("
                   "покупець заплатив та отримав книгу)\n3) Переглянути та прийняти нові замовлення\n4) Повідомити "
                   "про скасування замовлення (покупець відмовився купувати книгу або ще щось)\n5) Вихід\n")
    return result


# PRINT FOR MANAGER
def help_mngr():
    print(questn)
    result = input("1 - Попрацювати із замовленнями\n2 - Додати нову книгку в каталог\n3 - Оновити ціни на книги\n4 - "
                   "Додати нове видавництво\n5 - Вихід\n")
    return result


# PRINT FOR ADMIN
def help_adm():
    print(questn)
    result = input("1 - Переглянути усіх користувачів в системі\n2 - Призначити роль\n3 - Вихід\n")
    return result


# PRINT FOR USER
def help_usr():
    print(questn)
    choice = input("1 - Переглянути усі наявні книги в магазині\n2 - Відсортувати від найдешевшої до найдорожчої\n3 - "
                   "Відсортувати від найменшої до найбільшої\n4-  Здійснити замовлення\n5 - Вихід\n")
    return choice


# ПРИЗНАЧЕННЯ РОЛІ USER ДЛЯ КОРИСТУВАЧА, ЩО ТІЛЬКИ ЗАРЕЄСТРУВАВСЯ
def mk_user_role(cursor, user_id):
    cursor.execute(f"INSERT INTO user_role (role_id, user_id) VALUES ('{1}', '{user_id}')")
    mydb.commit()


# Додати нове видавництво для MANAGER
def add_new_publisher(cursor):
    publisherName = input("Введіть назву видавництва, яке бажаєте додати: ")
    try:
        cursor.execute(f"INSERT INTO publisher(publisher_name) VALUES('{publisherName}')")
        mydb.commit()
        print("Видавництво було успішно додано до системи.")
    except:
        print("Схоже, сталася помилка. Можливо, видавництво з такою назвою вже існує. Спробуйте ще раз.")
        return add_new_publisher(cursor)


# Оновити ціни на книги для MANAGER
def update_book(cursor):
    book_id = input("\n Введіть, будь ласка, ID книги, ціну якої бажаєте змінити: ")
    try:
        cursor.execute(f"SELECT title, price FROM book WHERE book_id = '{book_id}'")
        book_sql = cursor.fetchall()
        print(f" Ви обрали книжку '{book_sql[0][0]}', ціна - {book_sql[0][1]}")
        price_new = input("Введіть нову ціну: ")
        cursor.execute(f"UPDATE book SET price = '{price_new}' WHERE book_id = '{book_id}'")
        mydb.commit()
        print("\n Чудово, ціну змінено.\n")
    except IndexError:
        print("Схоже, ви ввели ID книги, якої не існує або немає в наявності. Спробуйте ще раз.")
        return update_book(cursor)
    except:
        print(unf_error_2)
        return update_book(cursor)


# (АВТОР КНИЖКИ (новий або вже існуючий)) FOR add_new_book для MANAGER
def odd_auth(cursor, name):
    try:
        cursor.execute(f"SELECT author_id FROM author WHERE author_name = '{name}'")
        cursor.fetchall()
        if not cursor.rowcount:
            print("Досі, цього письменника не було в системі, але він був до неї доданий.")
            cursor.execute(f"INSERT INTO author(author_name) VALUES('{name}')")
            mydb.commit()
        cursor.execute(f"SELECT author_id FROM author WHERE author_name = '{name}'")
        result = cursor.fetchall()
        return result[0][0]
    except:
        return "0"


# (ВИДАВНИЦТВО КНИЖКИ (нова або вже існуюча)) FOR add_new_book для MANAGER
def odd_publ(cursor, name):
    try:
        cursor.execute(f"SELECT publisher_id FROM publisher WHERE publisher_name = '{name}'")
        cursor.fetchall()
        if not cursor.rowcount:
            print("Досі, цього видавництва не було в системі, але воно було до неї додано.")
            cursor.execute(f"INSERT INTO publisher(publisher_name) VALUES('{name}')")
            mydb.commit()
        cursor.execute(f"SELECT publisher_id FROM publisher WHERE publisher_name = '{name}'")
        result = cursor.fetchall()
        return result[0][0]
    except:
        return "0"


# Додати нову книгку в каталог для MANAGER
def add_new_book(cursor):
    global publisherID, authorID
    title_m = input("Введіть, будь ласка, назву книги: ")
    amount_of_pages_m = input("Введіть кількість сторінок книги: ")
    genre_m = input("Введіть жанр книги(товару): ")
    price_m = input("Введіть ціну книги: ")
    author_m = input("Введіть ім'я та прізвище автора (введіть 0, якщо автор невідомий): ")
    if author_m != "0":
        authorID = odd_auth(cursor, author_m)
    publisher_m = input("Введіть видавництво книги (введіть 0, якщо інформація недоступна): ")
    if publisher_m != "0":
        publisherID = odd_publ(cursor, publisher_m)
    try:
        if author_m == "0" and publisher_m == "0":
            cursor.execute(
                f"INSERT INTO book(title, amount_of_pages, genre, price, author_id, publisher_id) VALUES('{title_m}', '{amount_of_pages_m}', '{genre_m}', '{price_m}', NULL, NULL)")
        elif author_m != "0" and publisher_m == "0":
            cursor.execute(
                f"INSERT INTO book(title, amount_of_pages, genre, price, author_id, publisher_id) VALUES('{title_m}', '{amount_of_pages_m}', '{genre_m}', '{price_m}', '{authorID}', NULL)")
        elif author_m == "0" and publisher_m != "0":
            cursor.execute(
                f"INSERT INTO book(title, amount_of_pages, genre, price, author_id, publisher_id) VALUES('{title_m}', '{amount_of_pages_m}', '{genre_m}', '{price_m}', NULL, '{publisherID}')")
        else:
            cursor.execute(
                f"INSERT INTO book(title, amount_of_pages, genre, price, author_id, publisher_id) VALUES('{title_m}', '{amount_of_pages_m}', '{genre_m}', '{price_m}', '{authorID}', '{publisherID}')")
        cursor.fetchall()
        mydb.commit()
        print("\tЧудово! Книжку було успішно додано до системи.")
    except:
        print(
            "Схоже сталася помилка. Можливо, дані, було введено некоректно, або книжка з такою назвою вже існує. "
            "Спробуйте ще раз.")
        add_new_book(cursor)


# Попрацювати із замовленнями для MANAGER
def ac_order(cursor, managerID):
    choice = help_chc()
    while choice != "5":
        if choice == "1":
            print("\tАрхів замовлень:")
            cursor = mydb.cursor()
            cursor.execute(
                "SELECT o.order_id, o.date_created, s.status_situation, b.book_id, b.title, b.price, u.user_id, "
                "CONCAT(u.user_name,' ',u.user_surname), u.user_email, u.user_phone, COALESCE(CONCAT(m.user_name,' ',"
                "m.user_surname), 'ніхто не розглядав !') FROM order_book o LEFT JOIN order_status s ON ("
                "o.status_id = s.status_id) LEFT "
                "JOIN book b ON (o.book_id = b.book_id) LEFT JOIN users u ON (o.user_id = u.user_id) LEFT JOIN "
                "users m ON (o.manager_id = m.user_id) WHERE s.status_id = 1 OR s.status_id = 3 ORDER BY u.user_name;")
            result1 = cursor.fetchall()
            print_orders(result1)
        elif choice == '2':
            cursor.execute(f"SELECT o.order_id, o.date_created, s.status_situation, b.book_id, b.title, b.price, "
                           f"u.user_id, CONCAT(u.user_name,' ',u.user_surname), u.user_email, u.user_phone, "
                           f"COALESCE(CONCAT(m.user_name,' ', m.user_surname), 'ніхто не розглядав !') FROM "
                           f"order_book o LEFT JOIN order_status s ON (o.status_id = s.status_id) LEFT JOIN book b ON "
                           f"(o.book_id = b.book_id) LEFT JOIN users u ON (o.user_id = u.user_id) LEFT JOIN users m "
                           f"ON (o.manager_id = m.user_id) WHERE s.status_id = 2 AND o.manager_id = '{managerID}';")
            result2 = cursor.fetchall()
            if not cursor.rowcount:
                print("Схоже, у вас немає активних замовлень : (")
            else:
                print_orders(result2)
                order_to_close = input("Введіть, будь ласка, ID замовлення, де клієнт вже купив та отримав книгу: ")
                try:
                    cursor.execute(f"UPDATE order_book SET status_id = 3 WHERE order_id = '{order_to_close}' AND "
                                   f"manager_id = '{managerID}'")
                    cursor.fetchall()
                    if not cursor.rowcount:
                        print("Схоже, Ви Ввели ID замовлення, якого не існує або немає в системі. Спробуйте пізніше.")
                    else:
                        mydb.commit()
                        print("Готово!")
                except:
                    print("Схоже, сталася помилка. Можливо, ви помилилися номером ID замовлення. Спробуйте пізніше")
        elif choice == "3":
            cursor.execute(
                "SELECT o.order_id, o.date_created, s.status_situation, b.book_id, b.title, b.price, u.user_id, "
                "CONCAT(u.user_name,' ',u.user_surname), u.user_email, u.user_phone, COALESCE(CONCAT(m.user_name,' ',"
                "m.user_surname), 'ніхто не розглядав !') FROM order_book o LEFT JOIN order_status s ON ("
                "o.status_id = s.status_id) LEFT "
                "JOIN book b ON (o.book_id = b.book_id) LEFT JOIN users u ON (o.user_id = u.user_id) LEFT JOIN "
                "users m ON (o.manager_id = m.user_id) WHERE o.manager_id IS NULL;")
            result3 = cursor.fetchall()
            print_orders(result3)
            order_to_work = input("Введіть, будь ласка, ID замовлення, яке бажаєте опрацювати: ")
            try:
                cursor.execute(
                    f"UPDATE order_book SET manager_id = '{managerID}' WHERE manager_id IS NULL AND order_id = '{order_to_work}'")
                cursor.fetchall()
                mydb.commit()
                cursor.execute(f"SELECT CONCAT(u.user_name,' ', u.user_surname), u.user_email, u.user_phone, b.title, "
                               f"b.price FROM order_book o JOIN users u ON o.user_id = u.user_id JOIN book b ON "
                               f"o.book_id = b.book_id WHERE o.order_id = '{order_to_work}'")
                result4 = cursor.fetchall()
                print(f"\tІм я та прізвище користувача - {result4[0][0]}")
                print(f"його пошта - {result4[0][1]}")
                print(f"його номер телефону - {result4[0][2]}")
                print(f"книга, яку він замовив - {result4[0][3]}, її ціна - {result4[0][4]}")
                print("\tВдалого спілкування!:)")
            except:
                print(unf_error_2)
        elif choice == "4":
            cursor.execute(
                "SELECT o.order_id, o.date_created, s.status_situation, b.book_id, b.title, b.price, u.user_id, "
                "CONCAT(u.user_name,' ',u.user_surname), u.user_email, u.user_phone, COALESCE(CONCAT(m.user_name,' ',"
                "m.user_surname), 'ніхто не розглядав !') FROM order_book o LEFT JOIN order_status s ON ("
                "o.status_id = s.status_id) LEFT "
                "JOIN book b ON (o.book_id = b.book_id) LEFT JOIN users u ON (o.user_id = u.user_id) LEFT JOIN "
                "users m ON (o.manager_id = m.user_id) WHERE s.status_id = 2 ORDER BY o.order_id;")
            result5 = cursor.fetchall()
            print_orders(result5)
            order_to_close = input("Введіть, будь ласка, ID замовлення, яке клієнт скасував (або відмовився "
                                   "отримувати книгу): ")
            try:
                cursor.execute(f"UPDATE order_book SET status_id = 1 WHERE order_id = '{order_to_close}'")
                cursor.fetchall()
                mydb.commit()
                print("Готово!")
            except:
                print(unf_error_2)
        else:
            print(opt_er)
        choice = help_chc()


# ВНЕСЕННЯ ЗАМОВЛЕННЯ ДО БД
def create_order(userID, bookID, cursor):
    cursor.execute(
        f"INSERT INTO order_book(date_created, status_id, book_id, user_id) VALUES(CURDATE(), 2, '{bookID}', '{userID}')")
    mydb.commit()


# СТВОРЕННЯ ЗАМОВЛЕННЯ
def make_order(user_id, cursor):
    book_id = input(" Введіть, будь ласка, ID книги, яку бажаєте замовити: ")
    try:
        cursor.execute(f"SELECT title, price FROM book WHERE book_id = '{book_id}'")
        book_sql = cursor.fetchall()
        print(f" Ви обрали книжку '{book_sql[0][0]}', ціна - {book_sql[0][1]}")
        confirm = input("Натисніть '1', щоб підтвердити, або будь-яку іншу клавішу, щоб скасувати\n")
        if confirm == "1":
            create_order(user_id, book_id, cursor)
            print(" Вітаємо! Ви здійснили замовлення. Наш менеджер зв'яжеться з Вами найближчим часом.")
        else:
            print(" Ви скасували замовлення.")
            return
    except IndexError:
        print("Схоже, ви ввели ID книги, якої не існує або немає в наявності. Спробуйте ще раз.")
        return make_order(user_id, cursor)
    except:
        print(unf_error)
        return
