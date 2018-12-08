import numpy as np
from math import *
import random
import copy

class TSP_SA:
	'''
	要求输入：
	初始温度：T
	温度衰减速率：delta_t
	每个温度下接受率：R
	算法终止条件：t_k<e;迭代次数K;函数值无变化;接受概率控制
	fitness=sum(sqrt((x1-x2)**2+(y1-y2)**2))
	城市个数:n
	城市坐标：x,y
	编码原则：字符串排序"abcdefghij"和"abcdedfghijklmnopqrst",其中"a":1,"b":2...
	'''
	def __init__(self):
		self.T=None
		self.delta_t=None
		#self.R=None
		self.e=None
		self.n=None
		self.dict_char_number={'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,
							'g':6,'h':7,'i':8,'j':9,'k':10,'l':11,
							'm':12,'n':13,'o':14,'p':15,'q':16,'r':17,'s':18,'t':19}
		self.distance_mat=None
	
	def input_info(self,T,delta_t,e,n,x,y):
		self.T=T
		self.delta_t=delta_t
		#self.R=R
		self.e=e
		self.n=n
		self.distance_mat=np.zeros([n,n])
		for i in range(n):
			for j in range(n):
				self.distance_mat[i][j]=sqrt((x[i]-x[j])**2+(y[i]-y[j])**2)
	
	def __inite(self):
		if self.n==10:
			original_x="bcdefghij"
		else:
			original_x="bcdefghijklmnopqrst"
		x=list(original_x)
		random.shuffle(x)
		x.append('a')
		x.insert(0,'a')
		x=''.join(x)
		return(x)
		
	def __cal_fitness(self,x):
		temp_distance=0
		for i in range(len(x)-1):
			m=self.dict_char_number[x[i]]
			n=self.dict_char_number[x[i+1]]
			temp_distance+=self.distance_mat[m][n]
		str_x=''.join(x)
		fitness=temp_distance
		return(fitness,str_x)
		
	def __choose_field_solution(self,str_x):
		x_list=list(str_x)
		x_list.pop(0);x_list.pop(-1)
		if self.n==10:
			while True:
				r1=random.randint(0,8)
				r2=random.randint(0,8)
				if r1==r2:
					continue
				else:
					break
		else:
			while True:
				r1=random.randint(0,18)
				r2=random.randint(0,18)
				if r1==r2:
					continue
				else:
					break
		new_x_list=copy.copy(x_list)
		'''
		new_x_list[r1]=x_list[r2]
		new_x_list[r2]=x_list[r1]
		'''
		l=min(r1,r2);h=max(r1,r2)
		temp=[]
		for i in range(l,h+1):
			temp.append(x_list[i])
		temp=temp[::-1]
		for i in range(l,h+1):
			new_x_list[i]=temp[i-l]
		
		new_x_list.append('a')
		new_x_list.insert(0,'a')
		return(new_x_list)
		
	def main(self):
		xi=self.__inite()
		fitness_xi=self.__cal_fitness(xi)
		tk=self.T
		temp_best=[1000,'abcdefjhiga']
		while True:
			#print(tk)
			if tk<self.e:
				break
			else:
				'''
				r=0
				n=1
				while True:
					#print(r/n)
					if (r/n)>self.R or (r/n)==self.R:
						break
					else:
						xj=self.__choose_field_solution(xi)
						n+=1
						fitness_xj=self.__cal_fitness(xj)
						if fitness_xj[0]<fitness_xi[0]:
							xi=''.join(xj)
							fitness_xi=fitness_xj
							r+=1
						else:
							P=exp(-(fitness_xj[0]-fitness_xi[0])/tk)
							rand=random.uniform(0,1)
							if P>rand:
								xi=''.join(xj)
								fitness_xi=fitness_xj
								r+=1
					'''
				for i in range(self.n*20):
					xj=self.__choose_field_solution(xi)
					fitness_xj=self.__cal_fitness(xj)
					#print(fitness_xi[0],fitness_xj[0])
					if fitness_xj[0]<fitness_xi[0]:
							xi=''.join(xj)
							fitness_xi=fitness_xj
					else:
						P=exp(-(fitness_xj[0]-fitness_xi[0])/tk)
						rand=random.uniform(0,1)
						#print(fitness_xj[0],fitness_xi[0])
						#print(P,rand)
						if P<rand:
							xi=''.join(xj)
							fitness_xi=fitness_xj
					#print(fitness_xi[0],fitness_xj[0])
				if fitness_xi[0]<temp_best[0]:
					temp_best[0]=fitness_xi[0]
					temp_best[1]=fitness_xi[1]
				#print(temp_best)
				tk=tk*self.delta_t
		print(temp_best[0],temp_best[1])
		return(temp_best[0],temp_best[1])
		
x1=[0.4000,0.2439,0.1707,0.2293,0.5171,0.8732,0.6878,0.8488,0.6683,0.6195]
y1=[0.4439,0.1463,0.2293,0.7610,0.9414,0.6536,0.5219,0.3609,0.2536,0.2634]
x2=[5.294,4.286,4.719,4.185,0.915,4.771,1.524,3.447,3.718,2.649,4.399,4.660,
	1.232,5.036,2.710,1.072,5.855,0.194,1.762,2.682]
y2=[1.558,3.662,2.774,2.230,3.821,6.041,2.871,2.111,3.665,2.556,1.194,2.949,
	6.440,0.244,3.140,3.454,6.203,1.862,2.693,6.097]		
road_number={}
for i in range(500):
	test=TSP_SA()
	#test.input_info(500,0.99,0.5,1,10,x2,y2)
	test.input_info(1000,0.99,1,20,x2,y2)
	road=test.main()
	if road[1] in road_number:
		road_number[road[1]]+=1
	else:
		road_number[road[1]]=0
		road_number[road[1]]+=1
sort=sorted(road_number.items(),key=lambda x:x[1],reverse=True)
#print(road_number)
merge={}
for i in sort:
	merge[i[0]]=i[1]
temp=copy.copy(merge)
temp_keys=list(temp.keys())
i=0
while True:
	if temp_keys==[]:
		break
	item=sort[i][0]
	i+=1
	print(item)
	if item[::-1] in temp_keys:
		merge[item]+=merge[item[::-1]]
		temp_keys.remove(item)
		temp_keys.remove(item[::-1])
	else :
		if item in temp_keys:
			temp_keys.remove(item)
print(merge)
'''
[('ankdhjosgrpemtfqiblca', 390), ('aclbiqftmeprgsojhdkna', 81), 
('ankdhjosgrpemtfqbilca', 13), ('ankhjosgrpemtfqiblcda', 11), 
('aclibqftmeprgsojhdkna', 2), ('ankdhojsgrpemtfqiblca', 2), ('adclbiqftmeprgsojhkna', 1)]		
'''
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
