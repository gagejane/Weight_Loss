import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import seaborn
from pandas.plotting import scatter_matrix

#read in the data
df = pd.read_csv('/Users/janestout/Dropbox/Projects/weight_loss/history.csv')

#view five structure and first five rows
#print('Original file structure:')
#print(df.info())
#print(df.head())

#original column names are hard to work with; rename
df= df.rename(index=str, columns={'Weight (lb)':'weight', 'Body Fat':'body_fat', 'Muscle Mass':'muscle_mass', 'Water':'water', 'BMI':'bmi', 'Date/Time':'date_time'})

#results are truncated; change display options in order to see all columns
pd.set_option('display.max_columns',None)

#print(df.info())
#print(df.head())

#body fat, muscle mass, and water are stored as character objects; remove % symbol and turn into float using this function
def drop_last(col_list):
    for col in col_list:
        #df['body_fat'] = df['body_fat'].str[:-1]
        df[col] = df[col].str[:-1].astype('float')
col_list = ['body_fat','muscle_mass','water']
drop_last(col_list)

#change date_time to datetime data strucure
df['date_time'] = pd.to_datetime(df['date_time'])

#sort by date and reset index
df = df.sort_values(by='date_time').reset_index(drop=True)

#view data
#print(df)

#case 0 was taken on 2/1; there are no other Feb data, so drop this case
#case 28 has missing data for all varaibles except weight, so drop
df = df.drop([0,28])

#For plotting: Add a column of date ordinals
df['date_ordinal'] = df['date_time'].apply(lambda date_time: date_time.toordinal())

#Make a plot with the ordinals on the date axis
ax = seaborn.regplot(
    data=df,
    x='date_ordinal',
    y='weight',
    ci=None, color='pink'
)

# Tighten up the axes for prettiness
ax.set_xlim(df['date_ordinal'].min() - 10, df['date_ordinal'].max() + 10)
ax.set_ylim(195, 215)

#Replace the ordinal X-axis labels with nice, readable dates
new_labels = df['date_time']
ax.set_xticklabels(new_labels)

#format the date_time varaible so that it shows mo/day
myFmt = DateFormatter("%m/%d")

#plug that format into what is seen on the xaxis
ax.xaxis.set_major_formatter(myFmt)

#make tick marks be the first of each month
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))

#create labels
plt.xlabel('Month/Day', fontweight='bold')
plt.ylabel('Pounds', fontweight='bold')
plt.title("Weight loss from March to June 2019", fontweight='bold')

#save figure
plt.savefig('/Users/janestout/Dropbox/Projects/weight_loss/weight_loss_line1.png')
#plt.show()
# #
#
# df1 = df[['weight','body_fat','bmi','water', 'muscle_mass']]
# scatter_matrix(df1,figsize = (10,10), alpha=.2)
# plt.suptitle('Relationship Between Weight Indicators', fontsize=20, fontweight='bold')
# plt.savefig('/Users/janestout/Dropbox/Projects/weight_loss/weight_loss_scatter_matrix.png')
# #plt.show()
#
# #source for working with date_time: https://www.earthdatascience.org/courses/earth-analytics-python/use-time-series-data-in-python/subset-time-series-data-python/
# df.set_index('date_time', inplace=True)
# march = df['2019-03-01':'2019-03-31']
# april = df['2019-04-01':'2019-04-30']
# may = df['2019-05-01':'2019-05-31']
#
# import math
#
# march_mean = march['weight'].mean()
# march_se = march['weight'].std()/math.sqrt(len(march.index))
# april_mean = april['weight'].mean()
# april_se = april['weight'].std()/math.sqrt(len(april.index))
# may_mean = may['weight'].mean()
# may_se = may['weight'].std()/math.sqrt(len(may.index))
# month = ['March', 'April', 'May']
# means = [march_mean, april_mean, may_mean]
# ses = [march_se, april_se, may_se]
#
# #source for bar plot: http://benalexkeen.com/bar-charts-in-matplotlib/
# x_pos = [i for i,_ in enumerate(month)]
# plt.bar(x_pos, means, color='green', yerr=ses)
# plt.xlabel('Month', fontweight='bold')
# plt.ylabel('Pounds', fontweight='bold')
# plt.title('Average Weight by Month (in lbs)', fontweight='bold')
# plt.xticks(x_pos, month)
# plt.ylim(195,210)
# #plt.show()
# plt.savefig('/Users/janestout/Dropbox/Projects/weight_loss/weight_loss_bar.png')
