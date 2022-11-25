from pyspark import SparkContext
sc = SparkContext(appName = "exercise 1")
#This path is to the file on hdfs
temperature_file = sc.textFile("BDA/input/temperature-readings.csv")
lines = temperature_file.map(lambda line: line.split(";"))

#Maps
#(key, value) = (year,temperature)
average = lines.map(lambda x: ((x[1][0:4],x[1][5:7],x[0]),float(x[3])))

#filters
average = average.filter(lambda x: int(x[0][0]) >= 1960 and int(x[0][0]) <= 2014)


#Transformations
average = average.map(lambda x: ((x[0][0],x[0][1],x[0][2]),float(x[1])))
averagerdd = (average.mapValues(lambda x: (x,1)).reduceByKey(lambda x,y:(x[0]+y[0],x[1]+y[1]))
.mapValues(lambda x: x[0]/x[1])).sortByKey(ascending = False)

#Actions
#Following code will save the result into /user/ACCOUNT_NAME/BDA/output folder
averagerdd.saveAsTextFile("BDA/output/AverageMonthlyTemp")
