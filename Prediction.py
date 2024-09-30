import csv
import logging
import asyncio
import time
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn import preprocessing, svm

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression

import sys

from arduino_iot_cloud import ArduinoCloudClient
from email.message import EmailMessage
import smtplib
import ssl
email_sender = 'jploveslego101@gmail.com'
email_password = 'wrgl awoa mxvk vxkg'
email_receiver = 'joshpeyton04@gmail.com'
subject = 'Rain Prediction For The Next Hour'


DEVICE_ID = "159e0a92-82b5-4668-a2d3-5a44ceccc208"
SECRET_KEY = "erz8xIuEXjNH2ptRyIb0U8o0D"

#C:\Users\joshp\OneDrive\Documents\University\SIT225\Python Code

def setNum(n):
   global a
   a = n

def setNum_b(n):
   global b
   b = n

def setNum_c(n):
   global c
   c = n
   
y_data = []
def setY(y):
   global y_data
   y_data.append(y)

def clearY():
    global y_data
    
    y_data = []

def on_c_changed(client, value):
    t = time.time()
    d_time = datetime.fromtimestamp(t)
    i_time = int(round(d_time.hour + (d_time.minute/60)))

    if i_time > 8 and i_time < 19:
        r = client["rain"]
        h = client["humidity"]
        temp = client["temperature"]
        t = time.time()
        d_time = datetime.fromtimestamp(t)
        t = d_time.hour + (d_time.minute/60)       
        val = a + 1        
        setNum_b(t)
        if val == 1:
            setNum_c(t + 1)
        setNum(val)
        setY([r, h, temp, t])
        # print()
        #360
        #321
        # print(y_data)
        print(b, c)
        if b >= c:
            df = pd.DataFrame(y_data)
            print(df)
            prediction(r, h, temp, t, df)
            
            setNum(0)
            clearY()
    else:
        body = "Outside of prediction hours"

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        time.sleep(60*60)

def calculate_temp(dataframe, temperature, humidity, rain, hour, delta_type, val):
    x = np.array(dataframe[['humidity', 'temperature', 'rain']])
    y = np.array(dataframe[[delta_type]])
 
    model = LinearRegression().fit(x,y)

    r_sq = model.score(x, y)

    arr = np.array([[humidity, rain, temperature]], dtype=object)

    delta = model.predict(arr)    
    print(delta)
    delta = delta[0][0]   
    print(delta)
    

    if delta_type == "t_Delta":
        temperature = temperature + delta
        return temperature
    elif delta_type == "h_Delta":
        humidity = humidity + delta
        return humidity
    else:
        rain = rain + delta
        return rain
    
def higher_fuzzy_logic(rain_s, humidity, s):
    if rain_s > 200:
        if humidity > 85:
            s = "Very High Likelihood Of Rain"
        elif humidity > 70:
            s = "High Likelihood Of Rain"
        elif humidity > 55:
            s = "Moderate Likelihood Of Rain"
        else:
            s = "Moderate Likelihood Of Rain"

    elif rain_s > 170:
        if humidity > 85:
            s = "High Likelihood Of Rain"
        elif humidity > 70:
            s = "Moderate Likelihood Of Rain"
        elif humidity > 55:
            s = "Moderate Likelihood Of Rain"
        else:
            s = "Low Likelihood Of Rain"

    elif rain_s > 140:
        if humidity > 85:
            s = "Moderate Likelihood Of Rain"
        elif humidity > 70:
            s = "Moderate Likelihood Of Rain"
        elif humidity > 55:
            s = "Low Likelihood Of Rain"
        else:
            s = "Low Likelihood Of Rain"

    elif rain_s > 100:
        if humidity > 85:
            s = "Moderate Likelihood Of Rain"
        elif humidity > 70:
            s = "Low Likelihood Of Rain"
        elif humidity > 55:
            s = "Low Likelihood Of Rain"
        else:
            s = "Very Low Likelihood Of Rain"

    else:
        if humidity > 85:
            s = "Low Likelihood Of Rain"
        elif humidity > 70:
            s = "Low Likelihood Of Rain"
        elif humidity > 55:
            s = "Very Low Likelihood Of Rain"
        else:
            s = "Very Low Likelihood Of Rain" 

    return s 


def average_fuzzy_logic(rain_s, humidity, s):
    if rain_s > 200:
        if humidity > 85:
            s = "High Likelihood Of Rain"
        elif humidity > 70:
            s = "Moderate Likelihood Of Rain"
        elif humidity > 55:
            s = "Moderate Likelihood Of Rain"
        else:
            s = "Low Likelihood Of Rain"

    elif rain_s > 170:
        if humidity > 85:
            s = "Moderate Likelihood Of Rain"
        elif humidity > 70:
            s = "Moderate Likelihood Of Rain"
        elif humidity > 55:
            s = "Low Likelihood Of Rain"
        else:
            s = "Low Likelihood Of Rain"
    elif rain_s > 140:
        if humidity > 85:
            s = "Moderate Likelihood Of Rain"
        elif humidity > 70:
            s = "Low Likelihood Of Rain"
        elif humidity > 55:
            s = "Low Likelihood Of Rain"
        else:
            s = "Very Low Likelihood Of Rain"

    elif rain_s > 100:
        if humidity > 85:
            s = "Low Likelihood Of Rain"
        elif humidity > 70:
            s = "Low Likelihood Of Rain"
        elif humidity > 55:
            s = "Very Low Likelihood Of Rain"
        else:
            s = "Very Low Likelihood Of Rain"

    else:
        if humidity > 85:
            s = "Low Likelihood Of Rain"
        elif humidity > 70:
            s = "Very Low Likelihood Of Rain"
        elif humidity > 55:
            s = "Very Low Likelihood Of Rain"
        else:
            s = "Extremely Low Likelihood Of Rain"    
    return s

def lower_fuzzy_logic(rain_s, humidity, s):
    if rain_s > 200:
        if humidity > 85:
            s = "Moderate Likelihood Of Rain"
        elif humidity > 70:
            s = "Moderate Likelihood Of Rain"
        elif humidity > 55:
            s = "Low Likelihood Of Rain"
        else:
            s = "Low Likelihood Of Rain"
    elif rain_s > 170:
        if humidity > 85:
            s = "Moderate Likelihood Of Rain"
        elif humidity > 70:
            s = "Low Likelihood Of Rain"
        elif humidity > 55:
            s = "Low Likelihood Of Rain"
        else:
            s = "Very Low Likelihood Of Rain"

    elif rain_s > 140:
        if humidity > 85:
            s = "Low Likelihood Of Rain"
        elif humidity > 70:
            s = "Low Likelihood Of Rain"
        elif humidity > 55:
            s = "Very Low Likelihood Of Rain"
        else:
            s = "Very Low Likelihood Of Rain"

    elif rain_s > 100:
        if humidity > 85:
            s = "Low Likelihood Of Rain"
        elif humidity > 70:
            s = "Very Low Likelihood Of Rain"
        elif humidity > 55:
            s = "Very Low Likelihood Of Rain"
        else:
            s = "Extremely Low Likelihood Of Rain"

    else:
        if humidity > 85:
            s = "Very Low Likelihood Of Rain"
        elif humidity > 70:
            s = "Very Low Likelihood Of Rain"
        elif humidity > 55:
            s = "Extremely Low Likelihood Of Rain"
        else:
            s = "Extremely Low Likelihood Of Rain"
    return s

def prediction(i_rain, i_hum, i_temp, c_time, current_df):
    p_rain = current_df[0].mean()
    p_hum = current_df[1].mean()
    p_temp = current_df[2].mean()
    d_time = datetime.fromtimestamp(c_time)
    i_time = int(round(d_time.hour + (d_time.minute/60)))
    predict_df = pd.read_csv('9_final_1.csv')
    # print(predict_df)
    # 218.375 56.900001525878906 18.15000057220459 
    t_df = predict_df.loc[predict_df['hour'] == i_time] 
    rain_s = calculate_temp(t_df, i_rain, i_hum, i_temp, i_time, "t_Delta", 0)
    humidity = calculate_temp(t_df, i_rain, i_hum, i_temp, i_time, "h_Delta", 1)
    temperature = calculate_temp(t_df, i_rain, i_hum, i_temp, i_time, "r_Delta", 2)
    rain_grow = 0
    hum_grow = 0
    s = ""
    #fuzzy logic section
    if p_rain < i_rain < rain_s:
        rain_grow = 2
    if p_rain > i_rain > rain_s:
        rain_grow = 1
    if p_hum < i_hum < humidity:
        hum_grow = 2
    if p_hum < i_hum < humidity:
        hum_grow = 1
    
    #here, rain growth 0 - humidity growth 0, rain growth 1 - humidity growth 2, rain growth 2 - humidity growth 1 have same odds of rain
    
    #rain growth 0 - humidity growth 1, rain growth 1 - humidity growth 0 have same growth rate

    #rain growth 0 - humidity growth 2, rain growth 2 - humidity growth 0 have same growth rate

    #rain growth 1 - humidity growth 1 is different, so is rain growth 2 - humidity growth 2
    print(hum_grow, rain_grow, humidity, rain_s)
    if rain_grow == 0:
        #Rain growth is 0
        #Humidity growth is 0
        if hum_grow == 0:
            s = average_fuzzy_logic(rain_s, humidity, s)
                        
        #Rain growth is 0
        #Humidity growth is 1
        elif hum_grow == 1:
            s = lower_fuzzy_logic(rain_s, humidity, s)
        
        #Rain growth is 0
        #Humidity growth is 2
        elif hum_grow == 2:
            s = higher_fuzzy_logic(rain_s, humidity, s)
            
    
    elif rain_grow == 1:
        #Rain growth is 1
        #Humidity growth is 0
        if hum_grow == 0:
            s = lower_fuzzy_logic(rain_s, humidity, s)
        #Rain growth is 1
        #Humidity growth is 1
        elif hum_grow == 1:
            if rain_s > 200:
                if humidity > 85:
                    s = "Moderate Likelihood Of Rain"
                elif humidity > 70:
                    s = "Low Likelihood Of Rain"
                elif humidity > 55:
                    s = "Low Likelihood Of Rain"
                else:
                    s = "Very Low Likelihood Of Rain"
            elif rain_s > 170:
                if humidity > 85:
                    s = "Low Likelihood Of Rain"
                elif humidity > 70:
                    s = "Low Likelihood Of Rain"
                elif humidity > 55:
                    s = "Very Low Likelihood Of Rain"
                else:
                    s = "Very Low Likelihood Of Rain"

            elif rain_s > 140:
                if humidity > 85:
                    s = "Low Likelihood Of Rain"
                elif humidity > 70:
                    s = "Very Low Likelihood Of Rain"
                elif humidity > 55:
                    s = "Very Low Likelihood Of Rain"
                else:
                    s = "Extremely Low Likelihood Of Rain"

            elif rain_s > 100:
                if humidity > 85:
                    s = "Very Low Likelihood Of Rain"
                elif humidity > 70:
                    s = "Very Low Likelihood Of Rain"
                elif humidity > 55:
                    s = "Extremely Low Likelihood Of Rain"
                else:
                    s = "Extremely Low Likelihood Of Rain"

            else:
                if humidity > 85:
                    s = "Very Low Likelihood Of Rain"
                elif humidity > 70:
                    s = "Extremely Low Likelihood Of Rain"
                elif humidity > 55:
                    s = "Extremely Low Likelihood Of Rain"
                else:
                    s = "Extremely Low Likelihood Of Rain"

        #Rain growth is 1
        #Humidity growth is 2
        elif hum_grow == 2:
            s = average_fuzzy_logic(rain_s, humidity, s)
    
    elif rain_grow == 2:
        #Rain growth is 2
        #Humidity growth is 0
        if hum_grow == 0:
            s = higher_fuzzy_logic(rain_s, humidity, s) 
        #Rain growth is 2
        #Humidity growth is 1
        elif hum_grow == 1:
            s = average_fuzzy_logic(rain_s, humidity, s)
        #Rain growth is 2
        #Humidity growth is 2
        elif hum_grow == 2:
            if rain_s > 200:
                if humidity > 85:
                    s = "Very High Likelihood Of Rain"
                elif humidity > 70:
                    s = "Very High Likelihood Of Rain"
                elif humidity > 55:
                    s = "High Likelihood Of Rain"
                else:
                    s = "High Likelihood Of Rain"

            elif rain_s > 170:
                if humidity > 85:
                    s = "Very High Likelihood Of Rain"
                elif humidity > 70:
                    s = "High Likelihood Of Rain"
                elif humidity > 55:
                    s = "High Likelihood Of Rain"
                else:
                    s = "Moderate Likelihood Of Rain"

            elif rain_s > 140:
                if humidity > 85:
                    s = "High Likelihood Of Rain"
                elif humidity > 70:
                    s = "Moderate Likelihood Of Rain"
                elif humidity > 55:
                    s = "Moderate Likelihood Of Rain"
                else:
                    s = "Low Likelihood Of Rain"

            elif rain_s > 100:
                if humidity > 85:
                    s = "Moderate Likelihood Of Rain"
                elif humidity > 70:
                    s = "Moderate Likelihood Of Rain"
                elif humidity > 55:
                    s = "Low Likelihood Of Rain"
                else:
                    s = "Low Likelihood Of Rain"
            else:
                if humidity > 85:
                    s = "Moderate Likelihood Of Rain"
                elif humidity > 70:
                    s = "Low Likelihood Of Rain"
                elif humidity > 55:
                    s = "Low Likelihood Of Rain"
                else:
                    s = "Very Low Likelihood Of Rain"  
    

    print(temperature, humidity, rain_s)
    body = f"""The past values are humidity: {round(p_hum, 2)}, rain: {round(p_rain, 2)}, temperature: {round(p_temp, 2)}
The current values are humidity: {round(i_hum, 2)}, rain: {round(i_rain, 2)}, temperature: {round(i_temp, 2)}
The predicted values are humidity: {round(humidity,2)}, rain: {round(rain_s,2)}, temperature: {round(temperature,2)}
There Is A {s}
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
    
    print(s)


def main():
    print("main() function")

    # Instantiate Arduino cloud client
    client = ArduinoCloudClient(
        device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY
    )

    # Register with 'temperature' cloud variable
    # and listen on its value changes in 'on_temperature_changed'
    # callback function.
    client.register(
        "rain", value=None, on_write=on_c_changed)
    client.register(
        "temperature", value=None, on_write=on_c_changed)
    client.register(
        "humidity", value=None,  on_write=on_c_changed)

    # start cloud client
    client.start()

if __name__ == "__main__":
    try:
        setNum(0)
        main()  # main function which runs in an internal infinite loop
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_type, file=print)