from abc import ABC, abstractmethod
from typing import Dict, Set
from queue import Queue

# least connection, round robin, etc... algorithms can be mentioned by client
# during initialisation


class RequestType:
    pass


class Request:
    id: str
    requestType: RequestType
    parameters: dict


class Destination:
    ipAddress: str
    requestsBeingServed: int
    threshold: int

    @classmethod
    def acceptRequest(cls, request: Request):
        if cls.threshold <= cls.requestsBeingServed:
            cls.requestsBeingServed += 1
            return True
        else:
            return False

    @classmethod
    def completeRequest(cls):
        cls.requestsBeingServed -= 1


class Service:

    name: str
    destinations: Set[Destination]

    @classmethod
    def addDestination(cls, destination: Destination):
        cls.destinations.add(destination)

    def removeDestination(cls, destination: Destination):
        cls.destinations.remove(destination)


class LoadBalancer(ABC):
    # Map<RequestType, Service> serviceMap
    serviceMap: Dict[RequestType, Service] = {}

    @classmethod
    def register(cls, requestType: RequestType, service: Service):
        cls.serviceMap[requestType] = service

    @classmethod
    def getDestinations(cls, request: Request):
        service: Service = cls.serviceMap.get(request.requestType)
        return service.destinations

    @abstractmethod
    def balanceLoad(self, request: Request):
        raise NotImplementedError()

class LeastConnectionLoadBalancer(LoadBalancer):

    def balanceLoad(cls, request: Request):
        d = cls.getDestinations(request)
        res = None
        for des in d:
            res = min(res, des.requestsBeingServed)
        return res

class RoutedLoadBalancer(LoadBalancer):

    def balanceLoad(cls, request: Request):
        destinations = cls.getDestinations(request)
        l = list(destinations)
        return l.pop(hash(request.id) % len(l))


class RoundRobinLoadBalancer(LoadBalancer):
    # Map<RequestType, Queue<Destination>> destinationsForRequest
    destinationsForRequest: Dict[RequestType, Queue[Destination]] = {}

    @classmethod
    def balanceLoad(cls, request: Request):
        if not cls.destinationsForRequest[request.requestType]:
            destinations = cls.getDestinations(request=request)
            cls.destinationsForRequest[request.requestType] = cls.cTq(destinations)
        destination = cls.destinationsForRequest.get(request.requestType).get()
        cls.destinationsForRequest.get(request.requestType).put(destination)
        return destination

    @classmethod
    def cTq(cls, destinations: Set[Queue]):
        return None



class LoadBalancerFactory:
    def createLoadBalancer(lbType: str):
        if lbType == "round-robin":
            return RoundRobinLoadBalancer()
        elif lbType == "least-connection":
            return RoundRobinLoadBalancer()
        else:
            return LeastConnectionLoadBalancer()
