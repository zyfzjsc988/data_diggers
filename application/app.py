from flask import Flask, render_template, request
from pymongo import MongoClient
import pandas as pd
import numpy as np
from sklearn import preprocessing

app = Flask(__name__)

MONGO_URL = 'mongodb://data_diggers:data_diggers@cluster0-shard-00-00-07rsk.mongodb.net:27017,cluster0-shard-00-01-07rsk.mongodb.net:27017,cluster0-shard-00-02-07rsk.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin'
client = MongoClient(MONGO_URL)
db = client.data_diggers

# calculate rank
def calculate_user_rank(weights, pearson, df):
    multiplier = pearson.copy()
    for key in multiplier.keys():
        if key == 'number_of_universities_per_person':
            multiplier[key] = multiplier[key] * int(weights['Education'])
        elif key == 'pubs_number_per_person':
            multiplier[key] = multiplier[key] * int(weights['Entertainment'])
        elif key == 'total_jobs_per_person':
            multiplier[key] = multiplier[key] * int(weights['Jobs'])
        elif key == 'school_number_per_person':
            multiplier[key] = multiplier[key] * int(weights['Schools'])
        elif key == 'stations_number_per_person':
            multiplier[key] = multiplier[key] * int(weights['Connectivity'])
        elif key == 'hospitals_number_per_person':
            multiplier[key] = multiplier[key] * int(weights['Hospitals'])
        elif (key == 'frostday_peryear') or (key == 'rainfall_permon') or (key == 'summerday_ave_temperature') or (key == 'summernight_ave_temperature') or (key == 'sunshine_permon') or (key == 'winterday_ave_temperature') or (key == 'winternight_ave_temperature'):
            multiplier[key] = multiplier[key] * int(weights['Weather'])
        elif key == 'gva':
            multiplier[key] = multiplier[key] * int(weights['GVA'])
        elif key == 'house_price':
            multiplier[key] = multiplier[key] * int(weights['HousePrice'])
        elif key == 'population':
            multiplier[key] = multiplier[key] * int(weights['Population'])
        elif (key == 'road_traffic_2015') or (key == 'road_traffic_2016'):
            multiplier[key] = multiplier[key] * int(weights['RoadTraffic'])
        elif key == 'traffic_noise':
            multiplier[key] = multiplier[key] * int(weights['Noise'])
        elif key == 'unemployment':
            multiplier[key] = multiplier[key] * int(weights['Unemployment'])

    # calculate the ranking - with for loop
    df['result'] = 0
    for key in multiplier.keys():
        # to numbers
        df[key] = pd.to_numeric(df[key])
        multiplier[key] = float(multiplier[key])

        # calculate
        df['result'] = df['result'] + df[key] * multiplier[key]

    # sort result
    df = df.sort_values(['result'])

    return df


# normalization by z-score
def scaleColumns(df):
    print(df[:2])
    scaler = preprocessing.StandardScaler()
    cols_to_scale = list(df)
    for col in cols_to_scale:
        df[col] = pd.to_numeric(df[col])
        df[col] = pd.DataFrame(scaler.fit_transform(pd.DataFrame(df[col])), columns=[col])
    print(df[:2])
    return df

# function to calculate cities ranking
def calculatecity(userRequest):
    # read collection
    collection = db.finalCities
    cursor = collection.find()
    listOfData = [c for c in cursor]
    df = pd.DataFrame(listOfData)
    df = df.set_index('city_name')

    # remove unused columns
    df = df.drop(columns=['uk_region', 'region', '_id', 'happiness', 'latitude', 'longitude', 'sample'])
    df = df.fillna(0)

    # generate new normalized columns
    df['number_of_universities_per_person'] = df['number_of_universities'] / df['population']
    df['pubs_number_per_person'] = df['pubs_number'] / df['population']
    df['total_jobs_per_person'] = df['total_jobs'] / df['population']
    df['school_number_per_person'] = df['school_number'] / df['population']
    df['stations_number_per_person'] = df['stations_number'] / df['population']
    df['hospitals_number_per_person'] = df['hospitals_number'] / df['population']

    # remove old columns
    df = df.drop(['hospitals_number', 'pubs_number', 'stations_number', 'school_number', 'total_jobs',
                  'number_of_universities'], axis=1)

    df.to_csv('output.csv')

    # normalize
    # df = scaleColumns(df)

    # sort DataFrame alphabetically
    df.columns = [x.lower() for x in df.columns]
    df = df.sort_index(axis=1)

    # read weights
    collection = db.SurveyWeights
    cursor = collection.find()
    weightsList = [c for c in cursor]
    # factors = factors[0]
    # factors.pop('_id')
    # factors = {k.lower(): v for k, v in factors.items()}

    # read Pearson's correlation coefficients
    collection = db.pearsonr_correlation_coefficient
    cursor = collection.find()
    pearsonList = [c for c in cursor]
    pearson = pearsonList[0]
    pearson.pop('_id')
    # sort alphabetically
    pearson = {k.lower(): v for k, v in pearson.items()}
    # drop some keys
    pearson.pop('number_of_universities')
    pearson.pop('pubs_number')
    pearson.pop('total_jobs')
    pearson.pop('school_number')
    pearson.pop('stations_number')
    pearson.pop('hospitals_number')

    # sort Pearson's coefficients
    # factors_np = []
    # for key in sorted(factors.iterkeys()):
    #     factors_np.append(factors[key])
    # factors_np = np.asarray(factors_np)

    # check if there are different column names
    for i in pearson.keys():
        if i in df.columns.values:
            pass
        else:
            print(i)

    # calculate ranking using numpy
    # data = df.values
    # array = np.dot(data, factors_np)
    # print(type(array))
    # print(array)
    # df['result2'] = array
    # df = df.sort_values(['result2'])

    # calculate the ranking - with for loop
    # df['result'] = 0
    # for key in factors.keys():
    #     df[key] = pd.to_numeric(df[key])
    #     factors[key] = float(factors[key])
    #     df['result'] = df['result'] + df[key] * factors[key]
    # df = df.sort_values(['result'])

    # print
    # print(df.count(axis=1))
    # print('----------')
    # print(len(pearson))
    # df.to_csv('output.csv', columns=['result2'])

    df = calculate_user_rank(userRequest, pearson, df)

    # 3 best cities
    best = df[0:3]
    bestList = list(best.index)
    print(bestList)

    # 3 worst cities
    worst = df[-3:]
    worstList = list(worst.index)
    print(worstList)

    answer =  bestList + worstList
    return answer


@app.route('/')
def home():
    # calculatecity(1)
    return render_template('home.html')


@app.route('/request', methods=['POST'])
def makerequest():
    collection = db.finalCities
    currentResult = collection.find_one()
    # gender = request.form['Gender']
    # age = request.form['Age']
    # region = request.form['Region']
    # employment = request.form['Employment']

    # transform user request
    userRequest = request.form.to_dict()
    print(userRequest)

    # calculate rank according to user input
    cityList = calculatecity(userRequest)

    return render_template('result.html', bestOne=cityList[0], bestTwo=cityList[1], bestThree=cityList[2], worstThree=cityList[5], worstTwo=cityList[4], worstOne=cityList[3])


if __name__ == '__main__':
    app.run()
