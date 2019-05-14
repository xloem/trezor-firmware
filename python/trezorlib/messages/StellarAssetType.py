# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p


class StellarAssetType(p.MessageType):

    def __init__(
        self,
        type: int = None,
        code: str = None,
        issuer: str = None,
    ) -> None:
        self.type = type
        self.code = code
        self.issuer = issuer

    @classmethod
    def get_fields(cls):
        return {
            1: ('type', p.UVarintType, 0),
            2: ('code', p.UnicodeType, 0),
            3: ('issuer', p.UnicodeType, 0),
        }
