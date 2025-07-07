"""Repository pattern implementation for data persistence"""
from abc import ABC, abstractmethod

class Repository(ABC):
    """Abstract base class for repository pattern"""
    
    @abstractmethod
    def add(self, obj):
        """Add an object to the repository"""
        pass

    @abstractmethod
    def get(self, obj_id):
        """Retrieve an object by its ID"""
        pass

    @abstractmethod
    def get_all(self):
        """Retrieve all objects"""
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Update an object with new data"""
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Delete an object by its ID"""
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Find an object by a specific attribute"""
        pass


class InMemoryRepository(Repository):
    """In-memory implementation of the repository pattern"""
    
    def __init__(self):
        """Initialize the in-memory storage"""
        self._storage = {}

    def add(self, obj):
        """Add an object to the repository"""
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Retrieve an object by its ID"""
        return self._storage.get(obj_id)

    def get_all(self):
        """Retrieve all objects"""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Update an object with new data"""
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """Delete an object by its ID"""
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """Find an object by a specific attribute"""
        for obj in self._storage.values():
            if hasattr(obj, attr_name) and getattr(obj, attr_name) == attr_value:
                return obj
        return None
