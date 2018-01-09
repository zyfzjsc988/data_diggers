from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# MONGO_URL='mongodb://data_diggers:data_diggers@cluster0-shard-00-00-07rsk.mongodb.net:27017,cluster0-shard-00-01-07rsk.mongodb.net:27017,cluster0-shard-00-02-07rsk.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin'
MONGO_URL = 'mongodb://data_diggers:data_diggers@cluster0-shard-00-00-07rsk.mongodb.net:27017,cluster0-shard-00-01-07rsk.mongodb.net:27017,cluster0-shard-00-02-07rsk.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin'
client = MongoClient(MONGO_URL)
db = client.data_diggers
collection = db.finalCities


@app.route('/db')
def dbrequest():
    aa = str(collection.find_one())
    return aa


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/request', methods=['POST'])
def makerequest():
    currentResult = collection.find_one()
    gender = request.form['Gender']
    age = request.form['Age']
    region = request.form['Region']
    employment = request.form['Employment']
    print(request.form)
    # cityName = calculatecity(gender, age, region, employment)
    return render_template('home.html', cityName=currentResult['city_name'])


if __name__ == '__main__':
    app.run()


def calculatecity(gender, age, region, employment):

    return 'True'
