#!/usr/bin/python

class Node(object):
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node
    
    def get_data(self):
        return self.data
    
    def get_next(self):
        return self.next_node
    
    def set_next(self, new_next):
        self.next_node = new_next
    
    def print_data(self):
        print (self.data)

class LinkedList(object):
    def __init__(self, head=None):
        self.head = head
    
    def insert(self, data):
        new_node = Node(data)
        new_node.set_next(self.head)
        self.head = new_node
    
    def size(self):
        current = self.head
        count = 0
        while current:
            count += 1
            current = current.get_next()
        return count
    
    def search(self, data):
        current = self.head
        found = False
        while current and found is False:
            if current.get_data() == data:
                found = True
            else:
                current = current.get_next()
        if current is None:
            raise ValueError("Data is not in linked list.")
        return current
    
    def delete(self, data):
        current = self.head
        previous = None
        found = False
        while current and found is False:
            if current.get_data() == data:
                found = True
            else:
                previous = current
                current = current.get_next()
        if current is None:
            raise ValueError("Data is not in linked list.")
        if previous is None:
            self.head = current.get_next()
        else:
            previous.set_next(current.get_next())

if __name__ == "__main__":
    my_solo_node = Node("Hello")
    my_solo_node.print_data()

    my_node = Node()
    my_list = LinkedList(my_node)
    for i in range(0, 9):
        my_list.insert(Node(i))
        