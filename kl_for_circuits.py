#kernighan_lin_algorithm_with_input_in_ISCAS85format
with open('netlist.isc','r') as graphfile:
    temp = []
    for line in graphfile:
        if line[0] != "*":
            temp.append(line)
n = len(temp)
split = [[]for i in range(n)]
for i in range(n):
    split[i] = temp[i].split()
inputnodes = []
fromnodes = []
faninnodesforgates = []
gates = []
#Spliting the nodes based on their types
for i in split:
    if 'inpt' in i:
        inputnodes.append(i)
    elif 'from' in i:
        fromnodes.append(i)
    elif 'and' in i or 'nand' in i or 'or' in i or 'nor' in i or 'xor' in i or 'xnor' in i or 'buff' in i or 'not' in i:
        gates.append(i)
    else:
        faninnodesforgates.append(i)
nodes = len(gates)
A = [[0 for x in range(nodes)] for y in range(nodes)]

#function to update gate to gate edges to adjacency matrix
def adjacentmatrix(node,fanin,nodeindex):
    for i in range(len(fanin)):
        for j in range(len(fanin[i])):
            if fanin[i][j] == node:
                A[i][nodeindex] = 1
                A[nodeindex][i] = 1
    return


#function to update from node edges to adjacency matrix
def fromedges(nodefrom, innodename, fanin):
    index=[]
    for i in range(nodes):
        if gates[i][1] == innodename:
            index.append(i)
    for i in range(len(fanin)):
        for j in range(len(fanin[i])):
            if fanin[i][j] in nodefrom:
                index.append(i)
    for k in index:
        for l in index:
            if k != l:
                A[k][l] = 1
                A[l][k] = 1
    return


for i in range(nodes):
    node = gates[i][0]
    adjacentmatrix(node, faninnodesforgates, i)
nodesfrom = []
for i in range(len(fromnodes)):
    if fromnodes[i][0] not in nodesfrom:
        nodesfrom = []
        nodesfrom.append(fromnodes[i][0])
        for j in range(i+1, len(fromnodes)):
            if fromnodes[i][3] == fromnodes[j][3]:
                nodesfrom.append(fromnodes[j][0])
        #print(nodesfrom)
        fromedges(nodesfrom, fromnodes[i][3], faninnodesforgates)

print "The adjacency matrix is A=",A
#Initial partition of nodes
left = []
right = []
for i in range(nodes):
    if i%2 == 0:
        left.append(i)
    else:
        right.append(i)
print "The initial partitions are left=",left,"right=",right
#Function to calculate external cost
def external(left,right):
    EA=[0 for x in range(nodes)]
    for i in range(len(left)):
        for j in range(len(right)):
            if A[left[i]][right[j]] == 1:
                EA[left[i]] = EA[left[i]]+1
    for i in range(len(right)):
        for j in range(len(left)):
            if A[right[i]][left[j]] == 1:
                EA[right[i]] = EA[right[i]]+1
    return EA
#Function to calculate internal cost
def internal(left,right):
    IA = [0 for x in range(nodes)]
    for i in range(len(left)):
        for j in range(len(left)):
            if i != j and A[left[i]][left[j]] == 1:
                IA[left[i]] = IA[left[i]]+1
    for i in range(len(right)):
        for j in range(len(right)):
            if i != j and A[right[i]][right[j]] == 1:
                IA[right[i]] = IA[right[i]]+1
    return IA
#Function to swap nodes from one partition to another
def swap(n1,n2):
    for i in range(len(left)):
        if left[i] == n1:
            k = i
            break
    for j in range(len(right)):
        if right[j] == n2:
            l = j
            break
    tempo = 0
    tempo = left[k]
    left[k] = right[l]
    right[l] = tempo
    return
#Kernighan-lin algorithm
swapped=[]
while True:
    EA = external(left, right)
    IA = internal(left, right)
    D = [a - b for a, b in zip(EA, IA)]
    print "The new partitions are", left, right
    print "The external cost for each node is", EA
    print "The internal cost for each node is", IA
    print "D values are", D
    cutcost = 0
    for i in left:
        cutcost = cutcost+EA[i]
    print "The cutcost of current partition is", cutcost
    G = []
    gain = []
    for i in left:
        for j in right:
            if i not in swapped and j not in swapped:
                gain.append(D[i]+D[j]-2*A[i][j])
                G.append([i, j, D[i]+D[j]-2*A[i][j]])
    print "The gains are", G
    if max(gain) <= 0:
        break
    else:
        for i in range(len(G)):
            if G[i][2] == max(gain):
                swapped.append(G[i][0])
                swapped.append(G[i][1])
                swap(G[i][0], G[i][1])
                break
print "The final partitions are", left, right
print "The final cutcost is", cutcost
