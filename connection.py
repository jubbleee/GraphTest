import node
class Connection:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.weight = 1
        self.decay = 100
        self.failed = False
