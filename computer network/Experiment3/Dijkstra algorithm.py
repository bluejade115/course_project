# 记录所有节点的开销
node_0_cost = [0.0, 1.0, float('inf'), 6.0, float('inf'), float('inf')]
node_1_cost = [1.0, 0.0, 3.0, 4.0, float('inf'), float('inf')]
node_2_cost = [float('inf'), 3.0, 0.0, 2.0, 6.0, float('inf')]
node_3_cost = [6.0, 4.0, 2.0, 0.0, 9.0, 2.0]
node_4_cost = [float('inf'), float('inf'), 6.0, 9.0, 0.0, float('inf')]
node_5_cost = [float('inf'), float('inf'), float('inf'), 2.0, float('inf'), 0.0]
node_all = {0: node_0_cost, 1: node_1_cost, 2: node_2_cost, 3: node_3_cost, 4: node_4_cost, 5: node_5_cost}


class Node:
    def __init__(self, cost, source_node):
        # 全部开销信息
        self.Cost = cost
        # 源节点的开销信息
        self.cost_self = cost[source_node]
        # 存储源节点
        self.SourceNode = source_node
        # 试验清单
        # {x:[y,z]} x是可选节点，y是从源节点到x的开销，z是z是上一跳的节点
        self.available_list = {i: [self.cost_self[i], source_node] for i in range(0, 6)
                               if self.cost_self[i] != float('inf') and self.cost_self[i] != 0.0}
        # 永久清单 开销 下一跳节点
        # {x:[y,z]} x是从源节点到x节点，y是开销，z是上一跳的节点
        self.best_cost_list = {source_node: [self.cost_self[source_node], source_node]}

        # print(self.available_list)

    def choose_from_available_list(self): # 从试验清单里选择节点
        if self.available_list:
            # 得到下一个节点
            available_list_copy = {index: value[0] for index, value in self.available_list.items()}
            min_cost_node = min(available_list_copy, key=available_list_copy.get)
            # print("min_cost", self.available_list[min_cost_node])
            self.best_cost_list[min_cost_node] = self.available_list[min_cost_node]
            del self.available_list[min_cost_node]
            return min_cost_node
        else:
            return None

    def update_after_chosen(self, min_cost_node): # 选择节点后进行更新
        # i 是节点 值代表开销
        if min_cost_node:
            for i in range(0, 6):  # 对列表进行遍历
                cost = self.Cost[min_cost_node][i]
                if i in self.best_cost_list:
                    if self.best_cost_list[min_cost_node][0] + cost < self.best_cost_list[i][0]:
                        self.best_cost_list[i][0] = self.best_cost_list[min_cost_node] + cost
                        self.best_cost_list[i][1] = min_cost_node
                elif i in self.available_list:
                    if self.best_cost_list[min_cost_node][0] + cost < self.available_list[i][0]:
                        self.available_list[i][0] = self.best_cost_list[min_cost_node][0] + cost
                        self.available_list[i][1] = min_cost_node
                else:
                    self.available_list[i] = [self.best_cost_list[min_cost_node][0] + cost, min_cost_node]
                # print("latest available list",self.available_list)

    def update_loop_v1(self): # 循环更新
        while True:
            self.update_after_chosen(self.choose_from_available_list())
            if self.available_list:
                # print(f"{self.SourceNode} 's best cost is", self.best_cost_list)
                continue
            else:
                break

        return self.best_cost_list


def execute_node(source_node):
    if source_node ==12345: # 表示更新所有节点
        for i in range(0,6):
            node = Node(node_all, i)
            temp_dict_0 = node.update_loop_v1()
            temp_dict = {}
            for i in range(0, 6):
                temp_dict[i] = temp_dict_0[i]
            print(f"{node.SourceNode} 's best cost is", temp_dict)
    else: # 更新某一节点
        node = Node(node_all, source_node)
        temp_dict_0 = node.update_loop_v1()
        temp_dict = {}
        for i in range(0, 6):
            temp_dict[i] = temp_dict_0[i]
        print(f"{node.SourceNode} 's best cost is", temp_dict)


def find_path(node1, node2): # 寻找路径
    node = Node(node_all, node1)
    _ = node.update_loop_v1()
    path_list = []
    path_index = 0
    node_index = node2
    while True:
        path_list.append(node.best_cost_list[node_index][1])
        if node.best_cost_list[node_index][1] == node1:
            print(f"the path from {node1} to {node2} is:", end='')
            path_list.reverse()
            path_list.append(node2)
            for i in path_list:
                print(i, end=' ')
            print()
            print("distance list is",end=' ')

            for i in path_list:
                print(node.best_cost_list[i][0],end=' ')
            print()
            break
        else:
            node_index = path_list[path_index]
            path_index += 1


def menu(): # 菜单
    while True:
        print("1. show the distance list of node")
        print("2. show the path from a node to other node")
        print("3. show all path with distance")
        print("4. stop")
        cmd = input("input the serial number of options:")
        if cmd == '1':
            node_input = int(input("which node?"))
            execute_node(node_input)
        elif cmd == '2':
            node1 = int(input("node1:"))
            node2 = int(input("node2:"))
            find_path(node1, node2)
        elif cmd == '3':
            execute_node(12345)
        elif cmd == '4':
            break


if __name__ == '__main__':
    menu()
