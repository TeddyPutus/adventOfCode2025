total_possible_paths = 0
BEAM_SPLITTER = "^"

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.straight = None

root = Node(0)
with open("C:/Users/teddy/IdeaProjects/adventOfCode2025/input_files/day_7.txt", "r") as f:
    input_data = f.readlines()
node_layer = set()
new_node_data = {}

cache = {}

def get_total_paths(node):
    if node is None:
        return 0
    
    if node.left is None and node.right is None and node.straight is None:
        # A leaf is end of path
        return 1

    if node in cache:
        # Don't bother with recursion if we've already solved
        return cache[node]

    total = 0
    if node.left: 
        total += get_total_paths(node.left)
    if node.right: 
        total += get_total_paths(node.right)
    if node.straight: 
        total += get_total_paths(node.straight)

    cache[node] = total
    return total

for i, line in enumerate(input_data):
    if i == 0:
        root = Node(line.index("S"))
        print(f"Root node is: {root.data}")
        node_layer = [root]
        continue
    beam_splitters = {i for i, ltr in enumerate(line) if ltr == BEAM_SPLITTER}
    
    if not beam_splitters:
        continue

    new_node_layer = set()
    for node in node_layer:
        if node.data in beam_splitters:
            if (new_node:=new_node_data.get(f"{i},{node.data + 1}")) is not None:
                node.right = new_node
            else:
                right_node =  Node(node.data + 1)
                new_node_data[f"{i},{node.data + 1}"] = right_node
                node.right = right_node
            if (new_node:=new_node_data.get(f"{i},{node.data - 1}")) is not None:
                node.left = new_node
            else:
                left_node =  Node(node.data - 1)
                new_node_data[f"{i},{node.data - 1}"] = left_node
                node.left = left_node
            new_node_layer.add(node.left)
            new_node_layer.add(node.right)
        else:
            if (new_node:=new_node_data.get(f"{i},{node.data}")) is not None:
                node.straight = new_node
            else:
                straight_node =  Node(node.data)
                new_node_data[f"{i},{node.data}"] = straight_node
                node.straight = straight_node
            new_node_layer.add(node.straight)
    if new_node_layer:
        node_layer = new_node_layer
        

print(f"Total possible paths: {get_total_paths(root)}")
