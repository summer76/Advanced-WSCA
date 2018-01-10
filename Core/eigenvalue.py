# encoding: utf-8
#!/usr/bin/python

"""
@author: Tzy-Shiah Wang (tzuchia0706@gmail.com)
@date 2017
@copyright GNU Public License
@cond GNU_PUBLIC_LICENSE
    AWSCA are free softwares: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    AWSCA are distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

"""

import networkx as nx
try:
	import numpy as np
	
except ImportError:
	raise ImportError("numpy can not be imported.")

try:
	import scipy as sp
except ImportError:
	raise ImportError("scipy can not be imported.")

def cal2Eigenvalue(topology):
	if type(topology) != nx.Graph :
		raise TypeError("Can't caculate eigenvalue, use only non directed graph")
	L = nx.normalized_laplacian_matrix(topology)
	e = np.linalg.eigvals(L.A)
	return e[1]

def calCriticalValue(topology):
	if type(topology) != nx.Graph :
		raise TypeError("Can't caculate critical value, use only non directed graph")
	L = nx.normalized_laplacian_matrix(topology)
	e = np.linalg.eigvals(L.A)
	return e[1]
	
def cal2dWSDValue(a1, a2, b1, b2):
	M = np.array([[a1, a2],[b1, b2]])
	D = [[1/((a1+a2)**(0.5)), 0],[0, 1/((b1+b2)**(0.5))]]
	I = [[1, 0], [0, 1]]
	L = I - np.dot(np.dot(D, M), D)
	e = np.linalg.eigvals(L)
	wsd = (1-e[0])**3+(1-e[1])**3
	return wsd
	
def calWSDValue(Mat):
	D = np.zeros((Mat[0].size,Mat[0].size),float)
	I = np.zeros((Mat[0].size,Mat[0].size),float)
	for i in range(Mat[0].size):
		for j in range(Mat[0].size):
			if(i == j):
				D[i][j] = 1/(rowSum(i, Mat)**(0.5))
				I[i][j] = 1
	L = I - np.dot(np.dot(D, Mat), D)
	e = np.linalg.eigvals(L)
	wsd = 0.
	for k in range(e.size):
		wsd += (1-e[k])**3
	return wsd

def rowSum(rowNum, Mat):
	sum = 0
	for i in range(Mat[rowNum].size):
		sum = sum + Mat[rowNum][i]
	return sum
