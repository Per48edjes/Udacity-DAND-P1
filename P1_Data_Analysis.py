import csv
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.stats as stats

# Open the CSV file and extract the data
with open("stroopdata.csv", "rb") as f:
    reader = csv.DictReader(f)
    data_table = list(reader)

# Turn extracted data into two numpy arrays
congruent_list = []
incongruent_list = []
for data_point in data_table:
    congruent_list.append(float(data_point['Congruent']))
    incongruent_list.append(float(data_point['Incongruent']))

Congruent_array = np.array(congruent_list)
Incongruent_array = np.array(incongruent_list)

data_table_list = [congruent_array, incongruent_array]

# Measures of central tendency and variability
i = 0
for condition in data_table_list:
    mean = np.mean(condition)
    median = np.median(condition)
    variance = np.var(condition, ddof=1)
    std_dev = np.std(condition, ddof=1)
    i = i + 1
    if i == 1:
        print 'The following statistics describe the Congruent data:'
    else:
        print ' The following statistics describe the Incongruent data:'
    print(
        'Mean: %6.5r' % mean,
        'Median: %6.5r' % median,
        'Variance: %6.5r' % variance,
        'Standard Deviation: %6.5r' % std_dev
    )


# Histogram of the data
plt.hist(data_table_list, bins='auto')

plt.title('Histogram of Task Performance')
plt.ylabel('Frequency')
plt.xlabel('Time Bins (seconds)')
plt.show()

# Scatter plot where each point is a person and their x, y values are
# their congruent, incongruent times, respectively.

plt.scatter(congruent_array, incongruent_array)
plt.show()


# Differences column
differences_array = np.subtract(congruent_array, incongruent_array)

# Compute the different values needed to perform 2-tailed t-test
mean_differences = np.mean(differences_array)
std_dev_differences = np.std(differences_array, ddof=1)
standard_error = std_dev_differences / math.sqrt(len(data_table))
DoF_ttest = len(data_table) - 1

# Compute the t-statistic
t_stat = mean_differences / standard_error

# Find the t-critical value for a 2-tailed t-test at alpha = 0.5 using SciPy
t_critical = stats.t.isf([0.025], DoF_ttest)

# Determine whether to retain or reject the null hypothesis
print 'For alpha = 0.5 for a two-tail t-test, we can...'
if abs(t_stat) > abs(t_critical):
    print 'Reject the null hypothesis'
else:
    print 'Retain the null hypothesis'

# Check values using SciPy function
print 't-statistic = %.10f pvalue = %.10f' % stats.ttest_rel(congruent_array, incongruent_array)
