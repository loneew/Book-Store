from flask import Flask, render_template, url_for, request, redirect
from command.authorization_command import Authorization
from command.catalog_command import ShowCatalog
from command.register_command import Register
from command.take_book_command import TakeBook
from command.using_books_command import ShowBooks

app = Flask(__name__)
app.secret_key = 'user'


@app.route('/')  # головна сторінка
def home():
    return render_template("home.html")


@app.route('/register', methods=['GET', 'POST'])  # реєстрація
def register():
    if request.method == 'POST':
        result = Register(request).execute()
        if result[0]:
            return render_template("profile.html")
        else:
            return render_template("error.html", error_text=result[2])
    else:
        return render_template("register.html")


@app.route('/authorization', methods=['GET', 'POST'])  # авторизація
def authorization():
    if request.method == 'POST':
        result = Authorization(request).execute()
        if result[0]:
            if result[1] == 1:
                return redirect('profile')
            else:
                return redirect('admin')
        else:
            return render_template("error.html", error_text=result[2])
    else:
        return render_template("authorization.html")


@app.route('/profile', methods=['GET', 'POST'])  # профіль
def profile():
    if request.method == "GET":
        return render_template("profile.html")
    elif request.method == "POST":
        action = request.form.get('action')
        if action == 'catalog':
            return redirect(url_for('catalog'))
        if action == 'take_book':
            return redirect(url_for('order'))
        if action == 'view_books':
            return redirect(url_for('mybook'))
    return redirect(url_for('profile'))


@app.route('/profile/catalog')
def catalog():
    result = ShowCatalog().execute()
    if result[0]:
        return render_template('catalog.html', page_title='Каталог книжок', books=result[1])
    else:
        return render_template("error.html", error_text=result[2])


@app.route('/profile/order', methods=['GET', 'POST'])
def order():
    result = ShowCatalog().execute()
    if result[0]:
        if request.method == 'POST':
            result_2 = TakeBook(request).execute()
            if result_2[0]:
                return render_template('text.html', text=result_2[2])
            else:
                return render_template('error.html', error_text=result_2[2])
        else:
            return render_template('order.html', books=result[1])
    else:
        return render_template("error.html", error_text=result[2])


@app.route('/profile/mybook')
def mybook():
    result = ShowBooks().execute()
    if result[0]:
        return render_template('catalog.html', page_title='Книжки, які ви читаєте', books=result[1])
    else:
        return render_template("error.html", error_text=result[2])


@app.route('/admin', methods=['GET', 'POST'])  # адміністратор
def admin():
    if request.method == "GET":
        return render_template("admin.html")
    elif request.method == "POST":
        action = request.form.get('action')
        if action == 'catalog_filling':
            return redirect(url_for('catalog_filling'))
        if action == 'accept_order':
            return redirect(url_for('accept_order'))
        if action == 'readers_page':
            return redirect(url_for('readers_page'))
    return redirect(url_for('admin'))


@app.route('/admin/catalog_filling')
def catalog_filling():
    return render_template("text.html", text="Not ready yet")


@app.route('/admin/accept_order')
def accept_order():
    return render_template("text.html", text="Not ready yet")


@app.route('/admin/readers_page')
def readers_page():
    return render_template("text.html", text="Not ready yet")


def launch():
    app.run(debug=True)
