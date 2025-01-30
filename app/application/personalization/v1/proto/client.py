import grpc

from app.application.personalization.v1.proto.embedding_pb2_grpc import (
    EmbeddingServiceStub,
)
from app.core.configs import config


def get_embedding_channel_stub():
    channel = grpc.aio.insecure_channel(config.EMBEDDING_GRPC_URL)
    stub = EmbeddingServiceStub(channel)

    return channel, stub
