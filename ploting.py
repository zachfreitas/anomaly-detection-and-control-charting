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
Churn_Alerting_Automation/Alerting_Plots_Module.py
@zfreitas
zfreitas Works beginning to end
Latest commit 60177b6 on Apr 29, 2021
 History
 1 contributor
92 lines (64 sloc)  3.04 KB
 

# General Libraries
import pandas as pd
import numpy as np
# %matplotlib inline # This code is for output that works with Notebooks.


# Spark Stuff
from pyspark.sql import DataFrame
from pyspark.sql.functions import udf, col, count, sum, when, avg, mean, min
import pyspark.sql.functions as sf
from pyspark.sql.types import *
from pyspark.sql.window import Window

from atg_pyspark.client import SparkCommandClient
from connections import open_connection, Connection

import pyspark




########################################################################
# Function: Alert Plotting Function

def plot_alert(initial_df: DataFrame, title: str = "", X_axis_lbl: str = "", Y_axis_lbl: str = ""):
    import matplotlib.pyplot as plt
    import matplotlib.pyplot as plt
    plt.style.use('classic')
    import numpy as np
    import pandas as pd
    
    # Sort the data Properly    
    #Option: sf.to_timestamp(sf.col("Activation Month BOP"), 'dd/MM/yyyy HH:mm:ss').alias("date"), 
    initial_df = (initial_df.toPandas()).sort_values(by= "date")

    # Set Variables
    date = np.array(initial_df['date'])
    actuals = np.array(initial_df['actuals'])
    bar = np.array(initial_df['bar'])
    ucl = np.array(initial_df['ucl'])
    lcl = np.array(initial_df['lcl'])
    colors = np.array(initial_df['RULE_1_BEYOND_3SIGMA'].apply(lambda x: 'r' if x == 1 else 'g'))
    color_lbl = np.array(initial_df['RULE_1_BEYOND_3SIGMA'].apply(lambda x: 'SPV' if x == 1 else 'CCV'))

    # Chart Limit Sizing
    if np.min(lcl) <= np.min(actuals): 
        y_lw_lim = np.min(lcl) - np.min(lcl) * 0.1
    else:
        y_lw_lim = np.min(actuals) - np.min(actuals) * 0.1
    
    if np.max(ucl) >= np.max(actuals): 
        y_up_lim = np.max(ucl) + np.max(ucl) * 0.1
    else:
        y_up_lim = np.max(actuals) + np.max(actuals) * 0.1
    
        

    from matplotlib.ticker import PercentFormatter
    
    plt.clf() # Clear the space
        

    fig = plt.figure(2, figsize=[15, 10])  # an empty figure with no Axes and adjust the size
    
      # Change the size of the output!
    plt.grid(which="major", axis="y")
    plt.scatter(date, actuals, color=colors, zorder=10)  # Plot some data on the axes.
    plt.plot(date, actuals,  color="b", zorder=2,  label="Actuals")  # Plot some data on the axes.
    plt.step(
        date, ucl, where="mid", label="ucl", linestyle="--", color="r", linewidth=2
    )
    plt.plot(date, bar, color="g", linewidth=2, linestyle=":")

    plt.step(
        date, lcl, where="mid", label="lcl", linestyle="--", color="r", linewidth=2
    )
    plt.xticks(date, rotation=90)
    plt.fill_between(date, np.array(lcl, dtype=float), np.array(ucl, dtype=float), alpha=0.1, color='green', interpolate=True, step='mid')
    plt.ylim(y_lw_lim, y_up_lim)
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    
    plt.xlabel(X_axis_lbl, size = 15)  # Add an x-label to the axes.
    plt.ylabel(Y_axis_lbl, size = 15)  # Add a y-label to the axes.
    plt.title(title, size = 25) # Add a title to the axes.
    plt.legend() # Add a legend.
    
    plt.show()
    
    
    
    
    
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
Churn_Alerting_Automation/Alerting_Plots_Module.py at 5b0b452824c7648f699ea2240463996191b1cd42 · zfreitas/Churn_Alerting_Automation