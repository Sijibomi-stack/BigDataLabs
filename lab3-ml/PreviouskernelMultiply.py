
from __future__ import division
from math import radians, cos, sin, asin, sqrt, exp
from datetime import datetime
from operator import truediv
from pyspark import SparkContext

sc = SparkContext(appName="lab_kernel")

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

h_distance = 150 # Up to you
h_date = 30 # Up to you
h_time = 3 # Up to you
a = 57.7236 # Up to you
b = 12.9641 # Up to you

times=["04:00:00", "06:00:00","08:00:00" ,"10:00:00","12:00:00","14:00:00",
       "16:00:00","18:00:00","20:00:00","22:00:00","00:00:00"]

date = "2013-11-02"# Up to you

def kernel(diff, kernel_width):
    weight = exp(-(diff/kernel_width)**2)
    return weight

def as_date(date):
    date_format = "%Y-%m-%d"
    a = datetime.strptime(date, date_format)
    return a

def diff_date(date1,date2,h_date):
    date_format = "%Y-%m-%d"
    a = datetime.strptime(date1, date_format)
    b = datetime.strptime(date2, date_format)
    delta = b - a
    dd = delta.days % 365
    if dd > (365/2):
        c = 365 - dd
    else:
         c = dd
    return kernel(c, h_date)

def diff_time(time1,time2,h_time):
    date_format = "%H:%M:%S"
    a = datetime.strptime(time1, date_format)
    b = datetime.strptime(time2, date_format)
    delta = b - a
    dt = delta.seconds/3600
    if dt > 12:
        c = 24 - (dt/3600)
    else:
        c = dt/3600
    return kernel(c, h_time)

temperature_file = sc.textFile("BDA/input/temperature-readings.csv")
stations_file = sc.textFile("BDA/input/stations.csv")

temps = temperature_file.map(lambda line: line.split(";"))
station = stations_file.map(lambda line: line.split(";"))

lines = temps.filter(lambda x: as_date(x[1]) < as_date(date)).cache()

year_temps = lines.map(lambda x: ((int(x[0]),x[1],x[2],(float(x[3])))))

year_temps = year_temps.map(lambda x: (x[0],
(diff_date(x[1], date, h_date),diff_time(x[2], "04:00:00", h_time),diff_time(x[2], "06:00:00", h_time),
diff_time(x[2], "08:00:00", h_time),diff_time(x[2], "10:00:00", h_time),diff_time(x[2], "12:00:00", h_time),
diff_time(x[2], "14:00:00", h_time),diff_time(x[2], "16:00:00", h_time),diff_time(x[2], "18:00:00", h_time),
diff_time(x[2], "20:00:00", h_time),diff_time(x[2], "22:00:00", h_time),diff_time(x[2], "00:00:00", h_time),x[3]))).cache()

year_temps_k = year_temps.map(lambda x: (x[0],(kernel(x[1][0],h_date),kernel(x[1][1],h_time),kernel(x[1][2],h_time),kernel(x[1][3],h_time),kernel(x[1][4],h_time),kernel(x[1][5],h_time),kernel(x[1][6],h_time),
                                                     kernel(x[1][7],h_time),kernel(x[1][8],h_time),kernel(x[1][9],h_time),
                                                     kernel(x[1][10],h_time),kernel(x[1][11],h_time),x[1][12]))).cache()

stations = station.map(lambda x: ((int(x[0]),float(x[3]),float(x[4]))))

stations = stations.map(lambda x: (x[0], x[1], x[2], haversine(x[1], x[2], a, b)))

stations= stations.map(lambda x: (x[0], kernel(x[3], h_distance)))

stations = stations.collectAsMap()
bc = sc.broadcast(stations)
joined = year_temps_k.map(lambda x: (x[0], x[1],bc.value.get(x[0])))

def mult_kernels(a,b,c):
    d = a*b*c
    return d

rdd = joined.map(lambda x: (x[0],mult_kernels(x[1][0], x[1][1], x[2]),mult_kernels(x[1][0],x[1][2], x[2]),
                         mult_kernels(x[1][0], x[1][3], x[2]),mult_kernels(x[1][0], x[1][4], x[2]),
                         mult_kernels(x[1][0], x[1][5], x[2]),mult_kernels(x[1][0], x[1][6], x[2]),
                         mult_kernels(x[1][0], x[1][7], x[2]),mult_kernels(x[1][0], x[1][8], x[2]),
                         mult_kernels(x[1][0], x[1][9], x[2]),mult_kernels(x[1][0], x[1][10], x[2]),
                         mult_kernels(x[1][0], x[1][11], x[2]),x[1][12])).cache()

rdd = rdd.map(lambda x:( [x[1]*x[-1],x[2]*x[-1],x[3]*x[-1],x[4]*x[-1],x[5]*x[-1],
                          x[6]*x[-1],x[7]*x[-1],x[8]*x[-1],x[9]*x[-1],x[10]*x[-1],
                          x[11]*x[-1]],[x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],
                                        x[9],x[10],x[11]]))

rdd = rdd.reduce(lambda x, y: ([x[0][0] + y[0][0],x[0][1] + y[0][1],x[0][2] + y[0][2],x[0][3] + y[0][3],
                                x[0][4] + y[0][4],x[0][5] + y[0][5],x[0][6] + y[0][6],x[0][7] + y[0][7],
                                x[0][8] + y[0][8],x[0][9] + y[0][9],x[0][10] + y[0][10]],[x[1][0]+y[1][0],
                                x[1][1] + y[1][1],x[1][2] + y[1][2],x[1][3] + y[1][3],x[1][4] + y[1][4],
                                x[1][5] + y[1][5],x[1][6] + y[1][6],x[1][7] + y[1][7],x[1][8] + y[1][8],
                                x[1][9] + y[1][9],x[1][10] + y[1][10]]))

rdd = map(truediv, rdd[0], rdd[1])
rdd = list(rdd)
print(times,rdd)
