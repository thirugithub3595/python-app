from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)


def get_connection():
    return pymysql.connect(
        host='mysql',
        user='root',
        password='root123',
        database='flaskdb'
    )


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Users table for login
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE,
            password VARCHAR(100)
        )
    ''')

    # Employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100)
        )
    ''')

    # Insert default admin user if it doesn't exist
    cursor.execute(
        'SELECT * FROM users WHERE username=%s',
        ('admin',)
    )

    admin = cursor.fetchone()

    if not admin:
        cursor.execute(
            'INSERT INTO users(username, password) VALUES(%s, %s)',
            ('admin', 'admin123')
        )

    conn.commit()
    cursor.close()
    conn.close()


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username'].strip()
    password = request.form['password'].strip()

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            'SELECT id, username FROM users WHERE username=%s AND password=%s',
            (username, password)
        )

        user = cursor.fetchone()
        print('LOGIN DEBUG:', username, password, user)

        cursor.close()
        conn.close()

        if user:
            return redirect('/login-success')

        return '<h2>Invalid Username or Password</h2>'

    except Exception as e:
        return str(e)


@app.route('/add', methods=['POST'])
def add_employee():
    name = request.form['name']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO employees(name) VALUES(%s)',
        (name,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/login-success')


@app.route('/login-success')
def login_success():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT id, name FROM employees')
    employees = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        'dashboard.html',
        username='admin',
        employees=employees
    )


@app.route('/delete/<int:id>')
def delete(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        'DELETE FROM employees WHERE id=%s',
        (id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/login-success')


@app.route('/edit/<int:id>')
def edit(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        'SELECT id, name FROM employees WHERE id=%s',
        (id,)
    )

    employee = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        'edit.html',
        employee=employee
    )


@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form['name']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        'UPDATE employees SET name=%s WHERE id=%s',
        (name, id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/login-success')


if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=5000)
