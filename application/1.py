from flask import Flask,render_template
from pymongo import MongoClient

app = Flask(__name__)

# MONGO_URL='mongodb://data_diggers:data_diggers@cluster0-shard-00-00-07rsk.mongodb.net:27017,cluster0-shard-00-01-07rsk.mongodb.net:27017,cluster0-shard-00-02-07rsk.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin'
MONGO_URL= 'mongodb://data_diggers:data_diggers@cluster0-shard-00-00-07rsk.mongodb.net:27017,cluster0-shard-00-01-07rsk.mongodb.net:27017,cluster0-shard-00-02-07rsk.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin'
client = MongoClient(MONGO_URL)
db = client.data_diggers
collection = db.reference

@app.route('/db')
def hello_world():
    aa =str(collection.find_one())
    return aa


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()


