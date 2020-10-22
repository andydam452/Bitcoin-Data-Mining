import csv
import pandas
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

file_path = "D:\Yeat3_Ser1\BigData\KT_Giuaky\ex1"

crawl_values = pandas.read_csv(file_path + "\crawl_result.csv")
excel_values={
    'Values': ['open','high','low','close','volume','market_cap'],
    'Max': [],
    'Min':[],
    'Average' : []
}

# parse string into number
for i in crawl_values.columns:
    if (i != 'Date'):
        for j in range (len(crawl_values[i])):
            crawl_values[i][j] = float(locale.atof(crawl_values[i][j]))

#export to excel file
def export_excel(excel_values):
    for i in crawl_values.columns:
        if(i != 'Date'):
            Max = crawl_values[[i]].sort_values(by=[i], ascending=False).iloc[0]
            Min = crawl_values[[i]].sort_values(by=[i], ascending=True).iloc[0]
            Ave = crawl_values[[i]].mean()

            excel_values['Max'].append(Max[0])
            excel_values['Min'].append(Min[0])
            excel_values['Average'].append(Ave[0])

    ex_table = pandas.DataFrame(excel_values,columns=['Values','Max','Min','Average'])
    ex_table.to_excel(file_path + "/analyse_data_1.3.xlsx",index = False)
    
    
export_excel(excel_values)