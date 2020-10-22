import csv
import pandas
import locale
import itertools

file_path = "D:\Yeat3_Ser1\BigData\KT_Giuaky\ex1"

def loadCSV():
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    crawl_values = pandas.read_csv(file_path + "\crawl_result.csv")

    # parse string into number
    for i in crawl_values.columns:
        if (i != 'Date'):
            for j in range (len(crawl_values[i])):
                crawl_values[i][j] = float(locale.atof(crawl_values[i][j]))
    
    return crawl_values

crawl_values = loadCSV()


# ---------------- Format data --------------- 

#so sanh 2 gia tri
def compare_values(a, b):
    return (True if a>b else False)

#so sanh gia tri cua 2 ngay ke nhau. Neu nho hon thi xoa gia tri
def standardlize_df(df):
    for i in range(len(df.columns)):
        j = df.columns[i]
        for k in range(len(df[j])):
            if(k == len(df[j])-1):
                df[j][k] = ''
                break
            elif(compare_values(df[j][k], df[j][k+1])):
                df[j][k] = j
            else: df[j][k] = ''
    return df

def find_item_set2(df):
    data = {
        'Items' : []
    }

    df = standardlize_df(df) 

    for index, row in df.iterrows():
        lst = []
        for i in row:
            if(i != 'Date' and i != ''):
                lst.append(i)
        data['Items'].append(lst)
            
    return pandas.DataFrame(data, columns=['Items']);

#------------- APRIORI ---------------

def compute_C1_and_L1_itemset(data, num_trans, min_support):
    #Tính C1 
    C1 = {}
    for transaction in data: 
        for item in transaction:
            if not item in C1:
                C1[item] = 1
            else: C1[item] +=1
    #Tính L1
    L1 = []
    support1 = {}
    for candidate, count in sorted(C1.items(), key=lambda x: x[0]):
        support = count / num_trans
        if support >= min_support:
            L1.insert(0, [candidate])
            support1[frozenset([candidate])] = count
    return list(map(frozenset, sorted(L1))), support1, C1

def compute_CK(LK_, k):
    CK = []
    for i in range(len(LK_)):
        for j in range(i+1, len(LK_)): #liệt kê tất cả tổ hợp trong LK-1 
            L1 = sorted(list(LK_[i]))[:k-2]
            L2 = sorted(list(LK_[j]))[:k-2]
            if L1 == L2: # nếu k-1 phần tử đầu giống nhau, nối 2 mảng
                new_candidate = frozenset(sorted(LK_[i] | LK_[j]))
                CK.append(new_candidate)
    return sorted(CK)

def compute_LK(D, CK, num_trans, min_support):
    support_count = {}
    for item in D:
        for candidate in CK:
            if candidate.issubset(item):
                if not candidate in support_count:
                    support_count[candidate] = 1
                else: support_count[candidate] += 1
    LK = []
    supportK = {}
    for candidate, count in sorted(support_count.items(), key=lambda x: x[0]):
        support = count / num_trans
        if support >= min_support:
            LK.append(candidate)
            supportK[candidate] = count
    return sorted(LK), supportK

def apriori(data, min_support):
    D = sorted(list(map(set, data)))
    num_trans = len(D)
    L1, support_list, CK = compute_C1_and_L1_itemset(data, num_trans, min_support)
    L = [L1]
    k = 1

    while(True): #tạo set k đến đi set thứ k-th rỗng
        #print('Running Apriori: the %i-th iteration with %i candidates...' % (k, len(CK)))
        k += 1
        CK = compute_CK(LK_=L[-1], k = k)
        LK, supportK = compute_LK(D, CK, num_trans, min_support)
        if len(CK) == 0:
            L = [sorted([tuple(sorted(list(itemset), key=lambda x: str(x))) for itemset in LK]) for LK in L]
            support_list = dict((tuple(sorted(list(k), key=lambda x: str(x))), v) for k, v in support_list.items())
            #print('Running Apriori: the %i-th iteration. Terminating ...' % (k-1))
            break
        else:
            L.append(LK)
            support_list.update(supportK)
    return L, support_list

def generate_association_rules(patterns, confidence_threshold):
        # {(left): ((right), confidence)}

        rules = {}


        for itemset in patterns.keys():
            upper_support = patterns[itemset]

            for i in range(1, len(itemset)):
                for ante in itertools.combinations(itemset, i):
                    ante = tuple(sorted(ante))
                    conse = tuple(sorted(set(itemset) - set(ante)))

                    if ante in patterns:
                        lower_support = patterns[ante]
                        confi = float(upper_support) / lower_support

                        if confi >= confidence_threshold:
                            rules[ante] = (conse, confi)
        
        return rules

# ----------- RUN ----------------
table = find_item_set2(crawl_values)

transactions = []
min_support = 0.2
min_confidence = 0.5

for i in range(len(table)):
    transactions.append(table['Items'][i])

L, support_list = apriori(transactions, min_support)
print("======== Suport List Apriori: ========\n", support_list)
rules = generate_association_rules(support_list, min_confidence)
print("======== Association rules Apriori: ========\n", rules, end = "\n ======== Apriori Done ========")