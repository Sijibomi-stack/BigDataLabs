
from pyspark import SparkContext
from pyspark.sql import SQLContext, Row
from pyspark.sql import functions as F
sc =SparkContext()
sqlContext=SQLContext(sc)

temperature_file = sc.textFile("BDA/input/temperature-readings.csv")
parts = temperature_file.map(lambda l:l.split(";"))

tempReadings = parts.map(lambda p: Row(station=p[0],  date=p[1], year=p[1].split("-")[0],
time=p[2],  Temp=float(p[3]), quality=p[4]))

TableReadings = sqlContext.createDataFrame(tempReadings)
TableReadings.registerTempTable("tempReadings")

maximum_temperature = TableReadings.select(["year","station","Temp"]).filter((TableReadings['year'] <=2014)
& (TableReadings["year"]>=1950)).groupby(['year','station']).agg(F.max('Temp')).groupby("year").agg(F.max("max(Temp)").alias("Temp")).orderBy('Temp',ascending=False)

maximum_temperature1 = maximum_temperature.join(TableReadings,["Temp","year"],"inner")

maximum_temperature2 = maximum_temperature1.select(["year","station","Temp"]).orderBy("Temp",ascending= False).withColumnRenamed("Temp","MaxValue")

minimum_temperature = TableReadings.select(["year","station","Temp"]).filter((TableReadings['year'] <=2014)
& (TableReadings["year"]>=1950)).groupby(['year','station']).agg(F.min('Temp')).groupby("year").agg(F.min("min(Temp)").alias("Temp")).orderBy('Temp',ascending=True)

minimum_temperature1 = minimum_temperature.join(TableReadings,["Temp","year"],"inner")

minimum_temperature2 = minimum_temperature1.select(["year","station","Temp"]).orderBy("Temp",ascending= True).withColumnRenamed("Temp","MinValue")

maximum_temperature2_rdd = maximum_temperature2.rdd
minimum_temperature2_rdd = minimum_temperature2.rdd

maximum_temperature2_rdd.saveAsTextFile("BDA/output/Max_temp")
minimum_temperature2_rdd.saveAsTextFile("BDA/output/Min_Temp")
