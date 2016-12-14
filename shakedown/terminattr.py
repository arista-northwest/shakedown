#!/usr/bin/env python3

import grpc
import sys
import shakedown.proto.openconfig_pb2 as pb

class Client(object):

    def __init__(self, addr, timeout=300):
        self._channel = grpc.insecure_channel(addr)
        self._stub = pb.OpenConfigStub(self._channel)
        self._timeout = timeout

    def _to_ocpath(self, path):
        elements = path.split('/')
        return pb.Path(element=elements)

    def get(self, path):
        path = self._to_ocpath(path)
        request = pb.GetRequest(path=[path])
        return self._stub.Get(request, self._timeout)

    def subscribe(self, paths):

        requests = []
        for path in paths:
            path = self._to_ocpath(path)
            subscription = pb.Subscription(path=path)
            subscription = pb.SubscriptionList(subscription=[subscription])
            requests.append(pb.SubscribeRequest(subscribe=subscription))

        for response in self._stub.Subscribe(requests, self._timeout):
            yield response

if __name__ == "__main__":
    client = Client(sys.argv[1])
    for response in client.subscribe(sys.argv[2:]):
        print(response)
