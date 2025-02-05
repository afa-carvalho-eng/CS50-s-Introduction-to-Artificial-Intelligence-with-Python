import sys

class Node():
    def __init__(self, state, parent, action, path_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):