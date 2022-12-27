import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, date

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite3'
app.config['SECRET_KEY'] = "random string"
 
db = SQLAlchemy(app)
 
# ...create table 
class Books(db.Model):
    id = db.Column('book_id', db.Integer, primary_key = True)
    book_name = db.Column(db.String(50))
    author = db.Column(db.String(50))
    year_published= db.Column(db.Integer)
    b_type = db.Column(db.Integer)
    books = db.relationship('Loans', backref='books')
    is_active = db.Column(db.String(20))


    def __init__(self, book_name, author, year_published, b_type,is_active):
        self.book_name = book_name
        self.author = author
        self.year_published = year_published
        self.b_type = b_type
        self.is_active = is_active
        

class Customers(db.Model):
    id = db.Column('customer_id', db.Integer, primary_key = True)
    customer_name = db.Column(db.String(50))
    city= db.Column(db.String(50))
    cust_age= db.Column( db.Integer)
    customers = db.relationship('Loans', backref='customers')
    is_active = db.Column(db.String(20))

    def __init__(self, customer_name, city, cust_age,is_active):
        self.customer_name = customer_name
        self.city = city
        self.cust_age = cust_age
        self.is_active = is_active


class Loans(db.Model):
    loan_id = db.Column('loan_id', db.Integer, primary_key = True)
    book_id = db.Column( db.Integer,db.ForeignKey('books.book_id'))
    customer_id= db.Column( db.Integer,db.ForeignKey('customers.customer_id'))
    loandate = db.Column(db.Date)#switch to time
    returndate = db.Column(db.Date)#switch to time
    is_active = db.Column(db.String(20))


    def __init__(self, loandate, returndate,book,customer,is_active):
        self.loandate = loandate
        self.returndate = returndate
        self.book_id= book
        self.customer_id= customer
        self.is_active = is_active





@app.route('/books/<id>', methods = ['GET', 'POST','DELETE', 'PUT'])
@app.route('/books/', methods = ['GET', 'POST','DELETE', 'PUT'])
def crud_books(id=-1):
    if request.method == 'GET':
        res=[]
        for book in Books.query.all():
            res.append({"book_name":book.book_name,
            "author":book.author,
            "year_published":book.year_published,
             "b_type": book.b_type,
             "id":book.id,
             "is_active":book.is_active})
        return  (json.dumps(res))
    if request.method == 'POST':
        request_data = request.get_json()
        book_name = request_data['book_name']
        author = request_data['author']
        year_published = request_data['year_published']
        b_type = request_data['b_type']
        is_active = request_data['is_active']
        new_book= Books(book_name,author, year_published,b_type,is_active)
        db.session.add (new_book)
        db.session.commit()
        return "A New Book Was Created."
    if request.method == 'DELETE':
        del_book= Books.query.get(id)
        db.session.delete(del_book)
        db.session.commit()
        return  {"msg":"row deleted"}
    if request.method == 'PUT':
        request_data = request.get_json()
        update_book = Customers.query.get(id)
        if update_book:
            is_active = request.json['is_active']
            db.session.commit()
        return  {"msg":"row updated"}   



# CRUD customers- read
@app.route('/cust/<id>', methods = ['GET', 'POST','DELETE', 'PUT'])
@app.route('/cust/', methods = ['GET', 'POST','DELETE', 'PUT'])
def crud_customers(id=-1):
    if request.method == 'GET':
        res=[]
        for cust in Customers.query.all():
            res.append({"customer_name":cust.customer_name,"city":cust.city,"cust_age":cust.cust_age,"id":cust.id,"is_active":cust.is_active})
        return  (json.dumps(res))
    if request.method == 'POST':
        request_data = request.get_json()
        customer_name = request_data['customer_name']
        city = request_data['city']
        cust_age = request_data['cust_age']
        is_active = request_data['is_active']
        newcust= Customers(customer_name, city, cust_age,is_active)
        db.session.add (newcust)
        db.session.commit()
        return "A New costumer Was Created."
    if request.method == 'DELETE':
        del_cust= Customers.query.get(id)
        db.session.delete(del_cust)
        db.session.commit()
        return  {"msg":"row deleted"}
    if request.method == 'PUT':
        request_data = request.get_json()
        update_cust = Customers.query.get(id)
        if update_cust:
            is_active = request.json['is_active']
            db.session.commit()
        return  {"msg":"row updated"}        



# # crud - Loans
@app.route('/loans/<id>',methods = ['GET', 'POST','DELETE', 'PUT'])
@app.route('/loans/',methods = ['GET', 'POST','DELETE', 'PUT'])
def crud_loans(id=-1): 
    if request.method == 'GET':
        res=[]
        for loan in Loans.query.all():
            res.append({"loan_id":loan.loan_id,
                        "customer_id":loan.customer_id,
                        "book_id":loan.book_id,
                        "b_type":loan.books.b_type,
                        "book_name":loan.books.book_name,
                        "loandate":loan.loandate.strftime("%Y-%m-%d"),
                        "returndate":loan.returndate.strftime("%Y-%m-%d"),
                        "is_active":loan.is_active,                   
                        "customer_name":loan.customers.customer_name
                        })
        return (json.dumps(res))   

    if request.method == 'POST': 
        request_data = request.get_json()
        customer_id = request_data["customer_id"]
        book_id = request_data["book_id"]
        loandate = request_data["loandate"]
        print(loandate)
        loandate_date = datetime.strptime(loandate, '%Y-%m-%d')
        print(loandate_date)
        returndate = request_data["returndate"]
        print(returndate)
        returndate_date = datetime.strptime(returndate, '%Y-%m-%d')
        print(returndate_date)
        is_active = request_data["is_active"]
        new_loan= Loans(loandate_date, returndate_date, book_id, customer_id, is_active)
        db.session.add(new_loan)
        db.session.commit()
        return {"msg":"Loan was added"}

    if request.method == 'PUT':
            request_data = request.get_json()
            upd_loan = Loans.query.get(id)
            if upd_loan:
                upd_loan.is_active =request_data["is_active"]
                db.session.commit()
            return {"msg":"The book returned"}


@app.route('/')
def hello():
    return 'Welcome to the library!!!!!!!!!'
 
if __name__ == '__main__':
    with app.app_context():db.create_all()
    app.run(debug = True)