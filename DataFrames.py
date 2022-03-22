from abc import ABC, abstractmethod
from random import randint

class DataFrame(ABC):

    def __init__(self):
        self.insert_costs = []
        self.search_costs = []

    @abstractmethod
    def insert(self):
        """
            Inserts the key-value pair in accordance with the type of DataFrame and stores 
            the number of opertions.
        """
    
    @abstractmethod
    def search(self):
        """ 
            Searches for the value associated to a key in accordance with the type
            of DataFrame and stores the number of opertions.
        """

    def get_average_costs(self):
        """ Returns the average of insert / search costs """
        assert len(self.insert_costs) != 0 and len(self.search_costs) != 0, "Must search/insert first"
        return (sum(self.insert_costs)/len(self.insert_costs),
                sum(self.search_costs)/len(self.search_costs))
                
    def get_costs(self):
        """ Returns the insert / search costs """
        return self.insert_costs, self.search_costs

class Node:
    def __init__(self, key, value):
        self.left = None
        self.right = None
        self.key = key
        self.value = value

class TreapNode(Node):
    def __init__(self, key, value, priority):
        super().__init__(key, value)
        self.priority = priority


class Tree(DataFrame):

    def search(self, key):
        self.search_costs.append(0)
        return self.__search(self.root, key)

    def __search(self, curr_node, key):
        if curr_node is None:
            print(f"key: {key} not found")
            self.search_costs[-1] = 0
            return None

        self.search_costs[-1] += 1
        if curr_node.key == key:
            return curr_node.value
        else:
            if key <= curr_node.key:
                return self.__search(curr_node.left, key)
            else:
                return self.__search(curr_node.right, key)

    def walk(self):
        """ Assumes that the node object has .left and .right fields and prints all elements """
        self.__walk(self.root)

    def __walk(self, curr_node):
        if curr_node is not None:
            print(curr_node.key, curr_node.value)
            self.__walk(curr_node.left)
            self.__walk(curr_node.right)


class BinaryTree(Tree):

    def __init__(self):
        super().__init__()
        self.root: Node = None

    def insert(self, key, value):
        new = Node(key, value)
        self.insert_costs.append(0)
        if self.root is None:
            self.root = new
        else:
            self.__insert(self.root, new)

    def __insert(self, curr_node, new_node):
        self.insert_costs[-1] += 1
        
        if new_node.key <= curr_node.key:
            if curr_node.left is None:
                curr_node.left = new_node
            else:
                self.__insert(curr_node.left, new_node)
        
        else:
            if curr_node.right is None:
                curr_node.right = new_node
            else:
                self.__insert(curr_node.right, new_node)
        

class Treap(Tree):

    def __init__(self, max_range=10**3):
        super().__init__()
        self.max_range = max_range
        self.root: TreapNode = None


    def insert(self, key, value):
        new = TreapNode(key, value, self.__generator())
        self.insert_costs.append(0)
        if self.root is None:
            self.root = new
            return
        
        left, right = self.split(self.root, key)
        self.root = self.merge(left, new)
        self.root = self.merge(self.root, right)

    def split(self, node, key):
        self.insert_costs[-1] += 1
        if node is None:
            return None, None
        
        if key < node.key:
            left, node.left = self.split(node.left, key)
            return left, node
        else:
            node.right, right = self.split(node.right, key)
            return node, right

    def merge(self, left, right):
        self.insert_costs[-1] += 1
        if left is None:
            return right
        if right is None:
            return left

        if left.priority > right.priority:
            left.right = self.merge(left.right, right)
            return left
        else:
            right.left = self.merge(left, right.left)
            return right

    def __generator(self):
        return randint(1, self.max_range)

class Item:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class LinkedList(DataFrame):
    
    def __init__(self):
        super().__init__()
        self.root: Item = None

    def insert(self, key, value):
        new = Item(key, value)
        
        if self.root is None:
            self.insert_costs.append(0)
            self.root = new
            return

        item = self.root
        self.insert_costs.append(1)
        while (item.next is not None):
            item = item.next
            self.insert_costs[-1] += 1
        
        item.next = new
         

    def search(self, key):
        assert self.root is not None, "Must insert atleast 1 element before searching"
        self.search_costs.append(0)
        item = self.root

        if item.key == key:
            return item.value

        while (item.next is not None):
            self.search_costs[-1] += 1
            if item.next.key == key:
                temp = item.next
                item.next = item.next.next
                temp.next = self.root
                self.root = temp
                return self.root.value
            else:
                item = item.next


        print(f"Value with key: {key} not found")
        return 0

    def print_linked_list(self):
        """ prints the current linked list from root to tail """
        item = self.root
        while (item is not None):
            print(item.value, end=" -> ")
            item = item.next
        print("None\n")
