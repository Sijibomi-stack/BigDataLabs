
from __future__ import division
from math import radians, cos, sin, asin, sqrt, exp
from datetime import datetime
from pyspark import SparkContext

sc = SparkContext(appName="ML Lab3")

def haversine(lon1, lat1, lon2, lat2):
    """Calculate the great circle distance between two points on the earth (specified in decimal degrees)"""
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 -lon1
    dlat = lat2 -lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km

# init values
h_distance = 150 # Up to you
h_date  = 30 #  Up  to  you
h_time = 3 # Up to you

lon2 = 58.4274 # Up to you
lat2 = 14.826 # Up to you

times=["04:00:00", "06:00:00","08:00:00" ,"10:00:00","12:00:00","14:00:00",
       "16:00:00","18:00:00","20:00:00","22:00:00","00:00:00"]

date = "2013-11-04"

temperature_file = sc.textFile("BDA/input/temperature-readings.csv")
stations_file = sc.textFile("BDA/input/stations.csv")

temps = temperature_file.map(lambda line: line.split(";"))
station = stations_file.map(lambda line: line.split(";"))

def as_date(date):
    date_format = "%Y-%m-%d"
    a = datetime.strptime(date, date_format)
    return a

def gaussian_kernel(diff, h):
    return exp(-(diff / h) ** 2)

dist_days = temps.map(lambda x:(x[0],(x[1],x[2],float(x[3])))).filter(lambda x: as_date(x[1][0]) < as_date(date)).cache()

stations = station.map(lambda x: ((x[0],(float(x[3]),float(x[4])))))

stations = stations.collectAsMap()
bc = sc.broadcast(stations)
joined = dist_days.map(lambda x: (x[0], x[1],bc.value.get(x[0])))
kernel = joined.map(lambda x: (x[0],haversine(lon2,lat2,float(x[2][0]),float(x[2][1])),(datetime.strptime(date,"%Y-%m-%d") - datetime.strptime(x[1][0],"%Y-%m-%d")).days,x[1][2])).cache()
res = kernel.map(lambda x: (x[1],x[2],x[3]))
result = res.map(lambda x: str(x).replace('(', '').replace(')', ''))
result.sample(False, 0.001).saveAsTextFile("BDA/output/kernel_values")
