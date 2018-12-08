import math
import random as rand


class GA:
    """
    要求输入
    population_size:种群大小
    accuracy:精度
    generation_size:迭代次数
    cross_rate:交叉概率
    mutate_rate:变异概率
    upper_bound:上限
    lower_bound:下限
    elitism:精英选择
    fitness:y=x+10sin(5x)+7cos(4x),x∈[0,9]
    """

    def __init__(self):
        self.chromosome_size = None  # 染色体长度
        self.m = None  # 输出最佳个体
        self.n = None  # 最佳适应度
        self.p = None  # 最佳个体出现的迭代次数
        self.q = None  # 最佳个体自变量值
        self.G = 0  # 当前迭代次数
        self.fitness_value = {}  # 当前适应度字典
        self.father = {}  # 选择的父代
        self. fitness_sum = None  # 当代适应度总和
        self.best_fitness = None  # 历代最佳适应度值
        self.best_individual = None  # 历代最佳适应个体
        self.fitness_average = []  # 历代平均适应值矩阵
        self.best_generation = None  # 最佳代

    def input_info(self, population_size=0, accuracy=0, generation_size=0,
                   cross_rate=0, mutate_rate=0, elitism=False,
                   upper_bound=0, lower_bound=0):
        self.population_size = population_size
        self.accuracy = accuracy
        self.generation_size = generation_size
        self.cross_rate = cross_rate
        self.mutate_rate = mutate_rate
        self.elitism = elitism
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound

    def fitness(self, x):
        y = round(x+10*math.sin(5*x)+7*math.cos(4*x), 6)
        y = 1/(1+math.e**(-y))  # Logistic
        return y

    def fun(self, x):
        y = round(x+10*math.sin(5*x)+7*math.cos(4*x), 6)
        return y

    def get_chromosome_size(self):
        i = 1
        piece = (self.upper_bound-self.lower_bound)*(10**self.accuracy)
        while True:
            temp = 2**i-piece
            if temp >= 0:
                self.chromosome_size = i
                break
            i += 1

    def numeric_decode(self, x):
        x = round(self.lower_bound+int(x, 2)*(self.upper_bound -
                  self.lower_bound)/(2**self.chromosome_size-1), self.accuracy)
        return x

    def inite(self):
        for i in range(self.population_size):
            temp = ""
            for j in range(self.chromosome_size):
                x = rand.randint(0, 1)
                temp += str(x)
            self.fitness_value[temp] = None

    def get_fitness_value(self):
        fitness_value_keys = list(self.fitness_value.keys())
        for i in range(self.population_size):
            temp = self.numeric_decode(fitness_value_keys[i])
            temp = self.fitness(temp)
            self.fitness_value[fitness_value_keys[i]] = temp

    def sorted_fitness_value(self):
        temp = sorted(self.fitness_value.items(),
                      key=lambda item: item[1], reverse=True)
        self.best_fitness = temp[0][1]
        self.best_individual = self.numeric_decode(temp[0][0])
        self.fitness_value = dict(temp)
        self.fitness_sum = sum(self.fitness_value.values())

    def selection(self):
        roulette_P = {}
        for individual in self.fitness_value:
            roulette_P[individual] = self.fitness_value[individual] /\
                                     self.fitness_sum
        cumulative_probability = []
        temp = 0
        for individual in roulette_P:
            temp = round(roulette_P[individual]+temp, 6)
            cumulative_probability.append(temp)
        for i in range(self.population_size):
            r = round(rand.random(), 6)
            for j in range(self.population_size):
                if (r > cumulative_probability[j]) and\
                   (r < cumulative_probability[j+1]):
                    self.father[i] = list(self.fitness_value.keys())[j]
                    break
                elif (r > 0) and (r < cumulative_probability[0]):
                    self.father[i] = list(self.fitness_value.keys())[0]
                    break

    def hybridization_and_variation(self):
        hybridization = {}
        for i in range(self.population_size):
            r = round(rand.random(), 6)
            if r < self.cross_rate:
                hybridization[i] = self.father[i]
        while True:
            if (len(hybridization) % 2) == 0:
                break
            else:
                while True:
                    r = rand.randint(0, self.population_size-1)
                    if r not in hybridization.keys():
                        break
                hybridization[r] = self.father[r]
                break
        temp_hy_values = list(hybridization.values())
        temp_hy_keys = list(hybridization.keys())
        num = int(len(hybridization)/2)
        for i in range(num):
            r = rand.randint(1, self.chromosome_size-1)
            list_hy_values1 = list(temp_hy_values[i])
            list_hy_values2 = list(temp_hy_values[i+num])
            for x in range(r, self.chromosome_size+1):
                temp = list_hy_values1[x-1]
                list_hy_values1[x-1] = list_hy_values2[x-1]
                list_hy_values2[x-1] = temp
            temp_hy_values[i] = "".join(list_hy_values1)
            temp_hy_values[i+num] = "".join(list_hy_values2)

        for i in range(2*num):
            self.father[temp_hy_keys[i]] = temp_hy_values[i]

        for i in range(self.population_size):
            temp = list(self.father[i])
            for j in range(self.chromosome_size):
                r = round(rand.random(), 6)
                if r < self.mutate_rate:
                    if temp[j] == '0':
                        temp[j] = '1'
                        self.father[i] = "".join(temp)
                    else:
                        temp[j] = '0'
                        self.father[i] = "".join(temp)
        self.fitness_value = {}
        for i in range(self.population_size):
            self.fitness_value[self.father[i]] = None
        while True:
            if len(self.fitness_value) != self.population_size:
                temp = ""
                for j in range(self.chromosome_size):
                    x = rand.randint(0, 1)
                    temp += str(x)
                self.fitness_value[temp] = None
            else:
                break

    def main(self):
        self.get_chromosome_size()
        self.inite()
        best_ans = float('-Inf')
        x = None
        while True:
            if self.G < self.generation_size:
                self.get_fitness_value()
                print("This is the %d times:" % self.G)
                self.sorted_fitness_value()
                self.selection()
                self.hybridization_and_variation()
                self.G += 1
                print(self.best_individual)
                y = self.fun(self.best_individual)
                print(y)
                print(self.fitness_sum)
                if y > best_ans:
                    best_ans = y
                    x = self.best_individual
            else:
                print(x, best_ans)
                break


'''
ga = GA()
ga.input_info(20, 4, 10, 0.6, 0.02, False, 9, 0)
ga.main()
'''
