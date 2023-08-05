import logging
from collections import Callable
from typing import List, Any, Optional

import attr

from perestroika.db_layers import DbLayer, DjangoDbLayer
from perestroika.deserializers import Deserializer, DjangoDeserializer
from perestroika.exceptions import RestException, BadRequest, InternalServerError
from perestroika.serializers import Serializer, DjangoSerializer
from perestroika.validators import DenyAll

logger = logging.getLogger(__name__)


@attr.s(auto_attribs=True)
class Method:
    mode: str = 'django'

    query: Any = None
    queryset: Any = None
    db_layer: Optional[DbLayer] = None

    serializer: Optional[Serializer] = None
    deserializer: Optional[Deserializer] = None

    skip_query_db: bool = False
    count_total: bool = False

    input_validator: Callable = DenyAll
    output_validator: Callable = DenyAll

    pre_query_hooks: List[Callable] = attr.Factory(list)
    post_query_hooks: List[Callable] = attr.Factory(list)

    request_hooks: List[Callable] = attr.Factory(list)
    response_hooks: List[Callable] = attr.Factory(list)

    def __attrs_post_init__(self):
        need_fields = []

        if self.mode == 'django':
            need_fields = ['queryset']

            if not self.db_layer:
                self.db_layer = DjangoDbLayer()

            if not self.serializer:
                self.serializer = DjangoSerializer()

            if not self.deserializer:
                self.deserializer = DjangoDeserializer()

        for field in need_fields:
            if getattr(self, field) is None and not self.skip_query_db:
                raise ValueError(f"Empty `{field}` is allowed only for resources with `skip_query_db` == True")

    def __set_name__(self, owner, name):
        if not hasattr(owner, 'methods') or not owner.methods:
            setattr(owner, 'methods', {})

        owner.methods[self.__class__.__name__.lower()] = self

    def schema(self):
        return {
            "output_schema": repr(self.output_validator)
        }

    def get_client_data(self, request, **kwargs):
        return self.deserializer.deserialize(request, self, **kwargs)

    def query_db(self, bundle):
        raise NotImplementedError()

    @staticmethod
    def validate(validator, bundle, validation_exception_class=RestException):
        _errors = []
        _objects = []

        for _object in bundle["items"]:
            try:
                _object = validator(_object)
                _objects.append(_object)
            except Exception as e:
                _desc = {
                    "data": _object,
                    "error": e
                }
                _errors.append(e)

        if _errors:
            raise validation_exception_class(message="Wrong data", errors=_errors)

        bundle["items"] = _objects

    def validate_input(self, bundle):
        self.validate(self.input_validator, bundle, validation_exception_class=BadRequest)

    def validate_output(self, bundle):
        self.validate(self.output_validator, bundle, validation_exception_class=InternalServerError)

    @staticmethod
    def apply_hooks(hooks, request, bundle):
        for hook in hooks:
            hook(request, bundle)

    def apply_pre_query_hooks(self, request, bundle):
        self.apply_hooks(self.pre_query_hooks, request, bundle)

    def apply_post_query_hooks(self, request, bundle):
        self.apply_hooks(self.post_query_hooks, request, bundle)

    def set_default_success_code(self, bundle):
        raise NotImplementedError()

    def apply_request_hooks(self, request, bundle):
        self.apply_hooks(self.request_hooks, request, bundle)

    def apply_response_hooks(self, request, bundle):
        self.apply_hooks(self.response_hooks, request, bundle)

    def handle(self, request, **kwargs):
        bundle = self.get_client_data(request, **kwargs)

        self.set_default_success_code(bundle)
        self.apply_request_hooks(request, bundle)
        self.validate_input(bundle)
        self.apply_pre_query_hooks(request, bundle)

        if not self.skip_query_db:
            self.query_db(bundle)

        self.apply_post_query_hooks(request, bundle)
        self.validate_output(bundle)
        self.apply_response_hooks(request, bundle)

        return self.serializer.serialize(request, bundle)


@attr.s(auto_attribs=True)
class CanFilterAndExclude(Method):
    filter_validator: Callable = DenyAll
    exclude_validator: Callable = DenyAll

    def set_default_success_code(self, bundle):
        raise NotImplementedError()

    def query_db(self, bundle):
        raise NotImplementedError()

    def schema(self):
        _schema = super().schema()
        _schema["filter_schema"] = repr(self.filter_validator)
        _schema["exclude_schema"] = repr(self.exclude_validator)
        return _schema


@attr.s(auto_attribs=True)
class NoBodyNoObjectsNoInput(CanFilterAndExclude):
    def set_default_success_code(self, bundle):
        raise NotImplementedError()

    def validate_input(self, bundle):
        """ Void validation because no input data"""
        pass

    def query_db(self, bundle):
        raise NotImplementedError()


@attr.s(auto_attribs=True)
class Get(NoBodyNoObjectsNoInput):
    def query_db(self, bundle):
        self.db_layer.get(bundle, self)

    def set_default_success_code(self, bundle):
        bundle["status_code"] = 200


@attr.s(auto_attribs=True)
class Post(Method):
    input_validator: Callable = DenyAll

    def query_db(self, bundle):
        self.db_layer.post(bundle, self)

    def schema(self):
        _schema = super().schema()
        _schema["input_schema"] = repr(self.input_validator)
        return _schema

    def set_default_success_code(self, bundle):
        bundle["status_code"] = 201


@attr.s(auto_attribs=True)
class Put(CanFilterAndExclude):
    def query_db(self, bundle):
        self.db_layer.put(bundle, self)

    input_validator: Callable = DenyAll

    def set_default_success_code(self, bundle):
        bundle["status_code"] = 200

    def schema(self):
        _schema = super().schema()
        _schema["input_schema"] = repr(self.input_validator)
        return _schema


@attr.s(auto_attribs=True)
class Delete(NoBodyNoObjectsNoInput):
    def query_db(self, bundle):
        raise NotImplementedError()

    def set_default_success_code(self, bundle):
        raise NotImplementedError()
