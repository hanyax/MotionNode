import numpy as np
import code
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
import random


def load_data(DATAPATH):
	f  = open(DATAPATH, 'r')
	data =  f.readlines()
	data = '\t '.join(data).replace('\n', ' ')
	data = data.split('\t')
	Xdata = []
	Ydata = []
	Zdata = []
	for line in data:
		if line.find('X')>-1:
			Xdata.append(line.split(':')[1].split(' ')[1])
		elif line.find('Y')>-1:
			Ydata.append(line.split(':')[1].split(' ')[1])
		elif line.find('Z')>-1:
			Zdata.append(line.split(':')[1].split(' ')[1])

	outdata = []
	for i in range(len(Xdata)-2):
		if len(Xdata[i])>1 and len(Ydata[i])>1 and len(Zdata[i])>1: 
			outdata.append([float(Xdata[i]),float(Ydata[i]),float(Zdata[i])])	

	return outdata


def load_fack_data():
	outdata = []
	for i in range(1000):
		x = random.random()
		y = random.random()
		z = random.random()
		outdata.append([x,y,z])
	return outdata


def load_fack_9dim_data():
	outdata = []
	for i in range(1000):
		x1 = random.random()
		y1 = random.random()
		z1 = random.random()
		x2 = random.random()
		y2 = random.random()
		z2 = random.random()
		x3 = random.random()
		y3 = random.random()
		z3 = random.random()
		outdata.append([x1,y1,z1,x2,y2,z2,x3,y3,z3])
	return outdata


def load_fack_9dim_data2():
	outdata = []
	for i in range(1000):
		x1 = random.random()
		outdata.append([x1,x1,x1,x1,x1,x1,x1,x1,x1])
	return outdata


def pca_process(data1, data2):
	label1 = np.zeros(len(data1))
	label2 = np.ones(len(data2))
	# concatenate data

	concatenated_data = np.concatenate((data1 ,data2))
	concatenated_label = np.concatenate((label1 ,label2))

	# training: learn a projection matrix
	pca = PCA(n_components=2)

	# apply the projection matrix, and get 2-dim data
	newData = pca.fit_transform(concatenated_data)
	print(newData.shape)
	fig = plt.figure()
	plt.xlabel('Principal Component 1', fontsize = 15)
	plt.ylabel('Principal Component 2', fontsize = 15)
	plt.scatter(newData[0:len(data1),0],newData[0:len(data1),1],c='red',alpha=0.2)
	plt.scatter(newData[len(data1):len(data1)+len(data2),0],newData[len(data1):len(data1)+len(data2),1],c='green',alpha=0.2)
	
	plt.grid()
	plt.show()



def main():
	# DATAPATH = 'data.txt'
	# data = load_data(DATAPATH)
	# data2 = load_fack_data()

	data1 = load_fack_9dim_data()
	data2 = load_fack_9dim_data2()

	pca_process(data1, data2)

if __name__ == '__main__':
    main()