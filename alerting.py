Skip to content
 Enterprise
Search or jump to…
Pull requests
Issues
Explore
 
@zfreitas 
zfreitas
/
Churn_Alerting_Automation
Private
Fork your own copy of zfreitas/Churn_Alerting_Automation
Code
Issues
Pull requests
Projects
1
Wiki
Security
Insights
Settings
Churn_Alerting_Automation/Alerting_Functions_Module.py
@zfreitas
zfreitas Works beginning to end
Latest commit 60177b6 on Apr 29, 2021
 History
 1 contributor
180 lines (147 sloc)  8.96 KB
 


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 23:57:39 2021
@author: zfreitas
"""
# Load Libraries

# General Libraries
import pandas as pd
import numpy as np

# Spark Stuff
from pyspark.sql import DataFrame
from pyspark.sql.functions import udf, col, count, sum, when, avg, mean, min
import pyspark.sql.functions as sf
from pyspark.sql.types import *
from pyspark.sql.window import Window

from atg_pyspark.client import SparkCommandClient
from connections import open_connection, Connection

import pyspark
# spark = pyspark.sql.SparkSession.builder.getOrCreate() 

# from ganymede.spark import initialize_spark_cluster, ExecutorOption
# spark = initialize_spark_cluster(
#     ExecutorOption.SPARK_4_CPU_30_GB,
#     num_executors = 10,
#     **{
#         'spark.driver.maxResultSize': '10G',
#         'spark.rpc.message.maxSize': '300'
#     }
# )

########################################################################
# Helper Functions

# get the shape of a pyspark dataframe.
def get_shape(data):
    Rows = data.count()
    Columns = len(data.columns)
    return print("Rows:", Rows,", Columns:", Columns)


########################################################################
# Function: Proportions Alert
def proportions(initial_df: DataFrame, sd: float = 2)-> DataFrame: #pd.DataFrame: 
    
    # Number of Standard Deviations
    d = sd
    
    updated_df = (initial_df
                  .select(sf.col("date"),
                          sf.col("num"),
                          sf.col("dnom"))
                  .sort(sf.col("date").asc())
                  .withColumn("actuals", sf.col("num") / sf.col("dnom"))
                  .withColumn("dnom_sum", sf.sum("dnom").over(Window.orderBy()))
                  .withColumn("num_sum", sf.sum("num").over(Window.orderBy()))
                  .withColumn("bar", sf.col("num_sum") / sf.col("dnom_sum"))
                  .withColumn("error", (((sf.col("bar") * (1 - sf.col("bar"))) / sf.col("dnom")) ** 0.5))
                  .withColumn("ucl", sf.col("bar") + ( d * sf.col("error")))
                  .withColumn("lcl", sf.col("bar") - ( d * sf.col("error")))
                  .withColumn("RULE_1_BEYOND_3SIGMA", sf.when((sf.col("actuals") < sf.col("lcl")) | (sf.col("actuals") > sf.col("ucl")), 1).otherwise(0)) # Rules
                  .withColumn("side", sf.when((sf.col("actuals") < sf.col("bar")), 1).otherwise(0)) # Rules
                  .withColumn("side_row_num",sf.row_number().over(Window.partitionBy("side").orderBy("date")))
                 )
    
    #data = updated_df.select("*").toPandas()
    #data = data.sort_values(by=['date'], ascending=True).reset_index(drop=True)
    return updated_df #data


########################################################################
# Function: Laney P-Chart Alert
def laneyp(initial_df: DataFrame, sd: float = 2)-> DataFrame: #pd.DataFrame: 
    
    # Number of Standard Deviations
    d = sd
    
    updated_df = (initial_df
                  .select(sf.col("date"),
                          sf.col("num"),
                          sf.col("dnom"))
                  .sort(sf.col("date").asc())
                  .withColumn("actuals", sf.col("num") / sf.col("dnom"))
                  .withColumn("dnom_sum", sf.sum("dnom").over(Window.orderBy()))
                  .withColumn("num_sum", sf.sum("num").over(Window.orderBy()))
                  .withColumn("bar", sf.col("num_sum") / sf.col("dnom_sum"))
                  .withColumn("zvalue", ( (sf.col("actuals")-sf.col("bar")) / ((sf.col("bar") * (1 - sf.col("bar"))) / sf.col("dnom")) ** 0.5)) # Z Value
                  .withColumn("mR", sf.abs(sf.col("zvalue") - sf.lag("zvalue", 1).over(Window.orderBy("date")))) # Absolute Moving Range
                  .withColumn("zstd", (sf.avg(sf.col("mR")).over(Window.orderBy()) / sf.lit(1.128)))   # Average Range / constant = zstd
                  .withColumn("error", sf.col("zstd") * (((sf.col("bar") * (1 - sf.col("bar"))) / sf.col("dnom")) ** 0.5))              
                  .withColumn("ucl", sf.col("bar") + ( d * sf.col("error")))
                  .withColumn("lcl", sf.col("bar") - ( d * sf.col("error")))
                  .withColumn("RULE_1_BEYOND_3SIGMA", sf.when((sf.col("actuals") < sf.col("lcl")) | (sf.col("actuals") > sf.col("ucl")), 1).otherwise(0)) # Rules
                  .withColumn("side", sf.when((sf.col("actuals") < sf.col("bar")), 1).otherwise(0)) # Rules
                  .withColumn("side_row_num",sf.row_number().over(Window.partitionBy("side").orderBy("date")))
                 ) 
    
    #data = updated_df.select("*").toPandas()
    #data = data.sort_values(by=['date'], ascending=True).reset_index(drop=True)
    return updated_df #data    

########################################################################
# Function: Bollinger Bands Alert    
def bollinger_band(initial_df: DataFrame, lookback: int = 14, sd: float = 2)-> DataFrame: #pd.DataFrame: 
    
    n = lookback
    
    # Number of Standard Deviations
    d = sd

    #create window by casting timestamp to long (number of seconds)
    w = (Window.orderBy(sf.col("date").cast('long')).rowsBetween(-n, 0))
    
    updated_df = (initial_df
                  .select(sf.col("date"),
                          sf.col("actuals"))
                  .sort(sf.col("date").asc())
                  .withColumn("bar", sf.avg("actuals").over(Window.orderBy())) # Mean
                  .withColumn("sq_dev_frm_mean", (sf.col("bar")-sf.col("actuals"))**2) # Squared Deviation from mean.
                  .withColumn("SSQ", sf.sum("sq_dev_frm_mean").over(Window.orderBy())) # Sum of Squares AKA: SSQ
                  .withColumn("std", (sf.col("SSQ") / (sf.count("SSQ").over(Window.orderBy()) - 1))**0.5) # (SSQ/(n-1))^0.5 
                  .withColumn('rolling_mean', sf.avg("actuals").over(w))
                  .withColumn("rolling_sq_dev_frm_mean", (sf.col("rolling_mean")-sf.col("actuals"))**2) # Rolling Squared Deviation from mean.
                  .withColumn('rolling_SSQ', sf.sum("rolling_sq_dev_frm_mean").over(w))
                  .withColumn("rolling_std", (sf.col("rolling_SSQ") / (sf.count("rolling_SSQ").over(w) - 1))**0.5) # (SSQ/(n-1))^0.5 for window AKA: Std Dev.
                  .withColumn("lcl", sf.col("rolling_mean") - (d * sf.col("rolling_std")))
                  .withColumn("ucl", sf.col("rolling_mean") + (d * sf.col("rolling_std")))
                  .withColumn("RULE_1_BEYOND_3SIGMA", sf.when((sf.col("actuals") < sf.col("lcl")) | (sf.col("actuals") > sf.col("ucl")), 1).otherwise(0)) # Rules
                  .withColumnRenamed('bar', 'bar1')
                  .withColumnRenamed('rolling_mean', 'bar')
                 )
    
#     data = updated_df.select("*").toPandas()
#     data = data.sort_values(by=['date'], ascending=True).reset_index(drop=True)
    return updated_df
            
    
    
    

########################################################################
# Function: Bollinger Bands for Binomial Data Alert    
def bollinger_band_p(initial_df: DataFrame)-> DataFrame: #pd.DataFrame:    
    
    d = 2
    # Lookback
    n = 14
    # create window by casting timestamp to long (number of seconds)
    w = Window.orderBy(sf.col("date").cast("long")).rowsBetween(-n, 0)
    
    updated_df = (initial_df
                  .select(sf.col("date"), sf.col("num"), sf.col("dnom"))
                  .sort(sf.col("date").asc())
                  .withColumn("actuals", sf.col("num") / sf.col("dnom"))
                  .withColumn("dnom_sum", sf.sum("dnom").over(Window.orderBy()))
                  .withColumn("num_sum", sf.sum("num").over(Window.orderBy()))
                  .withColumn("bar", sf.col("num_sum") / sf.col("dnom_sum"))
                  .withColumn("error", d * (((sf.col("bar") * (1 - sf.col("bar"))) / sf.col("dnom")) ** 0.5))
                  .withColumn("rolling_dnom_sum", sf.sum("dnom").over(w))
                    .withColumn("rolling_num_sum", sf.sum("num").over(w))
                  .withColumn("rolling_bar", sf.col("rolling_num_sum") / sf.col("rolling_dnom_sum"))
                  .withColumn("rolling_error", d * (((sf.col("rolling_bar") * (1 - sf.col("rolling_bar"))) / sf.col("dnom"))** 0.5))  # Rolling Deviation from Mean
                  .withColumn("sqd_dev", sf.col("rolling_error")**2) # Squared Deviation
                  .withColumn("rolling_ssq", sf.sum("sqd_dev").over(w)) # Rolling Sum of Squares
                  .withColumn("ssq_avg", sf.col("rolling_ssq")/(n-1)) # SSQ/(n-1)
                  .withColumn("std_dev", sf.col("ssq_avg")**0.5) # The Standard Deviation
                  .withColumn("lcl", sf.col("rolling_bar") - (d * sf.col("std_dev")))
                  .withColumn("ucl", sf.col("rolling_bar") + (d * sf.col("std_dev")))
                  .withColumn("RULE_1_BEYOND_3SIGMA", sf.when((sf.col("actuals") < sf.col("lcl")) | (sf.col("actuals") > sf.col("ucl")), 1).otherwise(0))  # Rules
                )    
    
#     data = updated_df.select("*").toPandas()
#     data = data.sort_values(by=['date'], ascending=True).reset_index(drop=True)
    return updated_df
        
FooterViaSat, Inc.
ViaSat, Inc.
ViaSat, Inc.
© 2024 GitHub, Inc.
Footer navigation
Help
Support
API
Training
Blog
About
GitHub Enterprise Server 3.10.3
Churn_Alerting_Automation/Alerting_Functions_Module.py at 5b0b452824c7648f699ea2240463996191b1cd42 · zfreitas/Churn_Alerting_Automation