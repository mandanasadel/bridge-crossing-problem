import bisect, itertools

class Node:
    def __init__(self, cost, heuristic, state, steps):
        self.cost = cost
        self.evaluation_function = cost + heuristic
        self.state = state
        self.steps = steps

    def __lt__(self, other):
        return self.evaluation_function < other.evaluation_function

    def print_steps(self):
        i = 0
        while i < len(self.steps):
            if (i+1) % 3 == 0:
                print(self.steps[i], '<-')
                i += 1
            else:
                print(self.steps[i], self.steps[i+1], '->')
                i += 2

class Tree:
    def __init__(self, fitness):
        state = [0] * len(fitness)
        steps = []
        cost = 0
        root = Node(cost, 0, state, steps)

        self.orig = fitness
        self.fringe = [root]
        self.fitness = sorted(fitness)

    def has_repeated_states(self, node):
        for item in self.fringe:
            if node.state == item.state and node.evaluation_function < item.evaluation_function:
                self.fringe.remove(item)
                bisect.insort(self.fringe, node)
                return True
            if node.state == item.state:
                return True
        return False
    '''
    h = the sum of every other time taken by people on the left of the bridge
    We choose this heuristic to minimize the wasted time by letting the slowest
    and 2nd slowest, 3rd slowest and 4th slowest, and so on cross the bridge
    to "mask" the 2nd person's time
    '''
    def find_heuristic(self,node,place):
        l = []
        h = 0
        for elem in list(range(len(self.fitness))):
                if node.state[elem] == place:
                        l.append(self.fitness[elem])
        l = l[::-1]
        for elem in range(len(l),2):
                h += l[elem]
        #print(h)
        return h

    def generate_nodes(self,node):
        fitness_len = len(self.fitness)
        if len(node.steps) % 3 == 0:
            #print("oldL " ,node.state," ",node.cost)
            h = self.find_heuristic(node,0)
            fin = []
            left = []
            c = 0
            for elem in range(fitness_len):
                    if node.state[elem] == 0:
                            left.append(elem)
                            c += 1
            a = left[0]
            b = left[1]           
            if c == 2:
                fin = [[a,b]]                
            else:
                c = left[-1]
                d = left[-2]
                fin = [[a,b],[a,c],[d,c]]
               
            c = 0
            #print(fin)
            for elem in fin:
                    new_state = list(node.state)

                    new_state[elem[0]] = 1
                    new_state[elem[1]] = 1
                    new_steps = list(node.steps)
                    if(self.fitness[elem[0]]==self.fitness[elem[1]]):
                        for f in range(self.orig.index(self.fitness[elem[0]])+1,fitness_len):
                            if(self.fitness[elem[1]]==self.fitness[f]):
                                new_steps.extend([self.orig.index(self.fitness[elem[0]])+1, f+1])
                                break
                    else:
                        new_steps.extend([self.orig.index(self.fitness[elem[0]])+1, self.orig.index(self.fitness[elem[1]])+1])

                    new_cost = node.cost + max(self.fitness[elem[0]], self.fitness[elem[1]])
                    new_node = Node(new_cost, h , new_state, new_steps)
                    #print("newL ",new_state," ",new_cost)
                    if not self.has_repeated_states(new_node):
                            bisect.insort(self.fringe, new_node)
        else:
            #print("oldR " ,node.state," ",node.cost)
            h = self.find_heuristic(node,1)
            for elem in list(range(fitness_len)):
                if (node.state[elem] == 1):
                    new_state = list(node.state)
                    new_state[elem] = 0

                    new_steps = list(node.steps)
                    new_steps.append(self.orig.index(self.fitness[elem])+1)

                    new_cost = node.cost + self.fitness[elem]

                    new_node = Node(new_cost, h, new_state, new_steps)
                    #print("newR ",new_state," ",new_cost)
                    if not self.has_repeated_states(new_node):
                        bisect.insort(self.fringe, new_node)

    def a_star(self):
        num_visited = 0;
        fitness_len = len(self.fitness)
        while True:
            if not self.fringe:
                return 'Failure'

            # Explore Fringe
            node = self.fringe.pop(0)
            num_visited += 1
            if node.state == [1] * fitness_len:
                print(node.cost, num_visited)
                node.print_steps()
                return 'Success'

            self.generate_nodes(node)

import time
t = time.process_time()

#inp = [1,2,5,10] #(a)
#inp = [1,2,5,10,3,4,14,18,20,50] #(b)
inp = [1,2,5,10,12,17,24,21,20,20,11,33,15,19,55] #(c)

state_space = Tree(inp)
state_space.a_star()

elapsed_time = time.process_time() - t
print(elapsed_time)
