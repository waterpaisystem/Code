#LIBRARIES
from __future__ import print_function
import json
import time
import datetime
import urllib
import requests
import csv
import mariadb
import sys
import yagmail

replacement = .2

#Email info
g_email = 'xxxxxxxxxxxxx' #Gmail account.
y_email = 'xxxxxxxxxxxxx' #Yahoo account.
password='xxxxxxxxx' #Password for Gmail account - protected for privacy.

#Connect to the mariadb database
try:
    conn = mariadb.connect(
        user="waterpai",
        password="xxxxxxxx",
        host="xxxxxxxxxx",
        port=3306,
        database="WeatherData"

    )
except mariadb.Error as e:
    yag.send(to = y_email, subject = 'Error connecting to MariaDB', contents = "Error connecting to MariaDB")
    sys.exit(1)

cur = conn.cursor()

def waterLawn(): #Irrigates the lawn with replacement inches of water for each zone.
    yag.send(to = y_email, subject = 'Beginning Irrigation', contents = 'Watering now')
    os.system('python WaterLawn.py')
    
#Get the last row of the ETData table.
cur.execute("select * from ETData order by time desc limit 1")

#Get the next_hour that it needs to start recording data for
for (station, time, tmpf, relh,solar, precip, speed, et) in cur:
    last_date = datetime.datetime.strptime(f"{time}", '%Y-%m-%d %H:%M:%S')
    next_hour = last_date + datetime.timedelta(hours = 1)

#Get the last row of the NeededIrrigationData table.
cur.execute("select * from NeededIrrigationData order by time desc limit 1")

#Get the next_hour that it needs to start recording data for
for (time, neededirrig) in cur:
    last_needed_irrig = float(f"{neededirrig}")

#Get the last row of the IrrigationData table.
cur.execute("select * from IrrigationData order by time desc limit 1")

#Get the next_hour that it needs to start recording data for
for (time, irrig) in cur:
    last_irrig = float(f"{irrig}")

    
#Base URL
url = "http://mesonet.agron.iastate.edu/cgi-bin/request/isusm.py?"

#Set start and end times for retrieving the data
startts = datetime.datetime(next_hour.year, next_hour.month, next_hour.day)
tomorrow = datetime.date.today() + datetime.timedelta(days = 1)
endts = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day)

#Add the date paramaters and variables to url. We get all the hourly data since day of next_hour
url += "mode=hourly&timeres=hourly&sts=CIRI4&"
url += startts.strftime("year1=%Y&month1=%m&day1=%d&")
url += endts.strftime("year2=%Y&month2=%m&day2=%d&")
url += "vars=tmpf&vars=relh&vars=solar&vars=precip&vars=speed&vars=et&format=comma&missing=-99"

#Download the data from url
data = urllib.request.urlopen(url, timeout = 3000).read().decode("utf-8")

#Update the ETData and IrrigationData table
last_irrig_date = ''
line_counter = 0
for line in data.splitlines():
    if(line_counter != 0):
        l = line.split(",")
        last_irrig_date = l[1]+":00"
        if(l[2] == str(-99) or l[3] == str(-99) or l[4] == str(-99) or l[5] == str(-99) or l[6] == str(-99) or l[7] == str(-99)):
            break
        if(datetime.datetime.strptime(l[1], '%Y-%m-%d %H:%M') > last_date):
            try:
                cur.execute("INSERT INTO ETData (station, time, tmpf, relh,solar, precip, speed, et) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                (l[0], l[1]+":00", l[2], l[3], l[4], l[5], l[6], l[7]))

                last_needed_irrig += .8*float(l[7])-float(l[5])
                last_irrig += .8*float(l[7])-float(l[5])
                
                cur.execute("INSERT INTO NeededIrrigationData (time, neededirrig) VALUES (?, ?)", (l[1]+":00", last_needed_irrig))

                #Uncomment when doing historical data
                '''
                current_hour = datetime.datetime.strptime(str(l[1]+":00"), '%Y-%m-%d %H:%M:%S').hour
                can_water = False #Irrigation can be run only if can_water==true.
                if(float(l[5])<.01 and float(l[6])<8 and current_hour>=2 and current_hour<=16): #Irrigate only if the current wind speed is <8 mph, and the time is between 2:00 am and 4:00 pm.
                    can_water = True
                    
                if(can_water and last_irrig > replacement):
                   last_irrig -= replacement
                cur.execute("INSERT INTO IrrigationData (time, irrig) VALUES (?, ?)", (l[1]+":00", last_irrig))
                '''

                
            except mariadb.Error as err: #Error as type mariadb.IntegrityError
                if("Duplicate entry" in str(err)): 
                    cur.execute("DELETE FROM ETData where station=? and time=?", (l[0],l[1])) #Remove duplicate entries from the table
                    cur.execute("INSERT INTO ETData (station, time, tmpf, relh,solar, precip, speed, et) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                    (l[0], l[1]+":00", l[2], l[3], l[4], l[5], l[6], l[7]))
                    
                    last_needed_irrig += .8*float(l[7])-float(l[5])
                    last_irrig += .8*float(l[7])-float(l[5])
                    
                    cur.execute("INSERT INTO NeededIrrigationData (time, neededirrig) VALUES (?, ?)", (l[1]+":00", last_needed_irrig))

                    #Uncomment when doing historical data
                    '''
                    current_hour = datetime.datetime.strptime(str(l[1]+":00"), '%Y-%m-%d %H:%M:%S').hour
                    can_water = False #Irrigation can be run only if can_water==true.
                    if(float(l[5])<.01 and float(l[6])<8 and current_hour>=2 and current_hour<=16): #Irrigate only if the current wind speed is <8 mph, and the time is between 2:00 am and 4:00 pm.
                        can_water = True
                    if(can_water and last_irrig > replacement):
                        last_irrig -= replacement
                    cur.execute("INSERT INTO IrrigationData (time, irrig) VALUES (?, ?)", (l[1]+":00", last_irrig))
                    '''

                else:
                    yag.send(to = y_email, subject = 'Error in data updation', contents = str(err))
    line_counter = line_counter + 1

wind = requests.get('https://api.weatherbit.io/v2.0/forecast/hourly?lat=41.709837&lon=-91.556808&key=xxxxxxx').json() #Used Weatherbit Forecast API for and current wind speed.
precip = requests.get('https://api.weatherbit.io/v2.0/forecast/daily?lat=41.709837&lon=-91.556808&key=xxxxxx').json()#Used WeatherBit Forecast API for 3 day precipitation forecast.
future_precip = 0
for i in range (0,3):
    future_precip += 0.0393701 * precip['data'][i]['precip'] #1 mm = .0393701 in.
current_wind = 2.23694 * wind['data'][0]['wind_spd']  #1 m/s = 2.23694 mph.
future_irrig = last_irrig - future_precip
current_hour = datetime.datetime.strptime(str(l[1]+":00"), '%Y-%m-%d %H:%M:%S').hour
if(future_irrig>replacement and current_wind<8 and current_hour > 1 and current_hour < 17): #Irrigate only if the forecast needed irrigation is > replacement, the current wind speed is <8 mph, and the time is between 10:00 am and 4:00 pm.
    last_irrig -= replacement
    cur.execute("DELETE FROM IrrigationData WHERE time='"+str(last_irrig_date)+"'")
    cur.execute("INSERT INTO IrrigationData (time, irrig) VALUES (?, ?)", (last_irrig_date, last_irrig))
    waterLawn()

conn.commit()
conn.close()






