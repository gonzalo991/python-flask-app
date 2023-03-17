from flask import Flask, redirect, render_template, request, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder=template_dir)


# Rutas de la aplicacion
@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute('SELECT * FROM users')
    myresult = cursor.fetchall()

    # Convertir los datos a diccionario
    insertObject = []
    columNames = [column[0] for column in cursor.description]

    for record in myresult:
        insertObject.append(dict(zip(columNames, record)))

    cursor.close()

    return render_template('index.html', data=insertObject)

# Ruta para guardar usuarios en la base de datos


@app.route('/user', methods=['POST'])
def addUser():
    Username = request.form['username']
    Nombre = request.form['name']
    Contraseña = request.form['password']

    if (Username and Nombre and Contraseña):
        cursor = db.database.cursor()
        sql = 'insert into users (Username,Nombre,Contraseña) values (%s,%s,%s)'
        data = (Username, Nombre, Contraseña)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))


@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = 'delete from users where id = %s'
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))


@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    Username = request.form['username']
    Nombre = request.form['name']
    Contraseña = request.form['password']

    if Username and Nombre and Contraseña:
        cursor = db.database.cursor()
        sql = "update users SET Username = %s, Nombre = %s, Contraseña = %s WHERE id = %s"
        data = (id, Username, Nombre, Contraseña)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=3000)
