# Copyright (c) 2016. Mount Sinai School of Medicine
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

def plot_kmf(df, 
             condition_col, 
             censor_col, 
             survival_col, 
             threshold=None,
             title=None,
             xlabel=None,
             ax=None,
             print_as_title=False):
    """
    Plot survival curves by splitting the dataset into two groups based on
    condition_col

    if threshold is defined, the groups are split based on being > or <
    condition_col

    if threshold == 'median', the threshold is set to the median of condition_col

    Parameters
    ----------
        df: dataframe
        condition_col: string, column which contains the condition to split on
        survival_col: string, column which contains the survival time
        censor_col: string,
        threshold: int or string, if int, condition_col is thresholded,
                                  if 'median', condition_col thresholded 
                                  at its median
        title: Title for the plot, default None
        ax: an existing matplotlib ax, optional, default None
        print_as_title: bool, optional, whether or not to print text
          within the plot's title vs. stdout, default False
    """
    kmf = KaplanMeierFitter()
    if threshold is not None:
        if threshold == 'median':
            threshold = df[condition_col].median()
        condition = df[condition_col] > threshold
        label = '{} > {}'.format(condition_col, threshold)
    else:
        condition = df[condition_col]
        label = '{}'.format(condition_col)

    df_with_condition = df[condition]
    df_no_condition = df[~condition]
    survival_no_condition = df_no_condition[survival_col]
    survival_with_condition = df_with_condition[survival_col]

    event_no_condition = (df_no_condition[censor_col].astype(bool))
    event_with_condition = (df_with_condition[censor_col].astype(bool))
             
    kmf.fit(survival_no_condition, event_no_condition, label="")
    if ax:
        kmf.plot(ax=ax, show_censors=True, ci_show=False)
    else:
        ax = kmf.plot(show_censors=True, ci_show=False)

    kmf.fit(survival_with_condition, event_with_condition, label=(label))
    kmf.plot(ax=ax, show_censors=True, ci_show=False)

    # Set the y-axis to range 0 to 1
    ax.set_ylim(0, 1)

    no_cond_str = "# no condition {}".format(len(survival_no_condition))
    cond_str = "# with condition {}".format(len(survival_with_condition))
    if title:
        ax.set_title(title)
    elif print_as_title:
        ax.set_title("%s | %s" % (no_cond_str, cond_str))
    else:
        print(no_cond_str)
        print(cond_str)

    if xlabel:
        ax.set_xlabel(xlabel)
 
    results = logrank_test(survival_no_condition, 
                           survival_with_condition, 
                           event_observed_A=event_no_condition, 
                           event_observed_B=event_with_condition)
    return results

def logrank(df,
            condition_col,
            censor_col,
            survival_col,
            threshold=None):
    if threshold is not None:
        if threshold == 'median':
            threshold = df[condition_col].median()
        condition = df[condition_col] > threshold
    else:
        condition = df[condition_col]
    df_with_condition = df[condition]
    df_no_condition = df[~condition]
    survival_no_condition = df_no_condition[survival_col]
    survival_with_condition = df_with_condition[survival_col]
    event_no_condition = (df_no_condition[censor_col].astype(bool))
    event_with_condition = (df_with_condition[censor_col].astype(bool))
    return logrank_test(survival_no_condition, 
                        survival_with_condition, 
                        event_observed_A=event_no_condition, 
                        event_observed_B=event_with_condition)
