from flask import Flask, render_template, request, url_for, redirect
# from flask_sqlalchemy import SQLAlchemy
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression

app = Flask(__name__)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# db = SQLAlchemy(app)

# class House(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     city = db.Column(db.String(100), nullable=False)
#     price = db.Column(db.Float, nullable=False)
#     bedroom = db.Column(db.Integer)

#     def __repr__(self):
#         return f"<House {self.city}>"


# @app.route("/")
# def home():
#     houses = House.query.all()
#     return render_template("index.html", houses=houses)

# # Route to update a house's details
# @app.route("/update/<int:id>", methods=["POST"])
# def update(id):
#     house = House.query.get(id)
#     if not house:
#         return f"House with ID {id} not found", 404

#     if request.method == "POST":
#         # Update the house with new values from the form
#         house.city = request.form['city']
#         house.price = request.form['price']
#         house.bedroom = request.form['bedroom']

#         # Commit the changes to the database
#         db.session.commit()

#         return redirect(url_for('home'))  # Redirect to home page after update

#     # If it's a GET request, render the update form
#     # return render_template("update.html", house=house)

# # Function to create the tables in the database
# @app.before_request
# def create_tables():
#     db.create_all()

# train data

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder


df=pd.read_csv("C:\\Users\\HP\\Downloads\\house_prices_india.csv")
# print(df)
# x=df['City'].tolist()
unique_cities = df["City"].unique()





# df=pd.read_csv("house_prices_india.csv")
le=LabelEncoder()
df["City"]=le.fit_transform(df["City"])




X=df[["City","Square Feet","Bedrooms","Bathrooms"]]
y=df["Price"]



X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

model=LinearRegression()
model.fit(X_train,y_train)


# pred=model.predict([[le.transform(["Delhi"])[0],2951,2,3]])




@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        selected_city = request.form['city']
        square_feet = int(request.form['square_feet'])
        bedrooms = int(request.form['bedrooms'])
        bathrooms = int(request.form['bathrooms'])
        
       
        pred_price = model.predict([[le.transform([selected_city])[0], square_feet, bedrooms, bathrooms]])
        
        predicted_price = int(pred_price[0])
        return render_template('index.html', cities=unique_cities, predicted_price=predicted_price)
    return render_template('index.html', cities=unique_cities)




# @app.route('/output')
# def output():
#     p=int(pred[0])
#     return render_template('index.html',y=pred)

if __name__ == "__main__":
    app.run(debug=True)
