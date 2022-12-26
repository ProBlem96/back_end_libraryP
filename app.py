import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import date

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


    def __init__(self, book_name, author, year_published, b_type):
        self.book_name = book_name
        self.author = author
        self.year_published = year_published
        self.b_type = b_type
        

class Customers(db.Model):
    id = db.Column('customer_id', db.Integer, primary_key = True)
    customer_name = db.Column(db.String(50))
    city= db.Column(db.String(50))
    cust_age= db.Column( db.Integer)
    customers = db.relationship('Loans', backref='customers')

    def __init__(self, customer_name, city, cust_age):
        self.customer_name = customer_name
        self.city = city
        self.cust_age = cust_age

class Loans(db.Model):
    loan_id = db.Column('loan_id', db.Integer, primary_key = True)
    book_id = db.Column( db.Integer,db.ForeignKey('books.book_id'))
    customer_id= db.Column( db.Integer,db.ForeignKey('customers.customer_id'))
    loandate = db.Column(db.String(50))#switch to time
    returndate = db.Column(db.Integer)#switch to time

    def __init__(self, loandate, returndate=0,book=0,customer=0):
        self.loandate = loandate
        self.returndate = returndate
        self.book_id= book
        self.customer_id= customer





@app.route('/books/<id>', methods = ['GET', 'POST','DELETE', 'PUT'])
@app.route('/books/', methods = ['GET', 'POST','DELETE', 'PUT'])
def crud_books(id=-1):
    if request.method == 'GET':
        res=[]
        for book in Books.query.all():
            res.append({"book_name":book.book_name,"author":book.author,"year_published":book.year_published, "b_type": book.b_type,"id":book.id})
        return  (json.dumps(res))
    if request.method == 'POST':
        request_data = request.get_json()
        book_name = request_data['book_name']
        author = request_data['author']
        year_published = request_data['year_published']
        b_type = request_data['b_type']
        newBook= Books(book_name,author, year_published,b_type)
        db.session.add (newBook)
        db.session.commit()
        return "A New Book Was Created."
    if request.method == 'DELETE':
        del_book= Books.query.get(id)
        db.session.delete(del_book)
        db.session.commit()
        return  {"msg":"row deleted"}
    if request.method == 'PUT':
        update_book = Books.query.get(id)
        book_name = request.json['book_name']
        author = request.json['author']
        year_published = request.json['year_published']
        b_type = request.json['b_type']
        update_book.book_name = book_name
        update_book.author = author
        update_book.year_published = year_published
        update_book.b_type = b_type
        db.session.commit()
        return  {"msg":"row updated"}



# CRUD customers- read
@app.route('/cust/<id>', methods = ['GET', 'POST','DELETE', 'PUT'])
@app.route('/cust/', methods = ['GET', 'POST','DELETE', 'PUT'])
def crud_customers(id=-1):
    if request.method == 'GET':
        res=[]
        for cust in Customers.query.all():
            res.append({"customer_name":cust.customer_name,"city":cust.city,"cust_age":cust.cust_age,"id":cust.id})
        return  (json.dumps(res))
    if request.method == 'POST':
        request_data = request.get_json()
        customer_name = request_data['customer_name']
        city = request_data['city']
        cust_age = request_data['cust_age']
        newcust= Customers(customer_name, city, cust_age)
        db.session.add (newcust)
        db.session.commit()
        return "A New costumer Was Created."
    if request.method == 'DELETE':
        del_cust= Customers.query.get(id)
        db.session.delete(del_cust)
        db.session.commit()
        return  {"msg":"row deleted"}
    if request.method == 'PUT':
        update_cust = Customers.query.get(id)
        customer_name = request.json['customer_name']
        city = request.json['city']
        cust_age = request.json['cust_age']
        update_cust.customer_name = customer_name
        update_cust.city = city
        update_cust.cust_age = cust_age
        db.session.commit()
        return  {"msg":"row updated"}        



# # crud - Loans
@app.route('/loans/<id>', methods = ['GET', 'POST','DELETE', 'PUT'])
@app.route('/loans/', methods = ['GET', 'POST','DELETE', 'PUT'])
def crud_loans(id=-1):
    if request.method == 'GET':
        all_loans=[]
        for loan in Loans.query.all():
            if loan.returndate == 0:
                all_loans.append({'loandate':loan.loandate,'returndate':loan.returndate, "customer_name":loan.customers.customer_name , "book_name":loan.books.book_name})
        return json.dumps(all_loans)
    if request.method == 'POST': 
        #loan a book
        request_data = request.get_json()
        customer_name = request_data['customer_name']
        book_name = request_data['book_name']
        customer_id = ""
        book_id = ""
        # get customer id by name
        for customer in Customers.query.all():
            if customer.customer_name == customer_name:
                customer_id = customer.id
                break
        #get book id by name book
        for book in Books.query.all():
            if book.book_name == book_name:
                book_id = book.id
                break
        loandate = date.today()
        returndate = 0
        new_loan = Loans(loandate,returndate,book_id,customer_id)
        db.session.add (new_loan) 
        db.session.commit()
        return "A New loan was applied."
    # if request.method == 'DELETE':
    #     del_loan = Loans.query.get(id)
    #     db.session.delete(del_loan)
    #     db.session.commit()
    #     return  {"msg":"row deleted"}
    if request.method == 'PUT':
        # return a book- i tried to...
        update_loan = Loans.query.get(id)
        request_data = request.get_json()
        customer_name = request_data['customer_name']
        book_name = request_data['book_name']
        update_loan.returndate = request_data["returndate"]
        db.session.commit()
        return {"return_date":update_loan.return_date}


# Tried to make a late loans by that but it's wasn't complete :(
@app.route('/lateloans/', methods = ['PUT'])
def late_loans():
    if request.method == 'PUT':
        all_late_loans=[]
        for loan in Loans.query.all():
            if loan.returndate != 0:
                continue
            days_num = 0
            if Loans.query.get(loan.book_id).b_type == 1:
                days_num = 10
            elif Loans.query.get(loan.book_id).b_type == 2:
                days_num = 5
            elif Loans.query.get(loan.book_id).b_type == 3:
                days_num = 2
            now = date.today()
            if days_num + loan.loandate < now: # check if compatible types
                all_late_loans.append({"book_name":Loans.query.get(loan.book_id).book_name,"customer_name":Loans.query.get(loan.customer_id).customer_name,"loandate":loan.loandate})
        return json.dumps(all_late_loans)

            



@app.route('/')
def hello():
    return 'Welcome to the library!'
 
if __name__ == '__main__':
    with app.app_context():db.create_all()
    app.run(debug = True)