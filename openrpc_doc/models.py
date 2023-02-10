"""
https://spec.open-rpc.org/#introduction
"""

import dataclasses
from collections.abc import Mapping
from typing import NewType, Literal, Any

SimVer = NewType('SimVer', str)
Url = NewType('Url', str)
Email = NewType('Email', str)

RuntimeExpression = str
"""https://spec.open-rpc.org/#runtime-expression"""
Schema = dict

Ignored = None


class Contact:
    name: str | Ignored = Ignored
    url: str | Ignored = Ignored
    email: Email | Ignored = Ignored


class License:
    name: str
    url: Url | Ignored = Ignored


@dataclasses.dataclass
class Info:
    title: str
    version: str
    description: str | Ignored = Ignored
    terms_of_service: str | Ignored = Ignored
    contact: Contact | Ignored = Ignored
    license: License | Ignored = Ignored


@dataclasses.dataclass
class ServerVariable:
    default: str
    enum: list[str] | Ignored = Ignored
    description: str | Ignored = Ignored


@dataclasses.dataclass
class Server:
    name: str
    url: RuntimeExpression
    summary: str | Ignored = Ignored
    description: str | Ignored = Ignored
    variables: Mapping[str, ServerVariable] | Ignored = Ignored


@dataclasses.dataclass
class ContentDescriptor:
    name: str
    schema: Schema
    summary: str | Ignored = Ignored
    description: str | Ignored = Ignored
    required: bool | False = False  # do not render
    deprecated: bool | False = False


@dataclasses.dataclass
class Reference:
    ref: str


@dataclasses.dataclass
class ExternalDocumentation:
    url: Url
    description: str | Ignored = Ignored


@dataclasses.dataclass
class Tag:
    name: str
    summary: str | Ignored = Ignored
    description: str | Ignored = Ignored
    external_docs: ExternalDocumentation | Ignored = Ignored


@dataclasses.dataclass
class Error:
    """https://spec.open-rpc.org/#error-object"""
    code: int  # must be specified
    message: str
    data: Any | Ignored = Ignored


@dataclasses.dataclass
class Link:
    """https://spec.open-rpc.org/#link-object"""
    name: str
    summary: str | Ignored = Ignored
    description: str | Ignored = Ignored
    method: str | Ignored = Ignored  # must be one of Method
    params: Mapping[str, Any | RuntimeExpression] | Ignored = Ignored
    server: Server | Ignored = Ignored


class Example:
    ...


@dataclasses.dataclass
class ExamplePairing:
    name: str | Ignored = Ignored
    summary: str | Ignored = Ignored
    description: str | Ignored = Ignored
    value: Any | Ignored = Ignored  # wtf
    externalValue: Url | Ignored = Ignored  # mutually exclusive with value


@dataclasses.dataclass
class Method:
    name: str
    params: list[ContentDescriptor | Reference]
    tags: list[Tag | Reference] | Ignored = Ignored
    summary: str | Ignored = Ignored
    description: str | Ignored = Ignored
    external_docs: ExternalDocumentation | Ignored = Ignored
    result: ContentDescriptor | Ignored = Ignored
    deprecated: bool | False = False  # do not render if false
    servers: list[Server] | Ignored = Ignored
    errors: list[Error | Reference] | Ignored = Ignored
    links: list[Link | Reference] | Ignored = Ignored
    param_structure: Literal['by-name', 'by-position', 'either'] = 'either'  # do not render
    examples: list[ExamplePairing] | Ignored = Ignored


@dataclasses.dataclass
class Components:
    content_descriptors: Mapping[str, ContentDescriptor] | Ignored = Ignored
    schemas: Mapping[str, Schema] | Ignored = Ignored
    examples: Mapping[str, Example] | Ignored = Ignored
    links: Mapping[str, Link] | Ignored = Ignored
    errors: Mapping[str, Error] | Ignored = Ignored
    example_pairing: Mapping[str, ExamplePairing] | Ignored = Ignored
    tags: Mapping[str, Tag] | Ignored = Ignored


@dataclasses.dataclass
class OpenRPC:
    info: Info
    methods: list[Method | Reference]
    openrpc: SimVer = SimVer('1.3.1')
    servers: list[Server] | Ignored = Ignored
    components: list[Components] | Ignored = Ignored
    external_docs: list[ExternalDocumentation] | Ignored = Ignored
