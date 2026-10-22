class Node:
    def __init__(self, freq, symbol=None):
        self.__freq = 0
        self.__symbol = symbol

def get_freq(self):
    return self.__freq
def get_symbol(self):
    return self.__symbol
def __lt__(self,other):
    return self.__freq < other.get_freq()



class Huffman:
    def __init__(self):
        #frequency table
        self.__freq = dict()
        #forest of nodes
        self.__forest = []
        self.__left = None
        self.__right = None

    def get_left(self):
        return self.__left
    def get_right(self):
        return self.__right

    def set_left(self, Node):
        return self.__left(Node)
    def set_right(self,Node):
        return self.__right(Node)

    def compute_frequencies(self, message):
        for char in message:
            if char in self.__freq:
                self.__freq[char] += 1
            else:
                self.__freq[char] = 1

    def initalize_forest(self):
        for symbol in self.__freq:
            #create a node for this symbol and its frequency
            node = Node(self.__freq[symbol], symbol)
            # add the node to the forest
            self.__forest.append(node)

    def build_huffman_tree(self):
        while len(self.__forest) > 1:
            #find the two smallest trees in the forest
            small1 =self.smallest_node()
            small2 = self.smallest_node()
            #combine them
            combined_freq = small1.get_freq() + small2.get_freq()
            #create a new node without symbol
            new_node = Node(combined_freq)
            #place this node to the forest
            self.__forest.append(new_node)


    def smallest_node(self):
        smallest_index = 0
        for i in range(1,len(self.__forest)):
            if self.__forest[i] < self.__forest[smallest_index]:
                smallest_index = i
        smallest = self.__forest.remove(smallest_index)
        return smallest

