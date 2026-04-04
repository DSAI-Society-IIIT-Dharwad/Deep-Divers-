from abc import ABC, abstractmethod


class BaseAgent(ABC):
    @abstractmethod
    def train(self, steps, callback=None):
        raise NotImplementedError

    @abstractmethod
    def save(self, path):
        raise NotImplementedError

    @abstractmethod
    def load(self, path):
        raise NotImplementedError

    @abstractmethod
    def predict(self, obs, deterministic=True):
        raise NotImplementedError
