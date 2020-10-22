import csv
import pandas as pd
import locale
import random
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score

file_path = "D:\Yeat3_Ser1\BigData\KT_Giuaky\ex1"

def loadCSV():
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    crawl_values = pd.read_csv(file_path + "\crawl_result.csv")

    # parse string into number
    for i in crawl_values.columns:
        if (i != 'Date'):
            for j in range (len(crawl_values[i])):
                crawl_values[i][j] = float(locale.atof(crawl_values[i][j]))
    
    return crawl_values

df = loadCSV()

open_col = df['Open'].head(30)
close_col = df['Close'].head(30)
vol_col = df['Volume'].head(31)
mkcap_col = df['Market Cap'].head(31)

open_close = close_col - open_col
statelst = []
for i in open_close:
  if i > 0 :
    statelst.append(1)
  else:
    statelst.append(0)

# xác suất trong 1 tháng gần nhất của statelst
rate_up = 0
rate_down = 0

for i in statelst:
  if i == 1:
    rate_up += 1
  else:
    rate_down += 1

P_up = rate_up/len(statelst)
P_down = 1-P_up

#xác xuất volume tăng và statelst tăng
vol_up_down = []
for i in range(len(vol_col)-1):
  if vol_col[i+1] - vol_col[i] < 0:
    vol_up_down.append(1)
  else :  
    vol_up_down.append(0)


count_vol_statelst_up = 0
count_vol_up_statelst_down = 0
count_vol_down_statelst_up = 0
count_vol_down_statelst_down =0
for i in range(len(statelst)):
  if vol_up_down[i] == 1 and statelst[i] == 1:
    count_vol_statelst_up += 1
  elif vol_up_down[i] == 1 and statelst[i] == 0:
    count_vol_up_statelst_down+=1
  elif vol_up_down[i] == 0 and statelst[i] == 1:
    count_vol_down_statelst_up += 1
  else:
    count_vol_down_statelst_down += 1

P_v_up_statelst_up = count_vol_statelst_up/len(statelst)
P_v_up_statelst_down = count_vol_up_statelst_down/len(statelst)
P_v_down_statelst_up = count_vol_down_statelst_up/len(statelst)
P_v_down_statelst_down = count_vol_down_statelst_down/len(statelst)

def bayes_prediction(n):
  if n == 1:
    P_yes = P_v_up_statelst_up*P_up
    P_no = P_v_up_statelst_down *P_down
    P = P_yes/(P_yes + P_no)
    return P
  elif n == 0:
    P_yes = P_v_down_statelst_up * P_up
    P_no =  P_v_down_statelst_down *P_down
    P = P_yes / (P_yes+P_no)
    return 1 - P

vol_random= []
for i in range(len(statelst)):
  temp = random.randint(0,1)
  vol_random.append(temp)

predict = []
for i in vol_random:
  if bayes_prediction(i) > 0.5:
    predict.append(1)
  else:
    predict.append(0)

# đánh giá bằng độ đo
y_true = []
y_pred = []
for i in statelst:
  y_true.append(i)

for j in predict:
  y_pred.append(j)

acc_result = accuracy_score(y_true, y_pred)
matrix_result = confusion_matrix(y_true, y_pred)
f1_score(y_true, y_pred, average='weighted')