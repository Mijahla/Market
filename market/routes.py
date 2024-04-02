from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/")
@app.route('/home')#decorators are like functions that execute before the actual function itself
def home_page():
    return render_template('home.html')
#Creating a new route to send data from this route to our html
@app.route('/market', methods=['GET','POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        #Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        #filter the purchased item based on the value
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object: #to access each user field
            #for budget warning
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f'Congratulations!! You purchased {p_item_object.name} for {p_item_object.price}$', category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}", category='danger')
        #Sell Item Logic
        sold_item = request.form.get('sold_item')  
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)  
                flash(f'Congratulations!! You sold {s_item_object.name} back to market! ', category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')
    


        return redirect(url_for('market_page'))
    
    if request.method == "GET":
        #to pass multiple values/info    
        items = Item.query.filter_by(owner = None) #returns all the items stored in the database
        owned_items = Item.query.filter_by(owner=current_user.id)
    return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)#To make it accessible from html template

#New route for the register page
@app.route('/register', methods=['GET','POST']) #to allow routes to handle post requests
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():# TO make sure that the user has clicked on the submit button and meets certain requirements
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created successfully! You are now logged in as {user_to_create.username}', category='success')

        return redirect(url_for('market_page'))#sends to the market route
    #To check for errors during the data input field
    if form.errors!= {}: #if there are no errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user:{err_msg}', category = 'danger')#To display messages inside html template
    return render_template('register.html', form=form)

#For creating login page
@app.route('/login', methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit(): #when all the info is valid and when submit button is entered
        # to make sure that the user exists and the password is correct
        attempted_user = User.query.filter_by(username=form.username.data).first() #.first grabs the object
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
            ):
                login_user(attempted_user)
                flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
                return redirect(url_for('market_page'))
        else:
            flash(f'Username and password do not match! Please try again', category='danger')
    return render_template('login.html', form=form)

#For log out button
@app.route('/logout')
def logout_page():
    logout_user()
    flash(f'You have been logged out!', category='info')
    #To redirect to home page after logging out
    return redirect(url_for('home_page'))
