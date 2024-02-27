# anomaly-detection-and-control-charting


# Churn Alerting Automation

---

## Table of Contents

[Purpose](#Purpose)\
[Tasks to be done](#Tasks-to-be-done)\
[Features](#Features)\
[Rules](#Rules)\
[Possible Causes By Pattern](#Possible-Causes-By-Pattern)


 
### Purpose

---

This project is about taking variables we know that impact churn and try to systematically monitor them in an automated solution that helps us surface issues faster and more efficiently.

### Tasks to be done

---

- [ ] Determine Process Flow
- [ ] Consider Input Data Structure
- [ ] Build out Rules
- [ ] Build out outlier detection functions
- [ ] Return prioritized ordered list of variables with outliers and charts
- [ ] Run Example 
- [ ] Code Review
- [ ] Share with Team


### Features
---
#### Univariate Outlier Detection Functions
Functions depend on the data we are monitoring.  I will add new functionality on a need basis but the list below shows what we vs what we may want to have.

##### Attributes:
- [X] Bollinger Band - `bollinger_band()`
- [X] P-Chart - `p_chart()`
- [ ] NP Chart - `np()`
- [ ] C Chart - `c()`
- [ ] U Chart - `u()`
- [ ] Mean and Amplitude - `u()`
- [ ] Mean and Standard Deviation - `imrstd()`
- [ ] Individual Values and Moving Range - ` mr() | imrx()`
- [ ] Individual values with subgroups - `u()`
- [ ] Exponentially Weighted Moving Average (EWMA) - `u()`
- [ ] Cumulative Sum (CUSUM) - `u()`

#### Multivariate Outlier Detection Functions

- [ ] T Square Hotelling
- [ ] T Square Hotelling with SubGroup
- [ ] Multivariate Exponentially Weighted Moving Average (MEWMA)

#### Other Charts



<br></br>
[Top](#Churn-Alerting-Automation)
<br></br>

#### Rules
Rules are used to identify when we think out process is out of control.

| Syntax      | Description | Description |
| :-----------: | :----------- | :----------- |
| 1 | Beyond Limits | One or more points beyond the control limits |
| 2 | Zone A | 2 out of 3 consecutive points in Zone A or beyond (2-3 std. dev.)|
| 3 | Zone B | 4 out of 5 consecutive points in Zone B or beyond (1-2 std. dev.) |
| 4 | Zone C| 7 or more consecutive points on one side of the average (in Zone C or beyond / 0+ std. dev.) |
| 5 | Trend | 7 consecutive points trending up or trending down |
| 6 | Mixture | 8 consecutive points with no points in Zone C |
| 7 | Stratification | 15 consecutive points in Zone C |
| 8 | Over-control | 14 consecutive points alternating up and down |

*Note: Not all rules apply to all types of control charts.*

##### Other common rules:
1. If one or more points falls outside of the upper control limit (UCL), or lower control limit (LCL). The UCL and LCL are three standard deviations on either side of the mean.
2. If two out of three successive points fall in the area that is beyond two standard deviations from the mean, either above or below.
3. If four out of five successive points fall in the area that is beyond one standard deviation from the mean, either above or below.
4. If there is a run of six or more points that are all either successively higher or successively lower.
5. If eight or more points fall on either side of the mean (some organization use 7 points, some 9).
6. If 15 points in a row fall within the area on either side of the mean that is one standard deviation from the mean.

<br></br>
[Top](#Churn-Alerting-Automation)
<br></br>

#### Possible Causes By Pattern

It is difficult to list possible causes for each pattern because special causes (just like common causes) are very dependent on the type of process.  Manufacturing processes have different issues that service processes.  Different types of control chart look at different sources of variation.  Still, it is helpful to show some possible causes by pattern description.  Table 3 attempts to do this based on the type of pattern. 

<br></br>


<p style="text-align: center;"><b>Table: Possible Causes by Pattern</b></p>

| Pattern Description | Rules | Possible Causes |
| :----------- | :-----------: | :----------- |
| Large shifts from the average | 1, 2 | New person doing the job  <br> Wrong setup <br> Measurement error <br> Process step skipped <br> Process step not completed <br> Power failure <br> Equipment breakdown <br> Weather event <br> Pandemic| 
| Small shifts from the average | 3, 4  | Previous Causes and/or <br> Raw material change <br> Change in work instruction <br> Different measurement device/calibration <br> Different shift <br> Person gains greater skills in doing the job <br> Change in maintenance program <br> Change in setup procedure |
| Trends | 5 | Competitive encroachment <br> Temperature effects (cooling, heating) | 
| Mixtures | 6 | More than one process present (e.g. shifts, machines) |
| Stratifications | 7 | More than one process present (e.g. shifts, machines) |
| Over-control | 8 | Tampering by operator <br> Alternating raw materials| 


<br></br>
##### Rules 1 - 4:
![Rules_1-4](assets/images/rules-1-4.png)
<br></br>
[Top](#Churn-Alerting-Automation)
<br></br>
##### Rules 5 - 6
![Rules_5-6](assets/images/rules-5-6.png)
<br></br>
[Top](#Churn-Alerting-Automation)
<br></br>
##### Rules 7 - 8
![Rules_7-8](assets/images/rules-7-8.png)

<br></br>
[Top](#Churn-Alerting-Automation)
<br></br>

### Usage Installation / Execution TBD 

---
TBD

[Top](#Churn-Alerting-Automation)
