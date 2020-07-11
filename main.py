from flask import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

# SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:hatriya2798@localhost/Meeraconsultant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receipt_no = db.Column(db.Integer)
    financial_year = db.Column(db.String(100))
    party_name = db.Column(db.String(200))
    address = db.Column(db.String(500))
    charges = db.Column(db.String(500))
    amount = db.Column(db.Float)
    date = db.Column(db.Date)
    total = db.Column(db.Float)

    def __init__(self, receipt_no, financial_year, party_name, address, charges, amount, date, total):
        self.receipt_no = receipt_no
        self.financial_year = financial_year
        self.party_name = party_name
        self.address = address
        self.charges = charges
        self.amount = amount
        self.date = date
        self.total = total


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/Invoice/<id>/', methods=['POST', 'GET'])
def invoice(id):
    all_data = Service.query.get(id)
    return render_template('Invoice.html', Service=all_data)


@app.route('/addinvoice')
def add_invoice():
    all_data = Service.query.all()
    return render_template('addinvoice.html', Service=all_data)


@app.route('/addinvoice', methods=['POST'])
def insert_invoice():
    if request.method == "POST":
        receipt_no = request.form["receipt_no"]
        financial_year = request.form["financial_year"]
        party_name = request.form["party_name"]
        address = request.form["address"]
        charges = request.form["charges"]
        amount = request.form["amount"]
        date = request.form["date"]
        total = amount
        my_data = Service(receipt_no, financial_year, party_name, address, charges, amount, date, total)
        db.session.add(my_data)
        db.session.commit()
        flash("Transaction Inserted Successfully")
        return redirect(url_for('add_invoice'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Service.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Deleted Successfully")

    return redirect(url_for('add_invoice'))


if __name__ == '__main__':
    app.run(debug=True)
