from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from datetime import datetime
import pickle
import matplotlib
import os

# Create your views here.

def home(request):
    if os.path.exists("user_input/static/user_input/graph.PNG"):
        os.remove("user_input/static/user_input/graph.PNG")
    
    return render(request, 'user_input/home.html')

def fetch_data(request):    

    if request.method == 'POST':
        if os.path.exists("user_input/static/user_input/graph.PNG"):
            os.remove("user_input/static/user_input/graph.PNG")

        if str('York') in str(request.POST['city']):  
            model = pickle.load(open('models/ny_model.pkl', 'rb'))

        elif str('Dallas') in str(request.POST['city']):
            model = pickle.load(open('models/tx_model_prophet.pkl', 'rb'))

        elif str('Mumbai') in str(request.POST['city']):
            model = pickle.load(open('models/mum_model.pkl', 'rb'))

        n_future = int(request.POST['time_frame'])  

        model_now = list(model.history_dates)[-1]
        model_now = model_now.strftime("%Y-%m-%d %H:%M")

        time_now = datetime.now().strftime("%Y-%m-%d %H:%51")

        d1 = datetime.strptime(model_now, '%Y-%m-%d %H:%M')
        d2 = datetime.strptime(time_now, '%Y-%m-%d %H:%M')
        diff = (d2 - d1).total_seconds() / 3600

        periods = int(diff) + n_future

        future_dates=model.make_future_dataframe(periods=periods, freq='H', include_history = False)
        prediction=model.predict(future_dates)
        preds = []

        for i in prediction.tail(n_future)['yhat'].values:
            preds.append(i)

        y_pred_future = np.array(preds)
        y_pred_future = [round(num, 1) for num in y_pred_future]

        if (n_future == 168):
            weeks = np.array_split(y_pred_future,7)
            max_in_days = [max(i) for i in weeks]
            min_in_days = [min(i) for i in weeks]
            avg = [np.mean(i) for i in weeks]

            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            i=days.index(datetime.today().strftime('%A')) 
            d1=days[i:] 
            d1.extend(days[:i])

            matplotlib.use('Agg')
            plt.figure(figsize=(11,6))
            plt.plot(d1, max_in_days, label='Peak temperatures', marker='.')
            plt.plot(d1, min_in_days, label='Lowest temperatures', marker='.')
            plt.plot(d1, avg, label='Avg. temperatures', marker='.')   
            plt.xticks(rotation = 25) 
            plt.ylabel('Temperature (°F)', fontsize=12)
            plt.title('From today until next week for '+request.POST["city"], fontsize=12)
            plt.grid()
            plt.legend()
            plt.savefig('user_input/static/user_input/graph.PNG')
        
        elif (n_future == 720):
            timestamps = pd.Series(pd.date_range(start = datetime.today(), periods=30, freq="D", tz ='US/East-Indiana')).tolist()
            month_days = []
            for i in timestamps:
                month_days.append(str(i)[5:10])

            days = np.array_split(y_pred_future,len(month_days))
            max_in_days = [max(i) for i in days]
            min_in_days = [min(i) for i in days]
            avg = [np.mean(i) for i in days]

            matplotlib.use('Agg')
            plt.figure(figsize=(11,6))
            plt.plot(month_days, max_in_days, label='Peak temperatures', marker='.')
            plt.plot(month_days, min_in_days, label='Lowest temperatures', marker='.')
            plt.plot(month_days, avg, label='Avg. temperatures', marker='.')   
            plt.xticks(rotation = 45) 
            plt.ylabel('Temperature (°F)', fontsize=12)
            plt.title('From today until next month for '+request.POST["city"], fontsize=12)
            plt.grid()
            plt.legend()
            plt.savefig('user_input/static/user_input/graph.PNG')

        else:
            timestamps = pd.Series(pd.date_range(start = datetime.now(), periods=24, freq="H", tz ='US/East-Indiana')).tolist()
            hours = []
            for i in timestamps:
                hours.append(str(i)[10:16])
            matplotlib.use('Agg')
            plt.figure(figsize=(11,6))
            plt.plot(hours, y_pred_future, marker='.')
            plt.xticks(rotation = 45) 
            plt.ylabel('Temperature (°F)', fontsize=12)
            plt.title('From now until tomorrow for '+request.POST["city"], fontsize=12)
            plt.grid()
            plt.savefig('user_input/static/user_input/graph.PNG')

    return render(request, 'user_input/home.html')
