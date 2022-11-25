from pyspark import SparkContext
from pyspark.sql import SQLContext, Row
from pyspark.sql import functions as F
sc =SparkContext(appName = "exercise 1")
sqlContext=SQLContext(sc)

temp_data = sc.textFile("BDA/input/temperature-readings.csv")
precip_data = sc.textFile("BDA/input/precipitation-readings.csv")

lines_temp = temp_data.map(lambda lines: lines.split(";"))
lines_precip = precip_data.map(lambda lines: lines.split(";"))

tempReadings = lines_temp.map(lambda p: Row(station=p[0],date=p[1],year=p[1].split("-")[0],
month=p[1].split("-")[1],time=p[2],  Temp=float(p[3]),quality=p[4]))

precipReadings = lines_precip.map(lambda p: Row(station=p[0], date=p[1], year=p[1].split("-")[0],
month=p[1].split("-")[1], day=p[1].split("-")[2], time=p[2], precip=float(p[3]), quality=p[4]))

TableTempReadings = sqlContext.createDataFrame(tempReadings)
TableTempReadings.registerTempTable("tempReadings")

TablePrecipReadings = sqlContext.createDataFrame(precipReadings)
TablePrecipReadings.registerTempTable("precipReadings")

maximum_temperature = TableTempReadings.select(["station","Temp"]).groupby("station").agg(F.max('Temp').alias("MaxTemp")).orderBy('MaxTemp',ascending=False)
maximum_temperature = maximum_temperature.select(["station","MaxTemp"]).filter((maximum_temperature["MaxTemp"] >= 25) & (maximum_temperature["MaxTemp"] <= 30))

maximum_precipitation_daily = TablePrecipReadings.select(["station","year","month","day","precip"]).groupby(["station","year","month","day"]).agg(F.sum("precip").alias("daily_precip_sum")).orderBy("daily_precip_sum",ascending=False)
maximum_precipitation =maximum_precipitation_daily.select(["station","daily_precip_sum"]).groupby("station").agg(F.max("daily_precip_sum").alias("maxDailyPrecipitation")).orderBy("station",ascending=False)
maximum_precipitationFiltered = maximum_precipitation.filter((maximum_precipitation["maxDailyPrecipitation"] > 100) & (maximum_precipitation["maxDailyPrecipitation"] < 200))

Result = maximum_temperature.join(maximum_precipitationFiltered,"station","inner").orderBy("station",ascending=False)

Result.rdd.saveAsTextFile("BDA/output/Qst4")
