
from pyspark import SparkContext
from pyspark.sql import SQLContext, Row
from pyspark.sql import functions as F
sc =SparkContext(appName = "exercise 1")
sqlContext=SQLContext(sc)

temperature_file = sc.textFile("BDA/input/temperature-readings.csv")
parts = temperature_file.map(lambda l:l.split(";"))

tempReadings = parts.map(lambda p: Row(station=p[0],date=p[1],year=p[1].split("-")[0],month=p[1].split("-")[1],day=p[1].split("-")[2],time=p[2],Temp=float(p[3]),quality=p[4]))
TableReadings = sqlContext.createDataFrame(tempReadings)
TableReadings.registerTempTable("tempReadings")

AverageTempDaily = TableReadings.select(["year","month","day","station","Temp"]).filter((TableReadings["year"]<=2014) & (TableReadings["year"]>=1960)).groupby(["year","month","day","station"]).agg((F.avg('Temp')).alias("daily_avg_temp")).orderBy(['year','month','station',"daily_avg_temp"],ascending=False)

AverageTempMonthly= AverageTempDaily.select(["year","month","station","daily_avg_temp"]).groupBy(["year","month","station"]).agg((F.avg('daily_avg_temp')).alias("avgMonthlyTemperature")).orderBy("avgMonthlyTemperature",ascending=False)

AverageTempMonthly_rdd = AverageTempMonthly.rdd

AverageTempMonthly.rdd.saveAsTextFile("BDA/output/AverageMonthlyTemp")
