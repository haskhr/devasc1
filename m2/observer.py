#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: Simple implementation of the Observer design pattern without any
fancy packages or frameworks.
"""


class Observer1:
    def __init__(self, name):
        self.name = name

    def update(self):
        print(f"{self.name}: observer1 update")


class Observer2:
    def __init__(self, name):
        self.name = name

    def update(self):
        print(f"{self.name}: observer2 update")


class Subject:
    def __init__(self, observers=set()):
        self.observers = observers

    def register(self, observer):
        self.observers.add(observer)

    def unregister(self, observer):
        self.observers.remove(observer)

    def notify(self):
        for observer in self.observers:
            observer.update()


o1 = Observer1("o1")
o2 = Observer2("o2")
s = Subject({o1})
s.register(o2)
s.notify()
s.unregister(o2)
s.notify()
