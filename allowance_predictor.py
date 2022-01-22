import pickle

def predict(past_week):
    # past week is 1d array
    model = pickle.load(open("allowance_model.pickle","rb"))
    return model.predict([past_week])[0]

#print(predict([63.4 , 64.72, 59.12, 60.37, 58.33, 59.15, 58.93]))
