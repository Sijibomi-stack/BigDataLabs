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
h_distance = 100 # Up to you
h_date  = 50 #  Up  to  you
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
kernel = joined.map(lambda x: (x[0],haversine(lon2,lat2,float(x[2][0]),float(x[2][1])),(datetime.strptime(date,"%Y-%m-%d") - datetime.strptime(x[1][0],"%Y-%m-%d")).days,x[1][1],x[1][2]))
kernel_gaussian = kernel.map(lambda x: (gaussian_kernel(x[1],h_distance), gaussian_kernel(x[2], h_date),x[3],x[4])).cache()
for time in times:
    results = dict()
    kernel_rdd =  kernel_gaussian.map(lambda x: (x[0],x[1],(datetime.strptime(time,'%H:%M:%S') - datetime.strptime(x[2],'%H:%M:%S')).seconds/3600,float(x[3]))).cache()
    gaussian_time = kernel_rdd.map(lambda x: (x[3],x[0],x[1],gaussian_kernel(x[2],h_time))).cache()
    kernel_sum = gaussian_time.map(lambda x: (x[0], x[1] + x[2] + x[3]))
    kernel_agg = kernel_sum.map(lambda x: (float(x[0])*x[1],x[1]))
    reduced=kernel_agg.reduce(lambda x,y: (x[0]+y[0],x[1]+y[1]))
    results=reduced[0]/reduced[1]
    print(time,results)
