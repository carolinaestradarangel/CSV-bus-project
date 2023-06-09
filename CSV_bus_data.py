#Carolina Estrada
import pandas 
import sqlite3
import numpy as np 
import matplotlib.pyplot as plt

def convert(filename,dbname):

  bus_data = pandas.read_csv("bus_data.csv")
  conn= sqlite3.connect(dbname)
  curr = conn.cursor()
  curr.execute("DROP table IF EXISTS bus_data")
  sql = '''CREATE TABLE bus_data(route text, date text, daytype text, rides int) '''
  curr.execute(sql)
  
  for i in range(len(bus_data)):
    route = bus_data['route'][i]
    route = "'"+route+"'"
    date = bus_data['date'][i]
    date = "'"+date+"'"
    daytype = bus_data['daytype'][i]
    daytype = "'"+daytype+"'"
    rides = bus_data['rides'][i]

    curr.execute("INSERT INTO bus_data VALUES( %s, %s,%s, %i)" % (route,date,daytype,rides))

  conn.commit()
  conn.close()

convert("bus_data.csv", "bus_data.db")
# this converts the csv file into the db file 

# had this function to check specific data to print out once ran program. 
# def select_data(sql):
#     conn=sqlite3.connect('bus_data.db')
#     cur=conn.cursor()
#     result= cur.execute(sql)
#     for i in result:
#         print(i)
#     conn.commit()
#     conn.close()

def route_data(r):
  conn = sqlite3.connect("bus_data.db")
  cur = conn.cursor()
  # the r would replace any route that the user inputs as a string and loop through it.
  output = cur.execute("SELECT AVG(rides) FROM bus_data WHERE route == ?",(r,))
  for i in output:
    print(i)
  # conn.commit()
  # conn.close()

# route_data('22')
  high_rides = cur.execute("SELECT COUNT(*) FROM bus_data WHERE rides > 1200").fetchall()
  total_rides = cur.execute("SELECT COUNT(*) FROM bus_data").fetchall()
  # print(high_rides)
  # print(total_rides)
  
  print((high_rides[0][0]/total_rides[0][0])*100,'%')
  conn.commit()
  conn.close()
  
# route_data('22')
def yr_sum(*years):
  """"This function takes input from the user and doesn't modify the file itself but looks through the file for specific years and takes the sum of rides for those specific years. It could look through one years of all of the years, it should hold for any case. 
  """
  r = [*years]
  # took it as a list to then loop through 
  conn = sqlite3.connect("bus_data.db")
  cur = conn.cursor()
  l = []
  for i in r:
    output = cur.execute("SELECT SUM(rides) FROM bus_data WHERE date LIKE '%/%/{}'".format(i))
    # the i would be replaced by the list of the years the user inputted to look at. 
    l.append(output.fetchall())
  sum = 0
  for n in l:
    sum += n[0][0]
    # turned the tuples to just integers. 
  print(sum)
  conn.commit()
  conn.close()

# yr_sum(2013,2014)

def my_func():
  
  timeline = ['2001','2002','2004','2006','2008','2010','2012','2014','2016','2018','2020','2022']
  # created a list of even numbers of years in database
  conn = sqlite3.connect("bus_data.db")
  cur = conn.cursor()
  list_of_avg_ride = []      
  for i in timeline:
    result = cur.execute("SELECT CEILING(AVG(rides)) FROM bus_data WHERE date LIKE '07/%/{}'".format(i))
    list_of_avg_ride.append(result.fetchall())
  # print(l)
  avg_ride = []
  for avg_ride_time in list_of_avg_ride:
    avg_ride.append(avg_ride_time[0][0])
  # print(avg_ride) 
  plt.scatter(timeline,avg_ride)
  plt.title("Average ridership vs. Yearly comparison based on July")
  plt.xlabel("Even Years starting from 2001")
  plt.ylabel("Average ridership")
  plt.savefig('average year comparison.png')
  conn.commit()
  conn.close()
my_func()
def update():
  convert("bus_data.csv", "bus_data_backup.db")
  conn = sqlite3.connect("bus_data.db")
  cur = conn.cursor()
  update_rides = "UPDATE bus_data SET rides == floor(rides - (rides*.10)) WHERE daytype == 'A'"
  cur.execute(update_rides)
  conn.commit()
  conn.close()

  # select_data("UPDATE bus_data SET rides == floor(rides - (rides*.10)) WHERE daytype == 'A'")
  # this function demonstrated the actual change of the db files. 
  
  # conn.commit()
  # conn.close()
# update()

# function below is to check if the data was actually changed in the db after the update. 
  
# def showallbusdata():
#     select_data("SELECT * FROM bus_data")

# showallbusdata()
#comment and uncomment this to check everything works and data runs. 
