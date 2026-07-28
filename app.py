from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)

def get_connection():
    return pymysql.connect(
        host="mysql",
        user="root",
        password="root123",
        database="flaskdb"
    )

@app.route("/")
def index():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Create users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100),
            password VARCHAR(100)
        )
        """)

        # Insert default user if table is empty
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.execute("""
            INSERT INTO users(username,password)
            VALUES('admin','admin123')
            """)
            conn.commit()

        # Check login
        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cursor.fetchone()

        if user:

            # Get all employees
            cursor.execute("SELECT * FROM employees")
            employees = cursor.fetchall()

            cursor.close()
            conn.close()

            return render_template(
                "dashboard.html",
                username=username,
                employees=employees
            )

        else:
            cursor.close()
            conn.close()
            return "<h2>Invalid Username or Password</h2>"

    except Exception as e:
        return str(e)


@app.route("/add", methods=["POST"])
def add_employee():

    name = request.form["name"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO employees(name) VALUES(%s)",
        (name,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE id=%s",
        (id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")

@app.route("/edit/<int:id>")
def edit(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM employees WHERE id=%s",
        (id,)
    )

    employee = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "edit.html",
        employee=employee
    )


@app.route("/update/<int:id>", methods=["POST"])
def update(id):

    name = request.form["name"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE employees SET name=%s WHERE id=%s",
        (name, id)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

