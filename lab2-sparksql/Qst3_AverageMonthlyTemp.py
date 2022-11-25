from pyspark import SparkContext
sc = SparkContext(appName = "exercise 1")
#This path is to the file on hdfs
temperature_file = sc.textFile("BDA/input/temperature-readings.csv")
lines = temperature_file.map(lambda line: line.split(";"))

#(key, value) = (year,temperature)
rdd = lines.map(lambda x: ((x[1][0:11],x[0]),float(x[3])))

#filters
average = rdd.filter(lambda x: int(x[0][0][0:4]) >= 1960 and int(x[0][0][0:4]) <= 2014)

max_temperatures = average.reduceByKey(lambda x,y :x if x>=y else y)
min_temperatures = average.reduceByKey(lambda x,y :x if x<=y else y)

temperature_average = max_temperatures.join(min_temperatures)

rdd = temperature_average.map(lambda x: (x[0], x[1][0] + x[1][1]))

daily_temp_rdd = rdd.map(lambda x: (x[0],x[1]/2))

monthly_temp_rdd = daily_temp_rdd.map(lambda x: ((x[0][0][0:7],x[0][1]),x[1])).mapValues(lambda x: (x, 1)).reduceByKey(lambda x, y: (x[0]+y[0], x[1]+y[1])).mapValues(lambda x: x[0]/x[1]).sortByKey(ascending=False)

monthly_temp_rdd.saveAsTextFile("BDA/output/Temp")
