
from pyspark import SparkContext
from pyspark.sql import SQLContext, Row
from pyspark.sql import functions as F
sc =SparkContext(appName = "exercise 1")
sqlContext=SQLContext(sc)

temperature_file = sc.textFile("BDA/input/temperature-readings.csv")
parts = temperature_file.map(lambda l:l.split(";"))

tempReadings = parts.map(lambda p: Row(station=p[0],date=p[1],year=p[1].split("-")[0],month=p[1].split("-")[1],time=p[2],  Temp=float(p[3]),quality=p[4]))

TableReadings = sqlContext.createDataFrame(tempReadings)
TableReadings.registerTempTable("tempReadings")

TempAbove10 = TableReadings.select(["year","month","station"]).filter((TableReadings['year'] <=2014) & (TableReadings["year"]>=1950)
& (TableReadings["Temp"] > 10)).groupby(["year","month"]).agg(F.count("station").alias("station_count")).orderBy("station_count",ascending=False)

TempAbove10.show()

TempAbove10.rdd.saveAsTextFile("BDA/output/temp_G10")
