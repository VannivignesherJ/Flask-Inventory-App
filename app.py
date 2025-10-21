from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="inventory_db2"
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    cursor.execute("""
        SELECT pm.movement_id, p.name AS product_name, 
               l1.name AS from_location, l2.name AS to_location, pm.qty
        FROM ProductMovement pm
        LEFT JOIN Product p ON pm.product_id = p.product_id
        LEFT JOIN Location l1 ON pm.from_location = l1.location_id
        LEFT JOIN Location l2 ON pm.to_location = l2.location_id
    """)
    movements = cursor.fetchall()
    return render_template('report.html', movements=movements)


@app.route('/add_movement', methods=['GET', 'POST'])
def add_movement():
    cursor.execute("SELECT * FROM Product")
    products = cursor.fetchall()
    cursor.execute("SELECT * FROM Location")
    locations = cursor.fetchall()

    if request.method == 'POST':
        product_id = request.form['product_id']
        from_loc = request.form['from_location']
        to_loc = request.form['to_location']
        qty = request.form['qty']

        cursor.execute("""
            INSERT INTO ProductMovement (product_id, from_location, to_location, qty)
            VALUES (%s, %s, %s, %s)
        """, (product_id, from_loc, to_loc, qty))
        db.commit()
        return redirect('/')

    return render_template('add_movement.html', products=products, locations=locations)


@app.route('/edit_movement/<int:id>', methods=['GET', 'POST'])
def edit_movement(id):
    cursor.execute("SELECT * FROM ProductMovement WHERE movement_id=%s", (id,))
    movement = cursor.fetchone()

    cursor.execute("SELECT * FROM Product")
    products = cursor.fetchall()
    cursor.execute("SELECT * FROM Location")
    locations = cursor.fetchall()

    if request.method == 'POST':
        product_id = request.form['product_id']
        from_loc = request.form['from_location']
        to_loc = request.form['to_location']
        qty = request.form['qty']

        cursor.execute("""
            UPDATE ProductMovement 
            SET product_id=%s, from_location=%s, to_location=%s, qty=%s 
            WHERE movement_id=%s
        """, (product_id, from_loc, to_loc, qty, id))
        db.commit()
        return redirect('/')

    return render_template('edit_movement.html', movement=movement, products=products, locations=locations)


@app.route('/delete_movement/<int:id>')
def delete_movement(id):
    cursor.execute("DELETE FROM ProductMovement WHERE movement_id=%s", (id,))
    db.commit()
    return redirect('/')


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_id = request.form['product_id']
        name = request.form['name']
        description = request.form['description']

        cursor.execute("""
            INSERT INTO Product (product_id, name, description)
            VALUES (%s, %s, %s)
        """, (product_id, name, description))
        db.commit()
        return redirect('/')

    return render_template('add_product.html')


@app.route('/add_location', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        location_id = request.form['location_id']
        name = request.form['name']

        cursor.execute("""
            INSERT INTO Location (location_id, name)
            VALUES (%s, %s)
        """, (location_id, name))
        db.commit()
        return redirect('/')

    return render_template('add_location.html')


if __name__ == '__main__':
    app.run(debug=True)
