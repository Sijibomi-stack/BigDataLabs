
from pyspark import SparkContext
from pyspark.sql import SQLContext, Row
from pyspark.sql import functions as F
sc =SparkContext(appName = "exercise 1")
sqlContext=SQLContext(sc)

station_data = sc.textFile("BDA/input/stations-Ostergotland.csv")
precip_data = sc.textFile("BDA/input/precipitation-readings.csv")

stations = station_data.map(lambda line: line.split(";"))

precip = precip_data.map(lambda line: line.split(";"))

precipReadings = precip.map(lambda p: Row(station=p[0], date=p[1], year=p[1].split("-")[0],
month=p[1].split("-")[1], day=p[1].split("-")[2], time=p[2], precip=float(p[3]), quality=p[4]))
TablePrecipReadings = sqlContext.createDataFrame(precipReadings)
TablePrecipReadings.registerTempTable("precipReadings")

stationReadings = stations.map(lambda x: Row(station=x[0], name=x[1]))
TablestationReadings = sqlContext.createDataFrame(stationReadings)
TablestationReadings.registerTempTable("stationReadings")

TablePrecipReadings = TablePrecipReadings.filter((TablePrecipReadings["year"] >= 1992)&
 (TablePrecipReadings["year"] <= 2016))
TablePrecipReadings = TablePrecipReadings.join(TablestationReadings,"station","inner")
TablePrecipReadings = TablePrecipReadings.groupby(["station","year","month"]).agg(F.sum("precip")).groupby(["year",
"month"]).agg(F.avg("sum(precip)").alias("avg_monthly_precipitation")).orderBy(["year","month"],ascending= False)
TablePrecipReadings.rdd.saveAsTextFile("BDA/output/Qst5")
