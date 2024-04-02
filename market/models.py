from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin

@login_manager.user_loader #from flask documentation
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin): #usermixin additional class which includes authentication etc
    id = db.Column(db.Integer(), primary_key=True) # so that flask identifies by the id nums
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    #Storing the password to avoid security risks 
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    #To allow users to own several items by creating relationship
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def prettier_budget(self): #inorder to add a comma in budget
        if len(str(self.budget)) >= 4:
            return  f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"

    @property #To announce that there is a new property and the function to return it back when user wants it
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        #receives the password argument and generates hash
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self, attempted_password): #To grab the password entered in login
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price
    
    def can_sell(self, item_obj):
        return item_obj in self.items
    
#Creating a model by inheriting from a class
class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True) # so that it can understand the unique models
    name = db.Column(db.String(length=30), nullable=False, unique=True) #Creating an instance of class Item 
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item{self.name}'
 

    def buy(self, user):
        self.owner = user.id #from models.py the id as foreign key
        #TO deduce the budget after the purchase
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()