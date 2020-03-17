import typing


class ServiceMetadata(typing.NamedTuple):
    name: str
    description: str
    parameters: dict
