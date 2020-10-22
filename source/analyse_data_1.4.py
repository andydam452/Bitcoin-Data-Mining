import csv
import pandas
import locale
import math
import seaborn as sns
from pylab import savefig

file_path = "D:\Yeat3_Ser1\BigData\KT_Giuaky\ex1"

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

crawl_values = pandas.read_csv(file_path + "\crawl_result.csv")


# parse string into number
for i in crawl_values.columns:
    if (i != 'Date'):
        for j in range (len(crawl_values[i])):
            crawl_values[i][j] = float(locale.atof(crawl_values[i][j]))

#pearson
def average(n):
    if (len(n) > 0):
        return float(sum(n))/len(n)

def pearson_corr(x, y):
    if (len(x) == len(y)) and len(x)>0:
        avg_x = average(x)
        avg_y = average(y)

        diffprod = 0
        xdiff2 = 0
        ydiff2 = 0

        for i in range(len(x)):
            xdiff = x[i] - avg_x
            ydiff = y[i] - avg_y

            diffprod += xdiff * ydiff

            xdiff2 += xdiff * xdiff
            ydiff2 += ydiff * ydiff

        return diffprod / math.sqrt(xdiff2 * ydiff2)

def pearson_into_data(df):

    pearson_corr_result = {
    'Values': ['Open', 'High', 'Low', 'Close', 'Volume','Market Cap'],
    'Open': [],
    'High':[],
    'Low': [],
    'Close' : [],
    'Volume' : [],
    'Market Cap' : []
    }

    for i in range(len(df.columns)):
        j = df.columns[i]
        if (j != 'Date'):
            for h in range(len(df.columns)):
                k = df.columns[h]
                if(df.columns[h] != 'Date'):
                    corr_val = pearson_corr(df[j],df[k])
                    pearson_corr_result[j].append(corr_val)
    
    pear_df = pandas.DataFrame(pearson_corr_result, columns=['Open', 'High', 'Low', 'Close', 'Volume','Market Cap'])
    print(pear_df)

    pearson_heatmap = sns.heatmap(pear_df, annot = True)

    figure = pearson_heatmap.get_figure()
    figure.savefig(file_path + '/pearson_heatmap.png')


def spearman_corr(x, y):
    if (len(x) == len(y)) and len(x) > 0:
        n = len(x)
        diffd = 0
        ndiff = 0
        for i in range(len(x)):
            xydiff = abs(x[i] - y[i])
            diffd += xydiff * xydiff
        ndiff = n*(math.pow(n,2) - 1)
        return float(1 - ((6 * diffd) / ndiff))

def spearman_into_data(df):

    spearman_corr_result = {
    'Values': ['Open', 'High', 'Low', 'Close', 'Volume','Market Cap'],
    'Open': [],
    'High':[],
    'Low': [],
    'Close' : [],
    'Volume' : [],
    'Market Cap' : []
    }

    for i in range(len(df.columns)):
        j = df.columns[i]
        if (j != 'Date'):
            for h in range(len(df.columns)):
                k = df.columns[h]
                if(df.columns[h] != 'Date'):
                    corr_val = spearman_corr(df[j],df[k])
                    spearman_corr_result[j].append(corr_val)
    
    spear_df = pandas.DataFrame(spearman_corr_result, columns=['Open', 'High', 'Low', 'Close', 'Volume','Market Cap'])
    print(spear_df)

    spearman_heatmap = sns.heatmap(spear_df, annot = False)

    figure = spearman_heatmap.get_figure()
    figure.savefig(file_path + '/spearman_heatmap.png')

pearson_into_data(crawl_values)
spearman_into_data(crawl_values)