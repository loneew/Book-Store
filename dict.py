import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="coursework"
)


unf_error = "Схоже, сталася непередбачувана помилка. Спробуйте пізніше."
unf_error_2 = "Схоже, сталася помилка. Спробуйте ще раз."
unf_error_3 = "Обрано некоректний варіант. Спробуйте ще раз."
unf_error_4 = "Неправильно введений логін або пароль! Спробуйте ще раз."
gdb = " Допобачення! Нехай щастить."
wlcm_1 = " Вітаємо! Ви успішно зареєструвалися у системі.\n"
wlcm_2 = " Вітаємо! Ви успішно увійшли у систему.\n"
opt_er = "Можливі опції: '1', '2', '3', '4', '5'. Спробуйте ще раз."
questn = "\tЩо бажаєте здійснити?"