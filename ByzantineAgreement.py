import random
import math


class System:
    def __init__(self):
        self.processors = []
        self.r = 1
        self.p = float(input("enter probabilty of lost message"))
        self.maxByz = input("enter upper bound fault processors")
        n = self.processors.len()
        t = self.maxByz
        c = (n - 2*t - 1)/t + 1
        self.termRound = math.log((1/0.001),c)


class Node:
    def __init__(self, status, round, queue, roundFault):
        self.status = float(status)
        self.round = int(round)
        self.queue = queue
        self.roundFault = roundFault
        self.isByz = False


def inAgreement(S): # takes in a System and sees if the processors are in agreement
    maxState = 0
    minState = 1
    for i in range(len(S.processors)):
        if not S.processors[i].isByz:
            if S.processors[i].status < minState:
                minState = S.processors[i].status
            if S.processors[i].status > maxState:
                maxState = S.processors[i].status
    return maxState - minState <=0.001

# runs the approximate concensus given a system
def run(S):
    for x in range(len(S.processors)):  #node becomes Byz if its fault round == round
        if S.processors[x].roundFault == S.r:
            S.processors[x].isByz = True
    for i in range(len(S.processors)):  # sends message to all processors
        if not S.processors[i].isByz:
            send(S.processors[i], S)

    for j in range(len(S.processors)):  # receives messages from non Byz nodes
        recieve(S.processors[j], S)
        S.processors[j].round = S.processors[j].round + 1

    for k in range(len(S.processors)):
        top = 0
        bottom = 1
        sum = 0
        ave = 0
        for m in range(len(S.processors[k].queue)):

            if not S.processors[k].queue[m].isByz: # if not Byz node, add the status
                value = S.processors[k].queue[m].status
                sum += S.processors[k].queue[m].status
            else: # if byzantine node, send a random value instead
                randNum = random.random()
                value= randNum
                sum += randNum
            if value> top:   # process for discarding the top and bottom value
                top = value
            if value<bottom:
                bottom = value
        sum = sum-top-bottom
        if len(S.processors[k].queue) > 0:
            ave += sum/(len(S.processors[k])-2)
        else:
            ave = ave + S.processors[k].status
        S.processors[k].status = ave  # update status
    for p in range(len(S.processors)):
        S.processors[p].queue.clear()
    S.r = S.r + 1
    if not inAgreement(S) or not S.r == S.termRound:  # run again if the processors are not in agreement
        run(S)


def send(node, S):  # puts node in the message queue of all processors in system S
    for k in range(len(S.processors)):
        if not S.processors[k].isByz:
            S.processors[k].queue.append(node)


#  pops a message in queue with probability p
def recieve(node,S):
    i = 0
    while i < (len(node.queue)):
        if random.random() < S.p: #probability p a message is lost
            node.queue.pop(i)
        else:
            i += 1



answer = ""
mySystem = System()
while answer != "q":
    x = input("input [0,1]: ")
    c = input("input fault round: ")
    processor = Node(x, 1, [], c)
    mySystem.processors.append(processor)
    y = input("q to quit or any key to add new processor")
    answer = y

run(mySystem)
print("round converge: " + str(mySystem.r - 1))
print("Output: " + str(mySystem.processors[0].status))
