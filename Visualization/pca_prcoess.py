import numpy as np
import code
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt



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

def pca_process(data):
	# training: learn a projection matrix
	pca = PCA(n_components=2)

	# apply the projection matrix, and get 2-dim data
	newData = pca.fit_transform(data)

	fig = plt.figure(figsize = (8,8))
	plt.xlabel('Principal Component 1', fontsize = 15)
	plt.ylabel('Principal Component 2', fontsize = 15)
	plt.scatter(newData[:,0],newData[:,1])
	plt.grid()
	plt.show()


def main():
	DATAPATH = 'data.txt'
	data = load_data(DATAPATH)
	pca_process(data)

if __name__ == '__main__':
    main()