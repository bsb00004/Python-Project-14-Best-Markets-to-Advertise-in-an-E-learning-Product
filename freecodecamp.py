#!/usr/bin/env python
# coding: utf-8

### Python Project 14:-  Finding the Two Best Markets to Advertise in an E-learning Product
# In this project, we'll aim to find the two best markets to advertise our product in — we're working for an e-learning company 
# that offers courses on programming. Most of our courses are on web and mobile development, 
# but we also cover many other domains, like data science, game development, etc.

#### Understanding the Data
# The survey data is publicly available in [this GitHub repository](https://github.com/freeCodeCamp/2017-new-coder-survey). 
# Below, we'll do a quick exploration of the 2017-fCC-New-Coders-Survey-Data.csv file stored in the `clean-data` 
# folder of the repository we just mentioned. 

#### Exploring Data
# Read in the data
import pandas as pd
direct_link = 'https://raw.githubusercontent.com/freeCodeCamp/2017-new-coder-survey/master/clean-data/2017-fCC-New-Coders-Survey-Data.csv'
fcc = pd.read_csv(direct_link, low_memory = 0) # low_memory = False to silence dtypes warning

# Quick exploration of the data
# print number of rows and columns
print(fcc.shape)
pd.options.display.max_columns = 150 # to avoid truncated output 

# print the first 5 rows
fcc.head()


# ### Checking for Sample Representativity
# For the purpose of our analysis, we want to answer questions about a population of new coders that are interested in the subjects we teach. We'd like to know:
# - Where are these new coders located.
# - What locations have the greatest densities of new coders.
# - How much money they're willing to spend on learning.

# So we first need to clarify whether the data set has the right categories of people for our purpose. 
# So let's take a look at the frequency distribution table of this column and determine whether the data we have is relevant.

# Frequency distribution table for 'JobRoleInterest'
fcc['JobRoleInterest'].value_counts(normalize = True) * 100

# It'd be useful to get a better picture of how many people are interested in a single subject and how many have mixed interests. 
# Consequently, in the next code block, we'll:

# Split each string in the 'JobRoleInterest' column
interests_no_nulls = fcc['JobRoleInterest'].dropna()
splitted_interests = interests_no_nulls.str.split(',')

# Frequency table for the var describing the number of options
n_of_options = splitted_interests.apply(lambda x: len(x)) # x is a list of job options
n_of_options.value_counts(normalize = True).sort_index() * 100

# The focus of most courses is on web and mobile development, 
# so let's find out how many respondents chose at least one of these two options.

# Frequency table
web_or_mobile = interests_no_nulls.str.contains(
    'Web Developer|Mobile Developer') # returns an array of booleans
freq_table = web_or_mobile.value_counts(normalize = True) * 100
print(freq_table)

# Graph for the frequency table above
get_ipython().magic('matplotlib inline')
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

freq_table.plot.bar()
plt.title('Most Participants are Interested in \nWeb or Mobile Development',
          y = 1.08) # y pads the title upward
plt.ylabel('Percentage', fontsize = 12)
plt.xticks([0,1],['Web or mobile\ndevelopment', 'Other subject'],
           rotation = 0) # the initial xtick labels were True and False
plt.ylim([0,100])
plt.show()
 
# It turns out that most people in this survey (roughly 86%) are interested in either web or mobile development. 
# Now we need to figure out what are the best markets to invest money in for advertising the courses. We'd like to know:
# - Where are these new coders located.
# - What are the locations with the greatest number of new coders.
# - How much money new coders are willing to spend on learning.

#### New Coders - Locations and Densities
# We can start by examining the frequency distribution table of the CountryLive variable,  
# We'll only consider those participants who answered what role(s) they're interested in,
# to make sure we work with a representative sample.

# Isolate the participants that answered what role they'd be interested in
fcc_good = fcc[fcc['JobRoleInterest'].notnull()].copy()

# Frequency tables with absolute and relative frequencies
absolute_frequencies = fcc_good['CountryLive'].value_counts()
relative_frequencies = fcc_good['CountryLive'].value_counts(normalize = True) * 100

# Display the frequency tables in a more readable format
pd.DataFrame(data = {'Absolute frequency': absolute_frequencies, 
                     'Percentage': relative_frequencies}
            )
# ### Spending Money for Learning
# Let's start with creating a new column that describes the amount of money a student has spent per month so far. 
# To do that, we'll need to divide the MoneyForLearning column to the MonthsProgramming column. 
# The problem is that some students answered that they have been learning to code for 0 months 
# (it might be that they have just started). To avoid dividing by 0, we'll replace 0 with 1 in the MonthsProgramming column.

# Replace 0s with 1s to avoid division by 0
fcc_good['MonthsProgramming'].replace(0,1, inplace = True)

# New column for the amount of money each student spends each month
fcc_good['money_per_month'] = fcc_good['MoneyForLearning'] / fcc_good['MonthsProgramming']
# print sum of null values
fcc_good['money_per_month'].isnull().sum()

# Let's keep only the rows that don't have null values for the money_per_month column.

# Keep only the rows with non-nulls in the `money_per_month` column 
fcc_good = fcc_good[fcc_good['money_per_month'].notnull()]
# print sum of Not null values
fcc_good['money_per_month'].notnull().sum()

# We want to group the data by country, and then measure the average amount of money that students spend per month in each country.
# First, let's remove the rows having null values for the CountryLive column, and check out if 
# we still have enough data for the four countries that interest us.

# Remove the rows with null values in 'CountryLive'
fcc_good = fcc_good[fcc_good['CountryLive'].notnull()]

# Frequency table to check if we still have enough data
fcc_good['CountryLive'].value_counts().head()
 
# This should be enough, so let's compute the average value spent per month in each country by a student. 
# We'll compute the average using the mean.

# Mean sum of money spent by students each month
countries_mean = fcc_good.groupby('CountryLive').mean()
countries_mean['money_per_month'][['United States of America',
                            'India', 'United Kingdom',
                            'Canada']]

#### Dealing with Extreme Outliers
# Let's use box plots to visualize the distribution of the money_per_month variable for each country.

# Isolate only the countries of interest
only_4 = fcc_good[fcc_good['CountryLive'].str.contains(
    'United States of America|India|United Kingdom|Canada')]

# Box plots to visualize distributions
import seaborn as sns
sns.boxplot(y = 'money_per_month', x = 'CountryLive',
            data = only_4)
plt.title('Money Spent Per Month Per Country\n(Distributions)',
         fontsize = 16)
plt.ylabel('Money per month (US dollars)')
plt.xlabel('Country')
plt.xticks(range(4), ['US', 'UK', 'India', 'Canada']) # avoids tick labels overlap
plt.show()

# It's hard to see on the plot above if there's anything wrong with the data for the United Kingdom, India, or Canada, 
# but we can see immediately that there's something really off for the US: two persons spend each month \$50000 or more for learning. 
# This is not impossible, but it seems extremely unlikely, so we'll remove every value that goes over \$20,000 per month.

# Isolate only those participants who spend less than 10000 per month
fcc_good = fcc_good[fcc_good['money_per_month'] < 20000]

# Now let's recompute the mean values and plot the box plots again.
# Recompute mean sum of money spent by students each month
countries_mean = fcc_good.groupby('CountryLive').mean()
countries_mean['money_per_month'][['United States of America',
                            'India', 'United Kingdom',
                            'Canada']]

# Isolate again the countries of interest
only_4 = fcc_good[fcc_good['CountryLive'].str.contains(
    'United States of America|India|United Kingdom|Canada')]

# Box plots to visualize distributions
sns.boxplot(y = 'money_per_month', x = 'CountryLive',
            data = only_4)
plt.title('Money Spent Per Month Per Country\n(Distributions)',
         fontsize = 16)
plt.ylabel('Money per month (US dollars)')
plt.xlabel('Country')
plt.xticks(range(4), ['US', 'UK', 'India', 'Canada']) # avoids tick labels overlap
plt.show()

# We can see a few extreme outliers for India (values over \$2500 per month), but it's unclear whether this is good data or not. 
# Maybe these persons attended several bootcamps, which tend to be very expensive. 
# Let's examine these two data points to see if we can find anything relevant.

# Inspect the extreme outliers for India
india_outliers = only_4[
    (only_4['CountryLive'] == 'India') & 
    (only_4['money_per_month'] >= 2500)]
india_outliers

# It seems that neither participant attended a bootcamp. They might have misunderstood and thought university tuition is included. 
# It seems safer to remove these two rows.

# Remove the outliers for India
only_4 = only_4.drop(india_outliers.index) # using the row labels

# Looking back at the box plot above, we can also see more extreme outliers for the US (values over \$6000 per month).
# Examine the extreme outliers for the US
us_outliers = only_4[
    (only_4['CountryLive'] == 'United States of America') & 
    (only_4['money_per_month'] >= 6000)]

us_outliers

# Remove the respondents who didn't attendent a bootcamp
no_bootcamp = only_4[
    (only_4['CountryLive'] == 'United States of America') & 
    (only_4['money_per_month'] >= 6000) &
    (only_4['AttendedBootcamp'] == 0)
]

only_4 = only_4.drop(no_bootcamp.index)


# Remove the respondents that had been programming for less than 3 months
less_than_3_months = only_4[
    (only_4['CountryLive'] == 'United States of America') & 
    (only_4['money_per_month'] >= 6000) &
    (only_4['MonthsProgramming'] <= 3)
]

only_4 = only_4.drop(less_than_3_months.index)


# We can also see an extreme outlier for Canada — a person who spends roughly \$5000 per month.
# Examine the extreme outliers for Canada
canada_outliers = only_4[
    (only_4['CountryLive'] == 'Canada') & 
    (only_4['money_per_month'] > 4500)]

canada_outliers


# This participant had been programming for no more than two months when he completed the survey. 
# He seems to have paid a large sum of money in the beginning to enroll in a bootcamp, and then he 
# probably didn't spend anything for the next couple of months after the survey.

# Remove the extreme outliers for Canada
only_4 = only_4.drop(canada_outliers.index)

# Let's recompute the mean values and generate the final box plots.

# Recompute mean sum of money spent by students each month
only_4.groupby('CountryLive').mean()['money_per_month']

# Visualize the distributions again
sns.boxplot(y = 'money_per_month', x = 'CountryLive',
            data = only_4)
plt.title('Money Spent Per Month Per Country\n(Distributions)',
          fontsize = 16)
plt.ylabel('Money per month (US dollars)')
plt.xlabel('Country')
plt.xticks(range(4), ['US', 'UK', 'India', 'Canada']) # avoids tick labels overlap
plt.show()

#### Choosing the Two Best Markets
# The data suggests strongly that we shouldn't advertise in the UK, but let's take a second look at India before deciding to choose Canada as our second best choice:

# Frequency table for the 'CountryLive' column
only_4['CountryLive'].value_counts(normalize = True) * 100

#### Conclusion
# The only solid conclusion we reached is that the US would be a good market to advertise in.
# For the second best market, it wasn't clear-cut what to choose between India and Canada. 
# We decided to send the results to the marketing team so they can use their domain knowledge to take the best decision.
