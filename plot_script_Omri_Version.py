import pandas as pd
import numpy as np
import seaborn as sns
from stat_funcs import *

data_dir = './analyzed/'

data_completion = pd.read_csv(data_dir + 'repetition_results_new.csv')


survey_data = pd.read_csv(data_dir + 'survey_data.csv')

#survey_data_no_understand = survey_data[survey_data['Q8_1'].str.contains('Neither Agree nor Disagree')
#                                        | survey_data['Q8_1'].str.contains('Disagree')
#                                        | survey_data['Q8_1'].str.contains('Strongly Disagree')]

no_understand = ['SVG0060', 'SVG0077', 'SVG0097', 'SVG0099', 'SVG0199','SVG0126']

data_completion_AC = data_completion[~data_completion['Subject_ID'].str.contains(no_understand[0])]
data_completion_AC = data_completion[~data_completion['Subject_ID'].str.contains(no_understand[1])]
data_completion_AC = data_completion[~data_completion['Subject_ID'].str.contains(no_understand[2])]
data_completion_AC = data_completion[~data_completion['Subject_ID'].str.contains(no_understand[3])]
data_completion_AC = data_completion[~data_completion['Subject_ID'].str.contains(no_understand[4])]
data_completion_AC = data_completion[~data_completion['Subject_ID'].str.contains(no_understand[5])]

data_completion_AC_reform = pd.melt(data_completion_AC, value_vars=['%_diatonic', '%_chromatic'])

sns.set_context("talk")
ax = sns.boxplot(x="variable", y="value", data=data_completion_AC_reform, saturation=.5)
sns.despine()

sns.set_context("talk")
sns.displot(data_completion_AC_reform, x="value", hue="variable", kind="kde", fill=True)
sns.despine()


perm_bias_paired(data_completion_AC['%_diatonic'], data_completion_AC['%_chromatic'], 10000)
