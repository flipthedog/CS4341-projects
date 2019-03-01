import copy

class Node:

    def __init__(self, x, y, parent = None):
        self.x = x
        self.y = y
        self.parent = parent

        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def calculate_md(self, end):

        return abs(self.point.x - self.end.x) + abs(self.point.y - self.end.y)

    def is_same(self, compare_node):

        if (abs(compare_node.x - self.x) == 0 and abs(compare_node.y - self.y) == 0):
            return True
        else:
            return False

class Astar:

    def __init__(self, start, end, wrld):

        self.width = wrld.width()
        self.height = wrld.height()
        self.start_node = Node(start[0], start[1])
        self.end_node = Node(end[0], end[1])
        self.path = None

    def return_path(self):
        path = [[self.start_node.x, self.start_node.y]]

        current_node = self.end_node

        while current_node is not None:
            if current_node is not None:
                print("Pulled", current_node.x, current_node.y)
                path.insert(0,[current_node.x, current_node.y])
                current_node = current_node.parent
            else:
                print("None")
        return path

    def find_path(self, wrld):
        evaluated = []
        notEvaluated = [[self.start_node.f_cost, self.start_node]]
        evaluated.append(self.start_node)
        notEvalCheck = []
        notEvalCheck.append(self.start_node)

        previous_steps = {}
        previous_steps[1] = self.start_node

        g_cost = {}
        f_cost = {}

        g_cost[self.start_node] = 0

        path_found = False
        current_node = None
        prev_node = None
        while not len(notEvaluated) <= 0 and not path_found:

            notEvaluated.sort(reverse=False, key=lambda x: x[0])

            current_node = notEvaluated.pop(0)[1]

            if current_node.is_same(self.end_node):
                return self.return_path()

            evaluated.append(current_node)

            x = current_node.x
            y = current_node.y

            for i in range(3):

                i -= 1


                for j in range(3):

                    j -= 1

                    # print(i,j)

                    # if the postition is in world bounds
                    if not (x + i >= self.width or x + i < 0 or y + j >= self.height or y + j < 0):
                        if not (j != 0 and i != 0) and not wrld.wall_at(x + i, y + j):

                            neighbor = Node(x + i, y + j)

                            if neighbor in evaluated:
                                continue

                            neighbor.parent = copy.deepcopy(current_node)

                            if neighbor.x == self.end_node.x and neighbor.y == self.end_node.y:
                                self.end_node.parent = copy.deepcopy(current_node)
                            tentative_gcost = g_cost[current_node] + self.find_gcost(neighbor, wrld)

                            if not self.hasnode(neighbor, notEvaluated):
                                g_cost[neighbor] = tentative_gcost
                                f_cost[neighbor] = g_cost[neighbor] + self.find_heuristiccost(neighbor, wrld)

                                notEvaluated.append([f_cost[neighbor], neighbor])

                            elif (tentative_gcost >= g_cost[neighbor]):
                                continue

                            previous_steps[neighbor] = current_node
                            neighbor.parent = copy.deepcopy(current_node)

                            g_cost[neighbor] = tentative_gcost
                            f_cost[neighbor] = abs(g_cost[neighbor]) + abs(self.find_heuristiccost(neighbor, wrld))

        if not path_found:

            print("\n ----------NO PATH REACHED ---------")

    def hasnode(self, node2, array):

        sub_array = []
        for element in array:
            sub_array.append(element[1])

        for node in sub_array:

            if node.x == node2.x and node.y == node2.y:
                return True

        return False

    def find_gcost(self, node, wrld):
        return 1

    def find_heuristiccost(self, node, wrld):
        return self.manhattan_distance(node, self.end_node)

    def manhattan_distance(self,node_1, node_2):

        return abs(node_1.x - node_2.x) + abs(node_1.y - node_2.y)