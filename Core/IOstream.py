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
import csv, sys
import matplotlib.pyplot as plt

def load_csv(file_name):
	#print file_name
	G = nx.Graph()
	with open (file_name,'rb') as file:
		reader = csv.reader(file)
		#G = nx.read_edgelist(file, delimiter=',')
		for row in reader:
			G.add_edge(int(row[0]),int(row[1]))
			G.add_edge(int(row[1]),int(row[0]))
	print ("--------------- loading graph Finish ---------------")
	return G
	
def load_txt(file_name):
	#print file_name
	with open (file_name,'rb') as file:
		G = nx.Graph()
		G = nx.read_edgelist(file, nodetype=int)

	print ("--------------- loading graph Finish ---------------") 
	return G

def OutputNode(group):
	for i in range(len(group)):
		print ('node_%s: %s') %(i, group[i])


def showGraph(graph):
	nx.draw_networkx(graph)
	#nx.draw_random(graph)
	#nx.draw_circular(graph)
	#nx.draw_spectral(graph)
	plt.show()

def normalizeGraph(readfile_name, norfile_name):
	#nFile = open (norfile_name, 'w')
	rFile = open (readfile_name, 'rb')
	nodeMap = {}
	
	
	