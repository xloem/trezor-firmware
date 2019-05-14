# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p


class MoneroAccountPublicAddress(p.MessageType):

    def __init__(
        self,
        spend_public_key: bytes = None,
        view_public_key: bytes = None,
    ) -> None:
        self.spend_public_key = spend_public_key
        self.view_public_key = view_public_key

    @classmethod
    def get_fields(cls):
        return {
            1: ('spend_public_key', p.BytesType, 0),
            2: ('view_public_key', p.BytesType, 0),
        }
