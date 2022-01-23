from refresh_allowance_data import allowance_condition, HISTORY_LENGTH
import refresh_allowance_data
import numpy as np
import pickle


model = pickle.load(open("allowance_model.pickle","rb"))

def predict(past_week):
    # past week is 1d array
    return model.predict([past_week[-7:]])[0]

def predict_n_days_forward(n):
    allowance_condition.acquire()
    last_week = refresh_allowance_data.allowance_data_past_week[-7:]
    allowance_condition.release()
    result = []

    for i in range(n):
        next_day = predict(last_week)
        result.append(next_day)
        last_week = np.append(last_week[1:], next_day)

    return np.array(result)





# print(predict([63.4 , 64.72, 59.12, 60.37, 58.33, 59.15, 58.93]))
