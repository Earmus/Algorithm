from scipy import stats
from mpl_toolkits.mplot3d import Axes3D
from numpy.linalg import cholesky
import random
import numpy as np
import matplotlib.pyplot as plt

class two_classes_one_dimension_bayesian_classifier(object):
	def __init__(self,x):
		self.x=x
		self.x_type=None
		self.p_x_w1_u=-2.122619230769231
		self.p_x_w1_sigma=1.191229374999184
		self.p_x_w2_u=2.101922222222222
		self.p_x_w2_sigma=1.241030682562574
		self.p_w1=0.9
		self.p_w2=0.1
	
	def p_x_w1(self,x):
		y=stats.norm.pdf(x,self.p_x_w1_u,self.p_x_w1_sigma)
		return  y
		
	def p_x_w2(self,x):
		y=stats.norm.pdf(x,self.p_x_w2_u,self.p_x_w2_sigma)
		return y
		
	def p_w1_x(self,x):
		y=self.p_x_w1(x)*self.p_w1/(self.p_x_w1(x)*self.p_w1+self.p_x_w2(x)*self.p_w2)
		return y
		
	def p_w2_x(self,x):
		y=self.p_x_w2(x)*self.p_w2/(self.p_x_w1(x)*self.p_w1+self.p_x_w2(x)*self.p_w2)
		return y
	
	def minium_risk(self,x):
		print(x)
		r1=self.p_w2_x(x)*1
		r2=self.p_w1_x(x)*6
		if r1>r2:
			return [r2,'w2']
		else:
			return [r1,'w1']
	
	def main(self):
		print(self.x)
		mr=self.minium_risk(self.x)
		print("The minium risk is %f and it belongs %s" % (mr[0],mr[1]))
		
def generate_multiple_classes_and_high_dimension(class_num,dimension_num,):
		cn=class_num
		dn=dimension_num
		c=[]
		for i in range(cn):
			c_temp=[]
			for j in range(dn):
				temp=(random.uniform(1,6),random.uniform(1,6))#可以修改范围
				c_temp.append(temp)
			c.append(c_temp)
		print(c)

def generate_p_w(class_num):
	p_w=[]
	for i in range(class_num):
		p_w.append(random.uniform(0,1))
	print(p_w)
	
def generate_lost(class_num):
	lost=np.random.randint(1,6,(class_num,class_num))#损失的范围可以改变
	for i in range(class_num):
		lost[i][i]=0
	print(lost)

class multiple_classes_and_high_dimension_bayesian_classifier(object):
	def __init__(self,classes,p_w):
		self.classes=classes
		self.cn=len(classes)
		self.dn=len(classes[0])
		self.p_w=p_w
		print(self.cn)
		print(self.dn)
	
	def p_x_wi(self,x,i):
		for d in self.classes[i]:
			y*=stats.norm.pdf(x,d[0],d[1])
		return(y)
	
	def generate_p_x_w(self):
		pass
		
'''
#手动实现高斯分布的数据
class generate_data(object):
	def __init__(self,classes,p_w,num):
		self.classes=classes
		self.cn=len(classes)
		self.dn=len(classes[0])
		self.p_w=p_w
		self.num=num
	
	def p_x_w_and_p_w(self,x):
		y=[]
		for i in range(self.cn):
			value=1
			for j in range(self.dn):
				value*=stats.norm.pdf(x[j],self.classes[i][j][0],self.classes[i][j][1])
			value*=self.p_w[i]
			y.append(value)
		return y
	
	def data(self):
		data=[]
		label=[]
		x=np.random.uniform(-6,6,(self.num,self.dn))
		for i in range(self.num):
			y=self.p_x_w_and_p_w(x[i])
			print(y)
			#label.append(y.index(max(y)))
			label.append(0)
		#print(label)
		ax=[[],[],[]]
		ay=[[],[],[]]
		az=[[],[],[]]
		#plt.xlim(xmax=6,xmin=0)
		#plt.ylim(ymax=6,ymin=0)
		for k in range(300):
			if label[k]==0:
				ax[0].append(x[k][0])
				ay[0].append(x[k][1])
				az[0].append(100*self.p_x_w_and_p_w([x[k][0],x[k][1]])[0])
			elif label[k]==1:
				ax[1].append(x[k][0])
				ay[1].append(x[k][1])
				az[1].append(10*max(self.p_x_w_and_p_w([x[k][0],x[k][1]])))
			else:
				ax[2].append(x[k][0])
				ay[2].append(x[k][1])
				az[2].append(10*max(self.p_x_w_and_p_w([x[k][0],x[k][1]])))
		#plt.plot(ax[0],ay[0],'ro')
		#plt.plot(ax[1],ay[1],'go')
		#plt.plot(ax[2],ay[2],'bo')
		axe = plt.subplot(111, projection='3d')
		axe.scatter(ax[0], ay[0], az[0], c='y')
		#axe.scatter(ax[1], ay[1], az[1], c='r')
		#axe.scatter(ax[2], ay[2], az[2], c='g')
		plt.show()

	def main(self):
		self.data()

#generate_multiple_classes_and_high_dimension(3,2)
classes=[[(4.666081960818584, 1.2929097547794894), (1.3619599160210285, 2.4462796249953054)], [(3.2460881789629497, 5.472743578494317), (1.6405661705329875, 1.7144540944086886)], [(4.212354523982159, 5.13956797214046), (5.976387741497341, 5.2585905539059645)]]
#generate_p_w(3)
p_x=[0.3434952049347802, 0.5539628494897179, 0.8676048420172261]
#generate_lost(3)
lost=[[0,3,5],[3,0,2],[1,5,0]]
data=generate_data(classes,p_x,300)
data.main()
'''

#python自带函数库生成高斯分布的数据
sampleNo=1000
mu= np.array([[1,5]])
Sigma=np.array([[1,0.5],[1.5,3]])
R=cholesky(Sigma)
s=np.dot(np.random.randn(sampleNo,2),R)
plt.subplot(144)
plt.plot(s[:,0],s[:,1],'+')
plt.show()

'''
B=two_classes_one_dimension_bayesian_classifier(1)
B.main()
'''










































