from abc import ABCMeta, abstractmethod

class Subject:
    __metaclass__ = ABCMeta


    def register_observer(self, observer):
        """Registers an observer with Subject."""
        pass

    def remove_observer(self, observer):
        """Removes an observer from Subject."""
        pass

    def notify_observers(self):
        """Notifies observers that Subject data has changed."""
        pass

class Observer:
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self):
        """Observer updates by pulling data from Subject."""
        pass

    def register_subject(self, subject):
        """Observer saves reference to Subject."""
        self.subject = subject

    def remove_subject(self):
        """Observer replaces Subject reference to None."""
        self.subject = None

class DisplayElement:
    __metaclass__ = ABCMeta

    @abstractmethod
    def display(self):
        """DisplayElement displays instance data."""
        pass
