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

import os
import eigenvalue as eg
import networkx as nx
from random import randint

wsd_Threshold = 1.
	
def Clustering(topology, Group):
	if type(topology) != nx.Graph :
		raise TypeError("Bad graph type, use only non directed graph")
	number_Of_Nodes = nx.number_of_nodes(topology)
	number_Of_Groups = 0
	
	for key in range(nx.number_of_nodes(topology)):
		Group[key] = -1
	
	terminal_Flag = terminal_Judge(Group)
	while terminal_Flag is False:
		start_Node = start_Node_Select(Group, topology)
		assign_Group(start_Node, Group, number_Of_Groups)	
		pheo = {}
		initialize_Pheo(pheo, len(Group))
		pheo_Update(start_Node, pheo, topology, Group)
		remain_Pheo = pheo_Count(pheo)
		while remain_Pheo > 0:
			next_Node = next_Node_Select(pheo)
			if Node_Merge_Judge(next_Node, Group, topology, number_Of_Groups) == True:
				assign_Group(next_Node, Group, number_Of_Groups)
				pheo_Update(next_Node, pheo, topology, Group)
			pheo[next_Node] = 0
			remain_Pheo = pheo_Count(pheo)
		number_Of_Groups = number_Of_Groups + 1
		terminal_Flag = terminal_Judge(Group)
	normalize_Group(Group)
		
def terminal_Judge(group):
	"""
	Judge whether all of the nodes have been assign a group.
	return: True-> all the nodes have assigned; False->at least one node hasn't been assigned.
	"""
	disc = True
	for i in range(len(group)):
		if group[i] is -1:
			disc = False
	return disc
	
def normalize_Group(Group):
	"""
	normalize the number of each group.
	:param Group: A list of group number of each group.
	return: A list of normalized group number.
	"""
	tempG = {}
	number_Of_Group = 0
	for i in range(len(Group)):
		count = 0
		for j in range(len(Group)):
			if Group[j] == i:
				count = count + 1
				Group[j] = number_Of_Group				
		if count > 0:
			number_Of_Group = number_Of_Group +1
	print ('number_Of_Group: %d') %(number_Of_Group)

def group_Count(group):
	"""
	calculate the total number of groups.
	:param Group: A list of group number of each node.
	return: total number of groups.
	"""
	temp_Group = {}
	for m in range(len(group)):
		temp_Group[m] = 0
	for i in range(len(group)):
		temp_Group[group[i]] = 1
	count = 0
	for j in range(len(temp_Group)):
		count = count + temp_Group[j]
	return count
	
def start_Node_Select(group, topology):
	"""
	select a node to start the procedure of certain clustering.
	return: a node.
	"""
	select_Node = -1
	temp_Degree = -1
	for i in range(0, len(group)):
		if group[i] == -1 and degree_Count(i, topology) > temp_Degree:
			temp_Degree = degree_Count(i, topology)
			select_Node = i
	return select_Node

def degree_Count(Nnum, topology):
	counter = 0
	for i in range(nx.number_of_nodes(topology)):
		if topology.has_edge(Nnum, i) or topology.has_edge(i, Nnum):
			counter = counter + 1
	return counter
	
def assign_Group(Gnum, group, _number_Of_Groups):
	group[Gnum] = _number_Of_Groups
	
def initialize_Pheo(pheo, length):
	for i in range(length):
		pheo[i] = 0

def pheo_Update(Nnum, pheo, topology, group):
	"""
	update the pheo to increase the probability that the neighborhood been chosen by the next time.
	"""
	for i in range(nx.number_of_nodes(topology)):
		if group[i] == -1: 
			pheo[i] = pheo[i] + edge_Count(i, Nnum, topology)

def pheo_Count(pheo):
	"""
	caculate the total amount of pheo.
	"""
	counter = 0
	for key in pheo:
		counter = counter + pheo[key]
	return counter
	
def edge_Count(Nnum1, Nnum2, topology):
	"""
	caculate the number of edges between any two selected nodes.
	"""
	if topology.has_edge(Nnum1,Nnum2) == True or topology.has_edge(Nnum2,Nnum1) == True:
		return 1
	else:
		return 0
	
def next_Node_Select(pheo):
	"""
	select a node to run the procedure of clustering.
	return: a node.
	"""
	next_Node = -1
	temp_Pheo = -1
	redunt_Time = 0
	for key in pheo:
		if pheo[key] == temp_Pheo:
			redunt_Time = redunt_Time + 1
			ran_Num = randint(1, (redunt_Time+1))
			if ran_Num > redunt_Time:
				next_Node = key
		elif temp_Pheo < pheo[key]:
			redunt_Time = 0
			next_Node = key
			temp_Pheo = pheo[key]
	return next_Node		

def Node_Merge_Judge(Nnum, group, topology, _number_Of_Groups):
	"""
	Judge whether a nodes have been assign into a selceted group.
	return: True-> merged; False-> unmerged.
	"""
	edge = edge_Between_Group(_number_Of_Groups, Nnum, topology, group)
	groupNodes = group_Node_Count(_number_Of_Groups, group)
	if edge == 0:
		return False
	else:
		wsd = eg.cal2dWSDValue(groupNodes, edge, edge, 1)
		if wsd < wsd_Threshold:
			return True
		else:
			return False

def edge_Between_Group(Gnum, Nnum, topology, group):
	"""
	caculate the number of edges between a node and a selected group.
	"""
	counter = 0
	for i in range(nx.number_of_nodes(topology)):
		if group[i] is Gnum:
			if topology.has_edge(i,Nnum) or topology.has_edge(Nnum,i):
				counter = counter + 1
	return counter
	
def group_Node_Count(Gnum, Group):
	count = 0
	for u in Group:
		if Group[u] is Gnum:
			count = count + 1
	return count
	
def group_Merge_Judge(Gnum1, Gnum2, group, topology):
	"""
	Judge whether a group have been assign into a selceted group.
	return: True-> merged; False-> unmerged.
	"""
	edge = cross_Group_Edge_Count(Gnum1, Gnum2, group, topology)
	group_Node1 = group_Node_Count(Gnum1, group)
	group_Node2 = group_Node_Count(Gnum2, group)
	if edge == 0 or group_Node1 == 0 or group_Node2 == 0:
		return False
	else:
		wsd = eg.cal2dWSDValue(group_Node1, edge, edge, group_Node2)
		if wsd < wsd_Threshold:
			return True
		else:
			return False

def cross_Group_Edge_Count(Gnum1, Gnum2, group, topology):
	counter = 0
	for i in range(nx.number_of_nodes(topology)):
		if group[i] is Gnum1:
			for j in range(nx.number_of_nodes(topology)):
				if j != i and group[j] is Gnum2:
					if topology.has_edge(i,j)or topology.has_edge(j,i):
						counter = counter + 1
	return counter

def merge_Group(Gnum1, Gnum2, group):
	for i in range(0, len(group)):
		if group[i] == Gnum2:
			group[i] = Gnum1
	
if __name__ == "__main__":
	main()