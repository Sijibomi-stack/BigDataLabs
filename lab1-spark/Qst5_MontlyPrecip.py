

from pyspark import SparkContext
sc = SparkContext(appName = "exercise 1")
# This path is to the file on hdfs

station_data = sc.textFile("BDA/input/stations-Ostergotland.csv")
precip_data = sc.textFile("BDA/input/precipitation-readings.csv")

stations = station_data.map(lambda line: line.split(";")[0]).collect()

precip = precip_data.map(lambda line: line.split(";"))

precip_years = precip.filter(lambda x: int(x[1][0:4])>=1993 and int(x[1][0:4])<=2016)
counts = precip_years.filter(lambda x: x[0] in stations)

counts = counts.map(lambda x: ((x[1][0:7], x[0]), float(x[3])))

preci_station = counts.reduceByKey(lambda a,b: a+b)

avg_preci = preci_station.map(lambda x: (x[0][0],  (x[1], 1)))

preci_monthly = avg_preci.reduceByKey(lambda a,b: (a[0]+b[0],a[1]+b[1]))
preci_monthly = preci_monthly.map(lambda x: (x[0][0:4], x[0][5:7], x[1][0]/x[1][1]))

preci_monthly.saveAsTextFile("BDA/output/Answer_Qst5")
