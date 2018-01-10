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

import os, sys
import networkx as nx	#->https://networkx.github.io/
import Core.IOstream as IO
import Core.AWSCA as AWSCA

def main():
	G = nx.Graph()
	G = IO.load_csv(sys.argv[1])
	group = {}
	AWSCA.Clustering(G, group)
	IO.OutputNode(group)
	#IO.showGraph(G)
		
if __name__ == "__main__":
	main()


