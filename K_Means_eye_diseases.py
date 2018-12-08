import xlrd
import math
import random

dataCDR_glaucoma=xlrd.open_workbook('C:/Users/Administrator/Desktop/dataCDR青光眼-45.xlsx')
dataCDR_normal=xlrd.open_workbook('C:/Users/Administrator/Desktop/dataCDR正常眼-53.xlsx')
dataOCT_glaucoma=xlrd.open_workbook('C:/Users/Administrator/Desktop/dataOCT青光眼-45.xlsx')
dataOCT_normal=xlrd.open_workbook('C:/Users/Administrator/Desktop/dataOCT正常眼-53.xlsx')
tableCDR_glaucoma=dataCDR_glaucoma.sheets()[0]
tableCDR_normal=dataCDR_normal.sheets()[0]
tableOCT_glaucoma=dataOCT_glaucoma.sheets()[0]
tableOCT_normal=dataOCT_normal.sheets()[0]

def mean_and_variance(data):
	sum=0
	for ex in data:
		sum+=ex
	mean=sum/len(data)
	variance=0
	for ex in data:
		variance+=(ex-mean)**2
	variance=math.sqrt(variance)
	return (mean,variance)

def K_nearst_neighbor():
	example_CDR=random.randint(0,44)
	print(example_CDR)
	row=tableCDR_glaucoma.row_values(example_CDR)
	example_m_v=mean_and_variance(row)
	K_CDR_glaucoma=[]
	for i in range(0,example_CDR):
		row=tableCDR_glaucoma.row_values(i)
		m_v=mean_and_variance(row)
		K_CDR_glaucoma.append(m_v[0])
	for i in range(example_CDR,45):
		row=tableCDR_glaucoma.row_values(i)
		m_v=mean_and_variance(row)
		K_CDR_glaucoma.append(m_v[0])
	K_CDR_normal=[]
	for i in range(53):
		row=tableCDR_normal.row_values(i)
		m_v=mean_and_variance(row)
		K_CDR_normal.append(m_v[0])
	k1=0;k2=0
	for i in K_CDR_glaucoma:
		k1+=(example_m_v[0]-i)**2
	k1=math.sqrt(k1)/45
	for i in K_CDR_normal:
		k2+=(example_m_v[0]-i)**2
	k2=math.sqrt(k2)/53
	if k1<k2:
		return('True')
	else:
		return('False')

record=[]
temp=0
for i in range(98):
	clas=K_nearst_neighbor()
	if clas == 'True':
		temp+=1
	record.append(clas)
print(record)
print(temp/98)




















