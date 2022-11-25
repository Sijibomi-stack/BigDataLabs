

from pyspark import SparkContext
sc = SparkContext(appName = "exercise 1")
# This path is to the file on hdfs

temp_data = sc.textFile("BDA/input/temperature-readings.csv")
precip_data = sc.textFile("BDA/input/precipitation-readings.csv")

#(key, value) = (year,temperature)
lines_temp = temp_data.map(lambda lines: lines.split(";"))
lines_precip = precip_data.map(lambda lines: lines.split(";"))

#filter
temp = lines_temp.map(lambda x: (int(x[0]), float(x[3])))
temp_max_stations = temp.reduceByKey(lambda a,b: a if a >= b else b)
temp_max_station = temp_max_stations.filter(lambda x: x[1] >= 25 and x[1] <= 30)

precip = lines_precip.map(lambda x: ((int(x[0]), x[1][0:4], x[1][5:7], x[1][8:10]), float(x[3])))
daily_precip = precip.reduceByKey(lambda a,b: a + b)
daily_precip = daily_precip.map(lambda x: (x[0][0], x[1]))
precip_max_station = daily_precip.reduceByKey(lambda a,b: a if a >= b else b)
precip_max_station_ = precip_max_station.filter(lambda x: x[1] >= 100 and x[1] <= 200)

join = data_temp_max_station.join(data_precip_max_station)

# Following code will save the result into /user/ACCOUNT_NAME/BDA/output folder
result.saveAsTextFile("BDA/output/Temp3040_Precip100200")
#data_precip_max_station_restrictions.saveAsTextFile("BDA/output/A1")
#data_temp_max_station_restrictions.saveAsTextFile("BDA/output/A2")
