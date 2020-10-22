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

# ------------- FB-Growth --------------
class FBNode(object):
    
    def __init__(self, value, count, parent):

        self.value = value
        self.count = count
        self.parent = parent
        self.link = None
        self.children = []

    def get_child(self, value):
        # trả về node con với giá trị cụ thể
        for node in self.children:
            if node.value == value:
                return node
        return None

    def add_child(self, value):
        # thêm child node mới
        child = FBNode(value, 1, self)
        self.children.append(child)
        return child 

class FBTree(object):
    def __init__(self, transactions, threshold, root_value, root_count):
        # tạo cây

        self.frequent = self.find_frequent_items(transactions, threshold)
        self.headers = self.build_header_table(self.frequent)
        self.root = self.build_fbtree(transactions, root_value, root_count, self.frequent, self.headers)
    
    def find_frequent_items(self, transactions, threshold):
        # trả về một dict với độ phổ biến lớn hơn threshold
        items = {}
        
        for transaction in transactions:
            for item in transaction:
                if not item in items:
                    items[item] = 1
                else:
                    items[item] += 1
        for key in list(items.keys()):
            if items[key] < threshold:
                del items[key]

        return items

    def build_header_table(self, frequent):
        headers = {}

        for key in frequent.keys():
            headers[key] = None

        return headers

    def build_fbtree(self, transactions, root_value, root_count, frequent, headers):

        root = FBNode(root_value, root_count, None)

        for transaction in transactions:
            sorted_items = [x for x in transaction if x in frequent] # loại cái hạng mục bé hơn threshold ra trong transaction
            sorted_items.sort(key=lambda x: frequent[x], reverse = True) # sắp xếp giảm dần theo giá trị của frequent
            if len(sorted_items) > 0:
                self.insert_tree(sorted_items, root, headers)
        return root
    
    def insert_tree(self, items, node, headers):
        # đệ quy cây FB
        first = items[0]
        child = node.get_child(first)
        if child is not None:
            child.count += 1
        else:
            # thêm child
            child = node.add_child(first)

            # Link tới headers
            if headers[first] is None: # tạo nhánh mới
                headers[first] = child
            else: #tạo nhánh mới
                current = headers[first]
                while current.link is not None:
                    current = current.link
                current.link = child
        # đệ quy
        remain_items = items[1:]
        if len(remain_items) > 0:
            self.insert_tree(remain_items, child, headers)

    def tree_has_single_path(self, node):
        # True nếu chỉ có 1 đường đi duy nhất (single path) | cây không có lá

        num_children = len(node.children)
        if num_children > 1:
            return False
        elif num_children == 0: 
            return True
        else: # TH có 1 node con
            return True and self.tree_has_single_path(node.children[0])

    def generate_pattern_list(self):
        # tạo list của các tổ hợp và support count
        patterns = {}
        items = self.frequent.keys() # các hạng mục

        if self.root.value is None:
            suffix_value = []
        else:
            suffix_value = [self.root.value]
            patterns[tuple(suffix_value)] = self.root.count

        for i in range(1, len(items) + 1):
            for subset in itertools.combinations(items, i):
                pattern = tuple(sorted(list(subset) + suffix_value))
                patterns[pattern] = min([self.frequent[x] for x in subset])
                
        return patterns

    def zip_patterns(self, patterns):
        # gán thêm hậu tố vào patterns nếu đang ở conditional FB tree

        suffix = self.root.value

        if suffix is not None:
            # đang ở conditional FB tree
            new_patterns = {}
            for key in patterns.keys():
                new_patterns[tuple(sorted(list(key) + [suffix]))] = patterns[key]
            
            return new_patterns

        return patterns

    def mine_sub_trees(self, threshold):
        # tạo cây con và khai thắc để lấy tổ hợp

        patterns = {}
        mining_order = sorted(self.frequent.keys(), key=lambda x: self.frequent[x])

        #lấy hạng mục trong cây và đảo ngược thứ tự duyệt
        for item in mining_order:
            suffixes = []
            conditional_tree_input = []
            node = self.headers[item]

            #duyệt cái link của node để lấy list của số lần xuất hiện của item
            while node is not None:
                suffixes.append(node)
                node = node.link

            #với mỗi item, duyệt ngược về lại root
            for suffix in suffixes:
                frequency = suffix.count
                path = []
                parent = suffix.parent

                while parent.parent is not None:
                    path.append(parent.value)
                    parent = parent.parent

                for i in range(frequency):
                    conditional_tree_input.append(path)

            # đã tạo được input của subtree, khởi tạo và lấy patterns
            subtree = FBTree(conditional_tree_input, threshold, item, self.frequent[item])
            subtree_patterns = subtree.mine_patterns(threshold)

            #thêm pattern của subtree vào pattern chính
            for pattern in subtree_patterns.keys():
                if pattern in patterns:
                    patterns[pattern] += subtree_patterns[pattern]
                else:
                    patterns[pattern] = subtree_patterns[pattern]

        return patterns


    def mine_patterns(self, threshold):
        if self.tree_has_single_path(self.root):
            return self.generate_pattern_list()
        else:
            return self.zip_patterns(self.mine_sub_trees(threshold))

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

def find_frequent_patterns(transactions, support_threshold):
    tree = FBTree(transactions, support_threshold, None, None)
    return tree.mine_patterns(support_threshold)

# ----------- RUN ----------------

table = find_item_set2(crawl_values)

transactions = []

for i in range(len(table)):
    transactions.append(table['Items'][i])

min_support = 0.2 * len(transactions)
min_confidence = 0.5

support_list = find_frequent_patterns(transactions, min_support)
print("\n======== Suport List FB-Growth: ========\n", support_list)
rules = FBTree.generate_association_rules(support_list, min_confidence)
print("======== Association rules FB-Growth: ========\n", rules, end = "\n ======== FB-Growth Done ========")