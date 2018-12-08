import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
'''
x1=np.linspace(-7,3,1000)
y1=stats.norm.pdf(x1,-2.122619230769231,1.191229374999184)
x2=np.linspace(-3,7,1000)
y2=stats.norm.pdf(x2,2.101922222222222,1.241030682562574)
plt.plot(x1,y1)
plt.plot(x2,y2,color='red')
plt.text(-6, 0.25, r'$p(X|w1)$',color='blue')
plt.text(4, 0.25, r'$p(X|w2)$',color='red')
plt.xlabel("x")
plt.show()
'''
x1=np.linspace(-7,7,1000)
x2=np.linspace(-7,7,1000)
y1=6*stats.norm.pdf(x1,-2.122619230769231,1.191229374999184)*0.9/(stats.norm.pdf(x1,-2.122619230769231,1.191229374999184)*0.9+stats.norm.pdf(x2,2.101922222222222,1.241030682562574)*0.1)
y2=stats.norm.pdf(x2,2.101922222222222,1.241030682562574)*0.1/(stats.norm.pdf(x1,-2.122619230769231,1.191229374999184)*0.9+stats.norm.pdf(x2,2.101922222222222,1.241030682562574)*0.1)
plt.plot(x1,y1)
plt.plot(x2,y2,color='red')
plt.text(-4, 5.5, r'$p(a1|X)$',color='blue')
plt.text(4, 0.6, r'$p(a2|X)$',color='red')
plt.xlabel("x")
plt.show()