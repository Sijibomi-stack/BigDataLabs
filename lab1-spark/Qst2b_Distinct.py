from pyspark import SparkContext
sc = SparkContext(appName = "exercise 1")
#This path is to the file on hdfs
temperature_file = sc.textFile("BDA/input/temperature-readings.csv")
lines = temperature_file.map(lambda line: line.split(";"))

#Maps
#(key, value) = (year,temperature)
year_temLess10Distinct = lines.map(lambda x: (x[1][0:7], (x[0], float(x[3]))))

#filters
year_temLess10Distinct = year_temLess10Distinct.filter(lambda x: int(x[0][0:4])>=1950 and int(x[0][0:4])<=2014)
year_temLess10Distinct = year_temLess10Distinct.filter(lambda x: float(x[1][1]) >= 10)

#Transformations
month = year_temLess10Distinct.map(lambda x: (x[0],x[1][0])).distinct()
month_unique = month.map(lambda x: x[0])
month_count = month_unique.map(lambda s : (s, 1))
count = month_count.reduceByKey(lambda a,b : a + b)                       


#Actions
#Following code will save the result into /user/ACCOUNT_NAME/BDA/output folder
count.saveAsTextFile("BDA/output/DistictTempAbove10")
