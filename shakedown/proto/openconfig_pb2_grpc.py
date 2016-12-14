import grpc
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities

import openconfig_pb2 as openconfig__pb2
import openconfig_pb2 as openconfig__pb2
import openconfig_pb2 as openconfig__pb2
import openconfig_pb2 as openconfig__pb2
import openconfig_pb2 as openconfig__pb2
import openconfig_pb2 as openconfig__pb2
import openconfig_pb2 as openconfig__pb2
import openconfig_pb2 as openconfig__pb2


class OpenConfigStub(object):

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Get = channel.unary_unary(
        '/openconfig.OpenConfig/Get',
        request_serializer=openconfig__pb2.GetRequest.SerializeToString,
        response_deserializer=openconfig__pb2.GetResponse.FromString,
        )
    self.GetModels = channel.unary_unary(
        '/openconfig.OpenConfig/GetModels',
        request_serializer=openconfig__pb2.GetModelsRequest.SerializeToString,
        response_deserializer=openconfig__pb2.GetModelsResponse.FromString,
        )
    self.Set = channel.unary_unary(
        '/openconfig.OpenConfig/Set',
        request_serializer=openconfig__pb2.SetRequest.SerializeToString,
        response_deserializer=openconfig__pb2.SetResponse.FromString,
        )
    self.Subscribe = channel.stream_stream(
        '/openconfig.OpenConfig/Subscribe',
        request_serializer=openconfig__pb2.SubscribeRequest.SerializeToString,
        response_deserializer=openconfig__pb2.SubscribeResponse.FromString,
        )


class OpenConfigServicer(object):

  def Get(self, request, context):
    """Get requests a single snapshot of specified data.  A Get request may
    contain a hint that the request will be repeated (i.e., polling).
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetModels(self, request, context):
    """GetModels returns information about the YANG models supported by the
    target.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Set(self, request, context):
    """Set is the primary function for sending configuration data to the target.
    It sets the paths contained in the SetRequest to the specified values. If
    any of the paths are invalid, or are read-only, the SetResponse will
    return an error. All paths in the SetRequest must be valid or the entire
    request must be rejected. If a path specifies an internal node, rather than
    a leaf, then the value must be the values of the node's children encoded
    in JSON. Binary data in the tree must be base64 encoded, but if a path
    specifies a leaf of binary type, it may be sent as binary. See SetRequest
    for further explanation on the atomicity and idempotency of a Set
    operation.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Subscribe(self, request_iterator, context):
    """Subscribe subscribes for streaming updates.  Streaming updates are provided
    as a series of Notifications, each of which update a portion of the tree.
    The initial SubscribeRequest contains a SubscriptionList, described below.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_OpenConfigServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Get': grpc.unary_unary_rpc_method_handler(
          servicer.Get,
          request_deserializer=openconfig__pb2.GetRequest.FromString,
          response_serializer=openconfig__pb2.GetResponse.SerializeToString,
      ),
      'GetModels': grpc.unary_unary_rpc_method_handler(
          servicer.GetModels,
          request_deserializer=openconfig__pb2.GetModelsRequest.FromString,
          response_serializer=openconfig__pb2.GetModelsResponse.SerializeToString,
      ),
      'Set': grpc.unary_unary_rpc_method_handler(
          servicer.Set,
          request_deserializer=openconfig__pb2.SetRequest.FromString,
          response_serializer=openconfig__pb2.SetResponse.SerializeToString,
      ),
      'Subscribe': grpc.stream_stream_rpc_method_handler(
          servicer.Subscribe,
          request_deserializer=openconfig__pb2.SubscribeRequest.FromString,
          response_serializer=openconfig__pb2.SubscribeResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'openconfig.OpenConfig', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
