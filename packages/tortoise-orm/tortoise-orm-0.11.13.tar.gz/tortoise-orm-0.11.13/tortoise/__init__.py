import asyncio
import importlib
import json
import logging
import os
from copy import deepcopy
from inspect import isclass
from typing import Coroutine, Dict, List, Optional, Type, Union, cast  # noqa

from tortoise import fields
from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.backends.base.config_generator import expand_db_url, generate_config
from tortoise.exceptions import ConfigurationError  # noqa
from tortoise.fields import ManyToManyRelationManager  # noqa
from tortoise.filters import get_backward_fk_filters, get_m2m_filters
from tortoise.models import Model
from tortoise.queryset import QuerySet  # noqa
from tortoise.transactions import current_transaction_map
from tortoise.utils import generate_schema_for_client

try:
    from contextvars import ContextVar
except ImportError:
    from aiocontextvars import ContextVar  # type: ignore

logger = logging.getLogger("tortoise")


class Tortoise:
    apps = {}  # type: Dict[str, Dict[str, Type[Model]]]
    _connections = {}  # type: Dict[str, BaseDBAsyncClient]
    _inited = False  # type: bool

    @classmethod
    def get_connection(cls, connection_name: str) -> BaseDBAsyncClient:
        return cls._connections[connection_name]

    @classmethod
    def _init_relations(cls) -> None:
        for app_name, app in cls.apps.items():
            for model_name, model in app.items():
                if model._meta._inited:
                    continue
                else:
                    model._meta._inited = True
                if not model._meta.table:
                    model._meta.table = model.__name__.lower()

                for field in model._meta.fk_fields:
                    field_object = cast(fields.ForeignKeyField, model._meta.fields_map[field])
                    reference = field_object.model_name
                    related_app_name, related_model_name = reference.split(".")
                    related_model = cls.apps[related_app_name][related_model_name]
                    field_object.type = related_model
                    backward_relation_name = field_object.related_name
                    if not backward_relation_name:
                        backward_relation_name = "{}s".format(model._meta.table)
                    if backward_relation_name in related_model._meta.fields:
                        raise ConfigurationError(
                            'backward relation "{}" duplicates in model {}'.format(
                                backward_relation_name, related_model_name
                            )
                        )
                    fk_relation = fields.BackwardFKRelation(model, "{}_id".format(field))
                    setattr(related_model, backward_relation_name, fk_relation)
                    related_model._meta.filters.update(
                        get_backward_fk_filters(backward_relation_name, fk_relation)
                    )

                    related_model._meta.backward_fk_fields.add(backward_relation_name)
                    related_model._meta.fetch_fields.add(backward_relation_name)
                    related_model._meta.fields_map[backward_relation_name] = fk_relation
                    related_model._meta.fields.add(backward_relation_name)

                for field in model._meta.m2m_fields:
                    field_mobject = cast(fields.ManyToManyField, model._meta.fields_map[field])
                    if field_mobject._generated:
                        continue

                    backward_key = field_mobject.backward_key
                    if not backward_key:
                        backward_key = "{}_id".format(model._meta.table)
                        field_mobject.backward_key = backward_key

                    reference = field_mobject.model_name
                    related_app_name, related_model_name = reference.split(".")
                    related_model = cls.apps[related_app_name][related_model_name]

                    field_mobject.type = related_model

                    backward_relation_name = field_mobject.related_name
                    if not backward_relation_name:
                        backward_relation_name = field_mobject.related_name = "{}_through".format(
                            model._meta.table
                        )
                    if backward_relation_name in related_model._meta.fields:
                        raise ConfigurationError(
                            'backward relation "{}" duplicates in model {}'.format(
                                backward_relation_name, related_model_name
                            )
                        )

                    if not field_mobject.through:
                        related_model_table_name = (
                            related_model._meta.table
                            if related_model._meta.table
                            else related_model.__name__.lower()
                        )

                        field_mobject.through = "{}_{}".format(
                            model._meta.table, related_model_table_name
                        )

                    m2m_relation = fields.ManyToManyField(
                        "{}.{}".format(app_name, model_name),
                        field_mobject.through,
                        forward_key=field_mobject.backward_key,
                        backward_key=field_mobject.forward_key,
                        related_name=field,
                        type=model,
                    )
                    m2m_relation._generated = True
                    setattr(related_model, backward_relation_name, m2m_relation)
                    model._meta.filters.update(get_m2m_filters(field, field_mobject))
                    related_model._meta.filters.update(
                        get_m2m_filters(backward_relation_name, m2m_relation)
                    )
                    related_model._meta.m2m_fields.add(backward_relation_name)
                    related_model._meta.fetch_fields.add(backward_relation_name)
                    related_model._meta.fields_map[backward_relation_name] = m2m_relation
                    related_model._meta.fields.add(backward_relation_name)

    @classmethod
    def _discover_client_class(cls, engine: str) -> BaseDBAsyncClient:
        # Let exception bubble up for transparency
        engine_module = importlib.import_module(engine)

        try:
            client_class = engine_module.client_class  # type: ignore
        except AttributeError:
            raise ConfigurationError(
                'Backend for engine "{}" does not implement db client'.format(engine)
            )
        return client_class

    @classmethod
    def _discover_models(cls, models_path, app_label) -> List[Type[Model]]:
        try:
            module = importlib.import_module(models_path)
        except ImportError:
            raise ConfigurationError('Module "{}" not found'.format(models_path))
        discovered_models = []
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isclass(attr) and issubclass(attr, Model) and not attr._meta.abstract:
                if attr._meta.app and attr._meta.app != app_label:
                    continue
                attr._meta.app = app_label
                discovered_models.append(attr)
        return discovered_models

    @classmethod
    async def _init_connections(cls, connections_config: dict, create_db: bool) -> None:
        for name, info in connections_config.items():
            if isinstance(info, str):
                info = expand_db_url(info)
            client_class = cls._discover_client_class(info.get("engine"))
            db_params = deepcopy(info["credentials"])
            db_params.update({"connection_name": name})
            connection = client_class(**db_params)  # type: ignore
            if create_db:
                await connection.db_create()
            await connection.create_connection(with_db=True)
            cls._connections[name] = connection
            current_transaction_map[name] = ContextVar(name, default=connection)

    @classmethod
    def _init_apps(cls, apps_config: dict) -> None:
        for name, info in apps_config.items():
            try:
                cls.get_connection(info.get("default_connection", "default"))
            except KeyError:
                raise ConfigurationError(
                    'Unknown connection "{}" for app "{}"'.format(
                        info.get("default_connection", "default"), name
                    )
                )
            app_models = []  # type: List[Type[Model]]
            for module in info["models"]:
                app_models += cls._discover_models(module, name)

            models_map = {}
            for model in app_models:
                model._meta.default_connection = info.get("default_connection", "default")
                models_map[model.__name__] = model

            cls.apps[name] = models_map

        cls._init_relations()

        cls._build_initial_querysets()

    @classmethod
    def _get_config_from_config_file(cls, config_file: str) -> dict:
        _, extension = os.path.splitext(config_file)
        if extension in (".yml", ".yaml"):
            import yaml

            with open(config_file, "r") as f:
                config = yaml.safe_load(f)
        elif extension == ".json":
            with open(config_file, "r") as f:
                config = json.load(f)
        else:
            raise ConfigurationError(
                "Unknown config extension {}, only .yml and .json are supported".format(extension)
            )
        return config

    @classmethod
    def _build_initial_querysets(cls) -> None:
        for app in cls.apps.values():
            for model in app.values():
                model._meta.generate_filters()
                model._meta.basequery = model._meta.db.query_class.from_(model._meta.table)
                model._meta.basequery_all_fields = model._meta.basequery.select(
                    *model._meta.db_fields
                )

    @classmethod
    async def init(
        cls,
        config: Optional[dict] = None,
        config_file: Optional[str] = None,
        _create_db: bool = False,
        db_url: Optional[str] = None,
        modules: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        """
        Sets up Tortoise-ORM.

        You can configure using only one of ``config``, ``config_file``
        and ``(db_url, modules)``.

        Parameters
        ----------
        config:
            Dict containing config:

            Example
            -------

            .. code-block:: python3

                {
                    'connections': {
                        # Dict format for connection
                        'default': {
                            'engine': 'tortoise.backends.asyncpg',
                            'credentials': {
                                'host': 'localhost',
                                'port': '5432',
                                'user': 'tortoise',
                                'password': 'qwerty123',
                                'database': 'test',
                            }
                        },
                        # Using a DB_URL string
                        'default': 'postgres://postgres:@qwerty123localhost:5432/events'
                    },
                    'apps': {
                        'models': {
                            'models': ['__main__'],
                            # If no default_connection specified, defaults to 'default'
                            'default_connection': 'default',
                        }
                    }
                }

        config_file:
            Path to .json or .yml (if PyYAML installed) file containing config with
            same format as above.
        db_url:
            Use a DB_URL string. See :ref:`db_url`
        modules:
            Dictionary of ``key``: [``list_of_modules``] that defined "apps" and modules that
            should be discovered for models.
        _create_db:
            If ``True`` tries to create database for specified connections,
            could be used for testing purposes.

        Raises
        ------
        ConfigurationError
            For any configuration error
        """
        if cls._inited:
            await cls.close_connections()
            await cls._reset_apps()
        if int(bool(config) + bool(config_file) + bool(db_url)) != 1:
            raise ConfigurationError(
                'You should init either from "config", "config_file" or "db_url"'
            )

        if config_file:
            config = cls._get_config_from_config_file(config_file)

        if db_url:
            if not modules:
                raise ConfigurationError('You must specify "db_url" and "modules" together')
            config = generate_config(db_url, modules)

        try:
            connections_config = config["connections"]  # type: ignore
        except KeyError:
            raise ConfigurationError('Config must define "connections" section')

        try:
            apps_config = config["apps"]  # type: ignore
        except KeyError:
            raise ConfigurationError('Config must define "apps" section')

        logger.info(
            "Tortoise-ORM startup\n    connections: %s\n    apps: %s",
            str(connections_config),
            str(apps_config),
        )

        await cls._init_connections(connections_config, _create_db)
        cls._init_apps(apps_config)

        cls._inited = True

    @classmethod
    async def close_connections(cls) -> None:
        for connection in cls._connections.values():
            await connection.close()
        cls._connections = {}
        logger.info("Tortoise-ORM shutdown")

    @classmethod
    async def _reset_apps(cls) -> None:
        for app in cls.apps.values():
            for model in app.values():
                model._meta.default_connection = None
        cls.apps = {}
        current_transaction_map.clear()

    @classmethod
    async def generate_schemas(cls, safe=True) -> None:
        """
        Generate schemas according to models provided to ``.init()`` method.
        Will fail if schemas already exists, so it's not recommended to be used as part
        of application workflow

        Parameters
        ----------
        safe:
            When set to true, creates the table only when it does not already exist.
        """
        if not cls._inited:
            raise ConfigurationError("You have to call .init() first before generating schemas")
        for connection in cls._connections.values():
            await generate_schema_for_client(connection, safe)

    @classmethod
    async def _drop_databases(cls) -> None:
        """
        Tries to drop all databases provided in config passed to ``.init()`` method.
        Normally should be used only for testing purposes.
        """
        if not cls._inited:
            raise ConfigurationError("You have to call .init() first before deleting schemas")
        for connection in cls._connections.values():
            await connection.close()
            await connection.db_delete()
        cls._connections = {}
        await cls._reset_apps()


def run_async(coro: Coroutine) -> None:
    """
    Simple async runner that cleans up DB connections on exit.
    This is meant for simple scripts.

    Usage::

        from tortoise import Tortoise, run_async

        async def do_stuff():
            await Tortoise.init(
                db_url='sqlite://db.sqlite3',
                models={'models': ['app.models']}
            )

            ...

        run_async(do_stuff())
    """
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(coro)
    finally:
        loop.run_until_complete(Tortoise.close_connections())


__version__ = "0.11.13"
