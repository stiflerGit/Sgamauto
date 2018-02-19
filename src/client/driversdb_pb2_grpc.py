# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import driversdb_pb2 as driversdb__pb2


class InsuranceStub(object):
  """The Insurance Server collect data by all the devices of the drivers that stipulate the contract
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.InitDevice = channel.unary_unary(
        '/Insurance/InitDevice',
        request_serializer=driversdb__pb2.Targa.SerializeToString,
        response_deserializer=driversdb__pb2.Config.FromString,
        )
    self.Analize = channel.unary_unary(
        '/Insurance/Analize',
        request_serializer=driversdb__pb2.Test.SerializeToString,
        response_deserializer=driversdb__pb2.ACK.FromString,
        )


class InsuranceServicer(object):
  """The Insurance Server collect data by all the devices of the drivers that stipulate the contract
  """

  def InitDevice(self, request, context):
    """A client-to-server notification RPC

    Initial configuration for the device tied to a specific car
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Analize(self, request, context):
    """Send all data collected by an alcohol test and send an ACK to the client
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_InsuranceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'InitDevice': grpc.unary_unary_rpc_method_handler(
          servicer.InitDevice,
          request_deserializer=driversdb__pb2.Targa.FromString,
          response_serializer=driversdb__pb2.Config.SerializeToString,
      ),
      'Analize': grpc.unary_unary_rpc_method_handler(
          servicer.Analize,
          request_deserializer=driversdb__pb2.Test.FromString,
          response_serializer=driversdb__pb2.ACK.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'Insurance', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))