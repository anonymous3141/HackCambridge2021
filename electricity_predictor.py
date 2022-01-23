import pickle

def elec_predict(weather_and_date_data):
    # Pandas dataframe input
    model = pickle.load(open("electricity_model.pickle","rb"))
    return model.predict(weather_and_date_data)[0]

#print(predict([63.4 , 64.72, 59.12, 60.37, 58.33, 59.15, 58.93]))
