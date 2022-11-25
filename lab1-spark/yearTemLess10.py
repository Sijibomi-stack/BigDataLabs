from pyspark import SparkContext
sc = SparkContext(appName = "exercise 1")
# This path is to the file on hdfs
temperature_file = sc.textFile("BDA/input/temperature-readings.csv")
lines = temperature_file.map(lambda line: line.split(";"))

# (key, value) = (year,temperature)
year_temLess10 = lines.map(lambda x: ((x[1][0:4], x[1][5:7]),float(x[3])))

#filters
year_temLess10 = year_temLess10.filter(lambda x: int(x[0][0]) >= 1950 and int(x[0][0]) <= 2014)
tempsAbove10 = year_temLess10.filter(lambda x: x[1] >= 10)

#Transformations
tempsAbove10counts = tempsAbove10.map(lambda x:((x[0][0], x[0][1]),1))
tempsAbove10 = tempsAbove10counts.reduceByKey(lambda x,y : x+y).sortByKey()

#Actions
# Following code will save the result into /user/ACCOUNT_NAME/BDA/output folder
tempsAbove10.saveAsTextFile("BDA/output/tempsAbove10")
