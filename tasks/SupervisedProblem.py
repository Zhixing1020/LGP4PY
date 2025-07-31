

from abc import ABC, abstractmethod
from typing import List


class SupervisedProblem(ABC):
    @abstractmethod
    def getDatanum(self) -> int:
        pass

    @abstractmethod
    def getDatadim(self) -> int:
        pass

    @abstractmethod
    def getOutputnum(self) -> int:
        pass

    @abstractmethod
    def getOutputdim(self) -> int:
        pass

    @abstractmethod
    def getTargets(self) -> List[int]:
        pass

    @abstractmethod
    def getTargetNum(self) -> int:
        pass

    @abstractmethod
    def getDataMax(self) -> List[float]:
        pass

    @abstractmethod
    def getDataMin(self) -> List[float]:
        pass

    @abstractmethod
    def getData(self) -> List[List[float]]:
        pass

    @abstractmethod
    def getDataOutput(self) -> List[List[float]]:
        pass

    @abstractmethod
    def getX(self) -> List[float]:
        pass

    @abstractmethod
    def getX_index(self) -> int:
        pass

    @abstractmethod
    def setX_index(self, ind: int):
        pass

    @abstractmethod
    def istraining(self) -> bool:
        pass
