from pyspark import SparkContext
sc = SparkContext(appName = "exercise 1")
# This path is to the file on hdfs
temperature_file = sc.textFile("BDA/input/temperature-readings.csv")
lines = temperature_file.map(lambda line: line.split(";"))

#Maps
# (key, value) = (year,temperature)
year_temperature = lines.map(lambda x: (x[1][0:4],(float(x[3]),x[0])))

#filters
year_temperature = year_temperature.filter(lambda x: int(x[0]) >= 1950 and int(x[0])<= 2014)

#Transformations
max_temperatures = year_temperature.reduceByKey(lambda x,y :x if x>=y else y)
max_temperatures1 = max_temperatures.sortBy(ascending = False, keyfunc=lambda k: k[1][0])
max_temperatures2 = max_temperatures1.map(lambda x: (x[0], float(x[1][0]),x[1][1]))

#Actions
# Following code will save the result into /user/ACCOUNT_NAME/BDA/output folder
max_temperatures2.saveAsTextFile("BDA/output/max_temperature")
