from flask import Flask, render_template, redirect,session,request
from flask_sqlalchemy import SQLAlchemy
import pickle
app = Flask(__name__)
import sqlite3
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///MovieReviewSentiment.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)  # INITIALIZE THE DATABASE 

filename = 'sentiment.pkl'
classifier = pickle.load(open(filename, 'rb'))
trans = pickle.load(open('transform.pkl','rb'))


class MovieReviewSentiment(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    Review=db.Column(db.String(500),nullable=False)
    prediction=db.Column(db.String(20))
    

@app.route("/")
def index():
    return render_template('sentiments.html')
    # MR=MovieReviewSentiment(Review='Nice Movie',prediction='Positive')
    # db.session.add(MR)
    # db.session.commit()
    
@app.route('/result', methods=['POST','GET'])
def result():
    if request.method == 'POST':
        message = request.form['message']
        data = [message]
        vect = trans.transform(data).toarray()
        my_prediction = classifier.predict(vect)
        if my_prediction==1:
            rev='Positive'
        else:
            rev='Negative'
        entry=MovieReviewSentiment(Review=message,prediction=rev)
        db.session.add(entry)
        db.session.commit()
        return render_template('result.html', prediction=my_prediction)
    else:
        return render_template('result.html', prediction=1)

@app.route("/about")
def about():
    return "<p>This is about page</p>"

@app.route("/data")
def data():
    conn = sqlite3.connect('MovieReviewSentiment.db')
    c = conn.cursor()
    c.execute("SELECT * FROM movie_review_sentiment")
    data = c.fetchall()
    # Close the database connection
    conn.close()
    return render_template('data.html',data=data)



if __name__=="__main__":
    app.run(debug=True)