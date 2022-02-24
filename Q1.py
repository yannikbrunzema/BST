
class Node:
    """The node class used
    to implement a BST"""

    def __init__(self, elem):
        """
        The constructor for a node
        :param elem: The node's value
        """
        self.left = None
        self.right = None
        self.data = elem


class BinarySearchTree:
    """The binary search tree
    class. Guarantees a BST upon
    inserting a new node."""

    def __init__(self):
        self.root = None

    def insert(self, element):
        """
        Inserts an element into the BST
        :param element: The element to be inserted.
        """
        if self.root is None:
            self.root = Node(element)
            return
        done = False
        curr_node = self.root
        while not done:
            if element > curr_node.data:
                if curr_node.right is None:
                    curr_node.right = Node(element)
                    done = True
                else:
                    curr_node = curr_node.right
            else:
                if curr_node.left is None:
                    curr_node.left = Node(element)
                    done = True
                else:
                    curr_node = curr_node.left

    def get_tree_height(self, node):
        """
        Calculates the sum of the heights
        of every node in the tree
        :param node: The node to be processed
        :return: curr_node_height: The height of
        the current node being processed
        tree_height_total: The sum of the heights
        of each node in the tree.
        """
        curr_node_height = 0
        tree_height_total = 0
        if node.left is not None:
            temp, sum = self.get_tree_height(node.left)
            if temp > curr_node_height:
                curr_node_height = temp
            tree_height_total += sum

        if node.right is not None:
            temp, sum = self.get_tree_height(node.right)
            if temp > curr_node_height:
                curr_node_height = temp
            tree_height_total += sum

        tree_height_total += curr_node_height
        return 1 + curr_node_height, tree_height_total

    def get_tree_height_result(self, node):
        """Helper function to return only
        the total tree height from get_tree_height"""
        result = self.get_tree_height(node)
        return result[1]

    def get_num_nodes_sub_tree(self, node):
        """Gets the amount of nodes in the subtree
        of a given node.
        :param node: The node to be processed
        :return: The number of nodes in the subtree"""
        if node is None:
            return 0
        return 1 + self.get_num_nodes_sub_tree(node.left) + self.get_num_nodes_sub_tree(node.right)

    def traverse_util(self, node, data):
        """Helper function for the
        get_weight_balance function.
        Calculates the difference between
        the amount of nodes in each nodes subtree
        :param node: The node to be processed
        :param data: The difference list"""
        if node is None:
            return
        left_num_nodes = 0
        right_num_nodes = 0
        if node.left is not None:
            left_num_nodes = self.get_num_nodes_sub_tree(node.left)
        if node.right is not None:
            right_num_nodes = self.get_num_nodes_sub_tree(node.right)
        difference = abs(left_num_nodes - right_num_nodes)
        data.append(difference)
        self.traverse_util(node.left, data)
        self.traverse_util(node.right, data)
        return

    def get_weight_balance_factor(self, root):
        """Calculates the weight balance factor
        using the traverse_util function
        :param: The root node
        :return The weight balance factor"""
        data = []
        self.traverse_util(root, data)
        maximum = max(data)
        return maximum

    def serialize_bst(self, root):
        """Serializes the BST.
        Returns a string."""
        pre_order_tree = []

        def pre_order(node):
            """Traverse the tree in pre-order
            and mark information regarding the
            children of each node in the format
            [(Value, Child_Info), ....]"""
            if node is None:
                return
            info = ''
            if node.right and node.left:
                info = '2'
            if node.right and not node.left:
                info = 'R'
            if node.left and not node.right:
                info = 'L'
            if not node.right and not node.left:
                info = '0'
            data_child_tuple = (node.data, info)
            pre_order_tree.append(data_child_tuple)
            pre_order(node.left)
            pre_order(node.right)
        pre_order(root)
        listToStr = '-'.join([str(elem) for elem in pre_order_tree])
        return listToStr

    def de_serialize_bst(self, serialized):
        """
        :param serialized: The serialized string
        :return: The equivalent BST generated from
        the serialized string.
        """
        temp_list = []
        tuple_list = []
        serialized = serialized.split('-')
        for i in range (len(serialized)):
            temp_list.append(serialized[i])
        for i in range(len(temp_list)):
            tuple_list.append(eval(temp_list[i]))
        value = tuple_list[i][0]
        def rebuild_tree(i):
            """
            Reconstructs the BST from the serialized
            list.
            :param i: Increment variable
            :return: The reconstructed BST
            """
            child_info = tuple_list[i][1]
            value = tuple_list[i][0]
            node = Node(value)
            if child_info == '2' or child_info == 'L':
                node.left = rebuild_tree(i+1)
            if child_info == 'R':
                node.right = rebuild_tree(i+1)
            if child_info == '0':
                print("")
            return node

        return rebuild_tree(0)


    def print_binary_tree(self, root, space, height):
        """Function taken from
        https://www.techiedelight.com/print-two-dimensional-view-binary-tree/
        Function prints tree with the root on the far left."""
        if root is None:
            return

        # increase distance between levels
        space += height

        # print right child first
        self.print_binary_tree(root.right, space, height)
        print()

        # print the current node after padding with spaces
        for i in range(height, space):
            print(' ', end='')

        print(root.data, end='')

        # print left child
        print()
        self.print_binary_tree(root.left, space, height)


if __name__ == "__main__":
    print()
    tree = BinarySearchTree()
    print("Inserting 6,4,9,5,8,7:")
    tree.insert(6)
    tree.insert(4)
    tree.insert(9)
    tree.insert(5)
    tree.insert(8)
    tree.insert(7)
    print()
    print("Tree representation (Left to Right)")
    tree.print_binary_tree(tree.root, 0, 10)
    serialized_string = tree.serialize_bst(tree.root)
    serialized_string = tree.serialize_bst(tree.root)
    print("Serialized string", serialized_string)
    print("Total height:", tree.get_tree_height_result(tree.root))
    print("Weight balance factor:", tree.get_weight_balance_factor(tree.root))
    deserialized_tree = BinarySearchTree()
    deserialized_tree.root = tree.de_serialize_bst(serialized_string)
    print("Resulting deserialized tree:")
    deserialized_tree.print_binary_tree(tree.root, 0, 10)






