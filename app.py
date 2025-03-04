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


 

df=pd.read_csv("data/house_prices_india.csv")

# df=pd.read_csv("C:\\Users\\HP\\Downloads\\house_prices_india.csv")
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
        
        predicted_price =f" {int(pred_price[0]):,}"
        return render_template('index.html', cities=unique_cities, predicted_price=predicted_price)
    return render_template('index.html', cities=unique_cities)


# @app.route('/output')
# def output():
#     p=int(pred[0])
#     return render_template('index.html',y=pred)

if __name__ == "__main__":
    app.run(debug=True)
