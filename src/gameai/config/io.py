import dataclasses
import enum
import pathlib
from inspect import isclass, signature
from types import UnionType
from typing import Any, Protocol, Type, TypeVar, Union, get_args, get_origin

import pygame
import yaml

RESOURCE_DIR = pathlib.Path(__file__).parent
SETTINGS_DIR = RESOURCE_DIR / "settings"
ASSETS_DIR = RESOURCE_DIR / "assets"

ConfigurableT_co = TypeVar("ConfigurableT_co", bound="Configurable")


# XXX: this whole module uses a lot of reflection magic
@dataclasses.dataclass
class Configurable:
    """Dataclass mixin to mark config objects as configurable from settings"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def from_config(cls: Type[ConfigurableT_co], data: dict) -> ConfigurableT_co:
        cls_fields = {field for field in signature(cls).parameters}

        data = data or {}
        defined_params, undefined_params = {}, {}
        for k, v in data.items():
            if k in cls_fields:
                defined_params[k] = v
            else:
                undefined_params[k] = v

        o = cls(**defined_params)

        for k, v in undefined_params.items():
            setattr(o, k, v)

        o._unmarshal_complex_types()
        return o

    def _unmarshal_complex_types(self) -> None:
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            unmarshalled_value = self._unmarshal_field(field.type, value)
            setattr(self, field.name, unmarshalled_value)

    def _unmarshal_field(self, type_, value) -> Any:
        if value is None:
            return None

        if isinstance(value, Configurable):
            # if the value is already a Loadable type
            # instance, no need to continue
            return value
        elif get_origin(type_) in (Union, UnionType):
            for t in get_args(type_):
                if isclass(t):
                    o = self._unmarshal_class(t, value)
                    if o is not None:
                        return o
        elif isclass(type_):
            instance = self._unmarshal_class(type_, value)
            if instance is not None:
                return instance

        if isinstance(value, list):
            # if the value is a list, expect the field type to be List[T]
            type_ = type_.__args__[0]
            return list(self._unmarshal_field(type_, o) for o in value)
        elif isinstance(value, dict):
            if hasattr(type_, "__args__") and len(type_.__args__) == 2:
                return {
                    k: self._unmarshal_field(type_.__args__[1], v)
                    for k, v in value.items()
                }
            else:
                return {k: v for k, v in value.items()}
        return value

    def _unmarshal_class(self, type_: type, value: Any) -> Any:
        # decode logic for special case clases
        if issubclass(type_, enum.Enum):
            return type_(value)
        elif issubclass(type_, Configurable):
            return type_.from_config(value)
        elif type_ is pygame.font.Font:
            return pygame.font.SysFont(**value)
        elif type_ is pygame.Surface:
            return pygame.image.load(ASSETS_DIR / value)
        return None


# pyright (and thus pylance) has a strict approach to abstract property types,
# (see discussion in https://github.com/microsoft/pyright/issues/2678)
# so instead of making Loadable an ABC with abstract properties, define a
# generic Protocol that Loadable subclasses must adhere to
class SupportsLoad(Protocol[ConfigurableT_co]):
    settings_file: str
    settings_type: Type[ConfigurableT_co]

    def __init__(self, settings: ConfigurableT_co, *args, **kwargs) -> None: ...

    @classmethod
    def _load_settings(cls) -> ConfigurableT_co: ...


# define a type where upper bound is a SupportsLoad subtype (eg. Game) that
# expects a concrete Configurable subtype (eg. GameSettings) to reference below
LoadableT = TypeVar("LoadableT", bound=SupportsLoad[Configurable])


class Loadable:
    """Mixin to mark scenes as loadable from YAML"""

    __loaded = {}

    # needed for mixin as otherwise we may have super() conflicts with
    # subclasses that also inherit from another parent
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def load(cls: Type[LoadableT], *args, **kwargs) -> LoadableT:
        """Loads referencing class from settings file

        Passes arguments to the class constructor.
        Caches classes and files so they are only loaded once.
        """
        # XXX: this works well for singleton classes like menus, but there may
        # be future classes that require a new instance on load()
        if cls.__name__ in Loadable.__loaded:
            return Loadable.__loaded[cls.__name__]

        settings = cls._load_settings()
        o = cls(*args, **kwargs, settings=settings)
        Loadable.__loaded[cls.__name__] = o
        return o

    @classmethod
    def _load_settings(cls: Type[LoadableT]) -> Configurable:
        filename = cls.settings_file
        # cache the settings file - useful for future objects that
        # may load multiple instances from the same settings
        if filename in Loadable.__loaded:
            return Loadable.__loaded[filename]

        try:
            with open(SETTINGS_DIR / filename) as f:
                settings = yaml.safe_load(f)
                Loadable.__loaded[filename] = settings
                return cls.settings_type.from_config(settings)
        except yaml.YAMLError as e:
            # TODO: log yaml load error
            print(f"Failed to read YAML from {filename}: {e}")
        except IOError as e:
            print(f"IO error reading {filename}: {e}")

        raise pygame.error(f"Failed to read configuration from {filename}")
