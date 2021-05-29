import math 
class Graph:
	nodeNames = []
	no_of_vertices = 0 
	adjacencyList = [] #2 dimenstional array to store adjacenct List
	outBoundLinksCount = [] #array to store total outbounds of a vertex 
	def __init__(self, no_of_vertices):
	    self.no_of_vertices = no_of_vertices;
	    self.nodeNames = [chr(i) for i in range(65,no_of_vertices+65)]
	    self.adjacencyList = [[0 for j in range(no_of_vertices)] for i in range(no_of_vertices)] #intialize with 0
	    self.outBoundLinksCount = [0] * no_of_vertices

	def addEdge(self, fromVertex,toVertex):
	    self.adjacencyList[fromVertex-1][toVertex-1] = 1 #make postion as adjacencyList[i][j] = 1  when edge present between i and j
	    self.outBoundLinksCount[fromVertex-1]+=1  #counting outbounds

	def eliminateDeadLinks(self): #function to eliminate deadLinks
		deadLinks = []
		for i in range(self.no_of_vertices):
			if self.outBoundLinksCount[i] == 0 : #if outboundLinksCount is 0 then it is a dead link
				deadLinks.append(i)
		updatedAdjacenyList = []
		newOutBoundLinksCount = []
		for i in range(self.no_of_vertices): #loop to remove deadlink info from adjacenctList, outBoundsCount, nodeNames
			node = []
			count = 0 
			for j in range(self.no_of_vertices):
				if i not in deadLinks and j not in deadLinks:
					node.append(self.adjacencyList[i][j])
					if self.adjacencyList[i][j] ==1:
						count+=1
			if count!=0:
				newOutBoundLinksCount.append(count)
			if len(node)!=0:
				updatedAdjacenyList.append(node)
			else:
				self.nodeNames.pop(i)

		self.outBoundLinksCount = newOutBoundLinksCount
		self.no_of_vertices = len(updatedAdjacenyList)
		self.adjacencyList = updatedAdjacenyList


def matrixMultiplication(matrix1,matrix2): #multiplication of 2 matrices where matrix1 = M X M and matrix2 = M X 1
	outMatrix = [0] * len(matrix1)
	for i in range(len(matrix1)):
		for j in range(len(matrix1)):
			outMatrix[i] += matrix1[i][j]*matrix2[j] 
	return outMatrix

def printRankOrder(graph,rankMatrix): #printing Ranked Order of Nodes
	print("\n:::::::Ranked Order::::::")
	rankOrder = {graph.nodeNames[i]: rankMatrix[i]  for i in range(graph.no_of_vertices)}
	sortedRankOrder = sorted(rankOrder.items(), key=lambda x: x[1], reverse=True)
	for i in sortedRankOrder:
		print("{} : {}".format(i[0],round(i[1],2)))

def pageRankCalc(graph,damping_factor): #pageRank Calculation
	graph.eliminateDeadLinks() #eliminating deadLinks
	no_of_vertices = graph.no_of_vertices
	M = [[float(graph.adjacencyList[i][j]/float(graph.outBoundLinksCount[i])) for j in range(no_of_vertices)] for i in range(no_of_vertices)] #probability matrix
	transposeM = [[M[j][i] for j in range(no_of_vertices)] for i in range(no_of_vertices)]
	dampingFactorMatrix = [damping_factor] * no_of_vertices 

	rankMatrix = matrixMultiplication(transposeM,dampingFactorMatrix)
	print("iteration "+str(1)+" :")
	print([round(x,2) for x in rankMatrix])
	print(" ")

	k=2
	while(True):
		newRankMatrix = matrixMultiplication(transposeM,rankMatrix)
		print("iteration "+str(k)+" :")
		print([round(x,2) for x in newRankMatrix])
		print(" ")
		if([round(x,2) for x in newRankMatrix] == [round(x,2) for x in rankMatrix]):
			break
		rankMatrix = newRankMatrix
		k+=1

	print("After "+str(k)+" iteration the values are same")


	printRankOrder(graph,rankMatrix)

f = open('graph.txt', 'r')
data = f.readlines()
graph = Graph(int(data[0])) #first line of file will be no of vertices
for i in range (1,len(data)):
	fromVertex,toVertex = data[i].split(' ') #taking edge data from file
	graph.addEdge(int(fromVertex),int(toVertex)) 

damping_factor = float(input("Enter Dampling Factor(d) : "))
pageRankCalc(graph,damping_factor)
