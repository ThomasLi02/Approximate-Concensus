import random


class System:
    def __init__(self):
        self.processors = []
        self.r = 1
        self.p = float(input("enter probabilty of lost message"))


class Node:
    def __init__(self, status, round, queue, roundCrash):
        self.status = float(status)
        self.round = int(round)
        self.queue = queue
        self.roundCrash = roundCrash
        self.isCrashed = False


def inAgreement(S): # takes in a System and sees if the processors are in agreement
    maxState = 0
    minState = 1
    for i in range(len(S.processors)):
        if not S.processors[i].isCrashed:
            if S.processors[i].status < minState:
                minState = S.processors[i].status
            if S.processors[i].status > maxState:
                maxState = S.processors[i].status
    return maxState - minState <=0.001

# runs the approximate concensus given a system
def run(S):
    for x in range(len(S.processors)):
        if S.processors[x].roundCrash == S.r:
            S.processors[x].isCrashed = True
    for i in range(len(S.processors)):  # sends message to all processors
        if not S.processors[i].isCrashed:
            send(S.processors[i], S)

    for j in range(len(S.processors)):  # recieves messages from good nodes
        recieve(S.processors[j], S)
        S.processors[j].round = S.processors[j].round + 1

    for k in range(len(S.processors)):
        sum = 0
        ave = 0
        for m in range(len(S.processors[k].queue)):
            if not S.processors[k].queue[m].isCrashed:
                sum += S.processors[k].queue[m].status
        if len(S.processors[k].queue) > 0:
            ave += sum/len(S.processors[k].queue)
        else:
            ave = ave + S.processors[k].status
        S.processors[k].status = ave  # update status
    for p in range(len(S.processors)):
        S.processors[p].queue.clear()
    S.r = S.r + 1
    if not inAgreement(S):  # run again if the processors are not in agreement
        run(S)


def send(node, S):  # puts node in the message queue of all processors in system S
    for k in range(len(S.processors)):
        if not S.processors[k].isCrashed:
            S.processors[k].queue.append(node)


# checks if the messages come from a crashed node, and pops a message with probability p
def recieve(node,S):
    i = 0
    while i < (len(node.queue)):
        if random.random() < S.p:
            node.queue.pop(i)
        else:
            i += 1



answer = ""
mySystem = System()
while answer != "q":
    x = input("input [0,1]: ")
    c = input("input crash round: ")
    processor = Node(x, 1, [], c)
    mySystem.processors.append(processor)
    y = input("q to quit or any key to add new processor")
    answer = y

run(mySystem)
print("round converge: " + str(mySystem.r - 1))
print("Output: " + str(mySystem.processors[0].status))
