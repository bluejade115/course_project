# 记录开销
node_0_cost = [0.0, 1.0, 6.0, float('inf'), float('inf'), float('inf')]
node_1_cost = [1.0, 0.0, 3.0, 4.0, float('inf'), float('inf')]
node_2_cost = [6.0, 3.0, 0.0, 2.0, 6.0, float('inf')]
node_3_cost = [float('inf'), 4.0, 2.0, 0.0, 9.0, 2.0]
node_4_cost = [float('inf'), float('inf'), 6.0, 9.0, 0.0, float('inf')]
node_5_cost = [float('inf'), float('inf'), float('inf'), 2.0, float('inf'), 0.0]
node_all = {0: node_0_cost, 1: node_1_cost, 2: node_2_cost, 3: node_3_cost, 4: node_4_cost, 5: node_5_cost}


class DistanceVector:
    def __init__(self, cost, source_node):
        # 记录所有节点的开销
        self.Cost = cost
        self.SourceNode = source_node
        # 初始化距离向量表
        self.distance_table = {i: [self.Cost[source_node][i], None] for i in range(6)}
        for i in range(6):
            if self.Cost[source_node][i] != float('inf'):
                self.distance_table[i] = [self.Cost[source_node][i], i]

    def update_distance_table(self, other_node, distance_table_other):  # 迭代更新距离向量表
        updated = False
        for node in range(6):
            new_distance = self.distance_table[other_node][0] + distance_table_other[node][0]
            if new_distance < self.distance_table[node][0]:
                self.distance_table[node] = [new_distance, other_node]
                updated = True
        print("the distance table:", self.distance_table)
        return updated

    def get_distance_list(self):  # 返回距离向量表
        return {node: (self.distance_table[node][0], self.distance_table[node][1]) for node in range(6)}


def execute_distance_vector(node_dict):  # 执行所有节点迭代更新
    updated = True
    while updated:
        updated = False
        for source_node in node_dict:
            for neighbor_node in node_dict[source_node].distance_table:
                if (neighbor_node != source_node and node_dict[source_node].update_distance_table
                    (neighbor_node, node_dict[neighbor_node].distance_table)):
                    updated = True


def find_path_from_to(node_dict_1, node1, node2): # 寻找从节点到另一个节点的路径
    path_list = [node1]
    now_node = node1
    next_node = node2
    while True:
        if node_dict_1[now_node].distance_table[next_node][1] == node2:
            path_list.append(node2)
            break
        else:
            path_list.append(node_dict_1[now_node].distance_table[next_node][1])
            now_node = node_dict_1[now_node].distance_table[next_node][1]
    print(f"the path from {node1} to {node2} is:", path_list)


def menu(node_dict_1): # 菜单
    while True:
        print("1. Show distance list from a node")
        print("2. Show path and cost from a node to another node")
        print("3. Stop")
        cmd = input("Input the serial number of options:")
        if cmd == '1':
            node_input = int(input("Which node? "))
            distance_list = node_dict_1[node_input].get_distance_list()
            for node, (cost, next_hop) in distance_list.items():
                next_hop_str = f" from node {next_hop}" if next_hop is not None else ""
                print(f"To node {node}: cost {cost}{next_hop_str}")
        elif cmd == '2':
            node1 = int(input("Node1: "))
            node2 = int(input("Node2: "))
            find_path_from_to(node_dict_1, node1, node2)
        elif cmd == '3':
            break


if __name__ == '__main__':
    node_dict = {i: DistanceVector(node_all, i) for i in range(6)} # 初始化所有节点及其距离向量表
    execute_distance_vector(node_dict) # 迭代更新所有节点
    menu(node_dict) # 进入菜单
