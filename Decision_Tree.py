import math
import xlrd
data=xlrd.open_workbook('C:/Users/Administrator/Desktop/Absenteeism_at_work.xls')
table=data.sheets()[0]
types=table.row_values(0)
types.pop(-1)
attributes={}
index=0
for temp in types:
	attributes[temp]=table.col_values(index)[1:]
	index+=1
#Stage 1
def attribute_entroy(attri_data):
	pi={}
	for temp in attri_data:
		if temp in pi:
			pi[temp]+=1
		else:
			pi[temp]=1
	number=len(attri_data)
	for key in pi:
		pi[key]=pi[key]/number
	entropy=0
	for key in pi:
		entropy+=-pi[key]*math.log(pi[key],2)
	m=len(pi)
	return (m,entropy)
Entry=[]
for name in attributes:
	temp=attribute_entroy(attributes[name])
	new=(temp[0],temp[1],name)
	Entry.append(new)
E=[]
for temp in Entry:
	E.append(temp[1])
most_infromative_attribute=max(E)
print(Entry
print(most_infromative_attribute)
for temp in Entry:
	if most_infromative_attribute in temp:
		print(temp[2])

def create_decision_tree():
	tree={}
	tree['root']='Work load Average/day'
