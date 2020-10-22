import threading
import os
import time

file_path = "D:\Yeat3_Ser1\BigData\KT_Giuaky\ex1"

def run_files(file_path):
    os.system('python ' + file_path)

try:
	t = time.time()
	t1 = threading.Thread(target=run_files, args=(file_path + '/apriori_2.py',))
	t2 = threading.Thread(target=run_files, args=(file_path + '/fbgrowth_2.py',))
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	print ("\n************* Done Apriori and FB-Growth in:", time.time()- t, "*************")
except:
	print ("Error")