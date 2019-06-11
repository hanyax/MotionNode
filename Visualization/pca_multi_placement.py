import numpy as np
import code
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

import random
import re
colors_list = ['blue', 'red', 'green', 'purple', 'magenta', 'orange', 'black']



def filetering(input):
	return re.sub("[^\d\.]", "", input)

def load_6dim_data(DATAPATH):
	outdata = []
	f  = open(DATAPATH, 'r')
	data =  f.readlines()

	for line in data:
		print(line.find('H')>-1)
		print(line.find('R')>-1)
		print(line.find('P')>-1)
		print(line.find('aX')>-1)
		print(line.find('aY')>-1)
		print(line.find('aZ')>-1)

		if line.find('H')>-1 and line.find('R')>-1 and line.find('P')>-1 and line.find('aX')>-1 and line.find('aY')>-1 and line.find('aZ')>-1:
			h = filetering(line.split(' ')[2])
			r = filetering(line.split(' ')[5])
			p = filetering(line.split(' ')[8])
			xa = filetering(line.split(' ')[11])
			ya = filetering(line.split(' ')[14])
			za = filetering(line.split(' ')[17])
			outdata.append([float(h),float(r),float(p),float(xa),float(ya),float(za)])
	return outdata

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
		outdata.append([x,y,z, x,y,z])
	return outdata


def load_fack_6dim_data():
	outdata = []
	for i in range(1000):
		x1 = random.random()
		y1 = random.random()
		z1 = random.random()
		x2 = random.random()
		y2 = random.random()
		z2 = random.random()
		outdata.append([x1,y1,z1,x2,y2,z2])
	return outdata


def load_fack_6dim_data2():
	outdata = []
	for i in range(1000):
		x1 = random.random()
		outdata.append([x1,x1,x1,x1,x1,x1])
	return outdata

def load_fack_6dim_data3():
	outdata = []
	for i in range(1000):
		x1 = random.random()
		y1 = random.random()
		outdata.append([x1,x1,x1,x1,y1,y1])
	return outdata

def load_fack_6dim_data4():
	outdata = []
	for i in range(1000):
		x1 = random.random()
		y1 = random.random()
		outdata.append([x1,y1,x1,y1,x1,y1])
	return outdata

def load_fack_6dim_data5():
	outdata = []
	for i in range(1000):
		x1 = random.random()
		y1 = random.random()
		outdata.append([y1,x1,y1,x1,y1,x1])
	return outdata


def pca_process(data, data_num):
	num_placement = len(data_num)
	# print(data_num)
	# training: learn a projection matrix
	pca = PCA(n_components=2)
	# apply the projection matrix, and get 2-dim data
	newData = pca.fit_transform(data)
	fig = plt.figure()

	plt.xlabel('Principal Component 1', fontsize = 15)
	plt.ylabel('Principal Component 2', fontsize = 15)

	for p in range(num_placement):
		start_idx = np.sum(data_num[:(p+1)])-data_num[p]
		to_idx = np.sum(data_num[:(p+1)])
		label_name = 'placement %d'%(p)
		plt.scatter(newData[start_idx:to_idx,0],newData[start_idx:to_idx,1],c=colors_list[p],alpha=0.2, label=label_name)
	plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	plt.tight_layout()
	plt.grid()
	plt.savefig('pca_projection.png', dpi=300, format='png', bbox_inches='tight')
	plt.show()

def pca_process_classification(data, data_num):
	num_placement = len(data_num)
	# print(data_num)
	# training: learn a projection matrix
	pca = PCA(n_components=2)
	# apply the projection matrix, and get 2-dim data
	newData = pca.fit_transform(data)
	fig = plt.figure()

	plt.xlabel('Principal Component 1', fontsize = 15)
	plt.ylabel('Principal Component 2', fontsize = 15)
	color_id = 0
	for p in range(num_placement):
		if p <=2:
			label_name = 'Correct Posture'
			color_id = 0
		else:
			label_name = 'Incorrect Posture'
			color_id = 1
		start_idx = np.sum(data_num[:(p+1)])-data_num[p]
		to_idx = np.sum(data_num[:(p+1)])
		# label_name = 'placement %d'%(p)
		plt.scatter(newData[start_idx:to_idx,0],newData[start_idx:to_idx,1],c=colors_list[color_id],alpha=0.2, label=label_name)
	plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	plt.tight_layout()
	plt.grid()
	plt.savefig('binary_classification.png', dpi=300, format='png', bbox_inches='tight')
	plt.show()


def prediction(input, template, good_squart):

	data_dim,num_squat,max_len = template.shape
	similarity = []
	# code.interact(local=locals())
	inference = np.zeros((6,max_len))
	for i in range(len(input)):
		for j in range(6):
			inference[j][i] = input[i][j]
	predicted_result = False
	for k in range(num_squat):
		error = 0
		if good_squart[k]==True:
			for i in range(max_len):
				for j in range(6):
					error += np.abs(inference[j][i] - template[j][k][i])/6
			# print(error)
			score = 1.0/(error+0.01)
			similarity.append(score)
			if score>50:
				predicted_result=True
	print(similarity)
	print('Good posture? %s'%(predicted_result))

def load_good_data(data):
	h = []
	r = []
	p = []
	xa = []
	ya = []
	za = []
	gradient = []
	for item in data:
		h.append(item[0])
		r.append(item[1])
		p.append(item[2])
		xa.append(item[3])
		ya.append(item[4])
		za.append(item[5])
	
	for i in range(len(h)-1):
		gradient.append(h[i+1]-h[i])

	index = [ n for n,i in enumerate(gradient) if i>300 ]
	num_squat = len(index)-1
	max_len = 0
	for i in range(num_squat):
		if (index[i+1]-index[i])>max_len:
			max_len = index[i+1]-index[i]

	template = np.zeros((6,num_squat,max_len))
	good_squat = []
	for i in range(6):
		temp = []
		if i ==0:
			temp = h
		if i ==1:
			temp = r
		if i ==2:
			temp = p
		if i ==3:
			temp = xa
		if i ==4:
			temp = ya
		if i ==5:
			temp = za

		for j in range(num_squat):
			squat_len = index[j+1]-index[j]
			template[i,j,0:index[j+1]-index[j]] = temp[index[j]:index[j+1]]
			if squat_len>100:
				good_squat.append(True)
			else:
				good_squat.append(False)
	'''
	fig = plt.figure(figsize=(10,10))
	for i in range(num_squat):
		if good_squat[i]==True:
			testdata = template[-1,i,:]
			plt.plot(testdata)

	plt.show()
	'''
	print(index)
	return template, good_squat

def time_plot(data,fname):
	fig = plt.figure(figsize=(10,10))

	plt.subplot(6,1,1)
	plt.tick_params(labelsize=5)
	plt.xlabel('Time', fontsize = 14)
	plt.ylabel('H', fontsize = 14)
	h = []
	for item in data:
		h.append(item[0])
	plt.plot(h)
	plt.grid()

	plt.subplot(6,1,2)
	plt.tick_params(labelsize=5)
	plt.xlabel('Time', fontsize = 14)
	plt.ylabel('R', fontsize = 14)
	r = []
	for item in data:
		r.append(item[1])
	plt.plot(r)
	plt.grid()

	plt.subplot(6,1,3)
	plt.tick_params(labelsize=5)
	plt.xlabel('Time', fontsize = 14)
	plt.ylabel('P', fontsize = 14)
	p = []
	for item in data:
		p.append(item[2])
	plt.plot(p)
	plt.grid()

	plt.subplot(6,1,4)
	plt.tick_params(labelsize=5)
	plt.xlabel('Time', fontsize = 14)
	plt.ylabel('Xa', fontsize = 14)
	xa = []
	for item in data:
		xa.append(item[3])
	plt.plot(xa)
	plt.grid()

	plt.subplot(6,1,5)
	plt.tick_params(labelsize=5)
	plt.xlabel('Time', fontsize = 14)
	plt.ylabel('Ya', fontsize = 14)
	ya = []
	for item in data:
		ya.append(item[4])
	plt.plot(ya)
	plt.grid()

	plt.subplot(6,1,6)
	plt.tick_params(labelsize=5)
	plt.xlabel('Time', fontsize = 14)
	plt.ylabel('Za', fontsize = 14)
	za = []
	for item in data:
		za.append(item[5])
	plt.plot(za)
	plt.grid()
	plt.subplots_adjust(wspace=1, hspace=1)
	plt.savefig(fname, dpi=300, format='png', bbox_inches='tight')
	# plt.show()

def main():
	# load data
	datapath = '../Data_output_txt_MotionShield/output_to_txt/test_data.txt'
	data1 = load_6dim_data('../Data_output_txt_MotionShield/output_to_txt/MultipleSquatData.txt')
	data2 = load_6dim_data('../Data_output_txt_MotionShield/output_to_txt/MultipleSquatData.txt')
	#data2 = load_6dim_data('../Data_output_txt_MotionShield/output_to_txt/lowerleg_p1_correct_data2.txt')
	#data3 = load_6dim_data('../Data_output_txt_MotionShield/output_to_txt/lowerleg_p1_correct_data3.txt')
	#data4 = load_6dim_data('../Data_output_txt_MotionShield/output_to_txt/lowerleg_p1_wrong_data1.txt')
	#data5 = load_6dim_data('../Data_output_txt_MotionShield/output_to_txt/lowerleg_p1_wrong_data2.txt')
	#data6 = load_6dim_data('../Data_output_txt_MotionShield/output_to_txt/lowerleg_p1_wrong_data3.txt')
	# data4 = load_fack_6dim_data3()
	# data5 = load_fack_6dim_data4()
	# concatenate all data from different placements

	template, good_squart = load_good_data(data1)
	prediction(data2[66:187], template, good_squart)

	# time_plot(data1, 'muliply_squat.png')
	#time_plot(data2, 'text_data2.png')
	#time_plot(data3, 'text_data3.png')
	#time_plot(data4, 'text_data4.png')
	#time_plot(data5, 'text_data5.png')
	#time_plot(data6, 'text_data6.png')
	#concatenated_data = np.concatenate((data1 ,data2, data3, data4, data5, data6))
	#data_num = [len(data1), len(data2), len(data3), len(data4), len(data5), len(data6)]
    # run pca
	#pca_process(concatenated_data, data_num)

if __name__ == '__main__':
    main()
