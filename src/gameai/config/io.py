import abc
import dataclasses
import enum
import pathlib
from inspect import isclass, signature
from types import UnionType
from typing import Any, Type, TypeVar, Union, get_args, get_origin

import pygame
import yaml

CONF_DIR = pathlib.Path(__file__).parent / "settings"

ConfigurableT = TypeVar("ConfigurableT", bound="Configurable")
LoadableT = TypeVar("LoadableT", bound="Loadable")


# XXX: this whole module uses a lot of reflection magic
@dataclasses.dataclass
class Configurable:
    """Dataclass mixin to mark config objects as loadable from YAML"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def from_config(cls: Type[ConfigurableT], data: dict) -> ConfigurableT:
        cls_fields = {field for field in signature(cls).parameters}
        print("loading from config", cls, data)

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

    def _unmarshal_class(self, type_: type, value) -> Any:
        # decode logic for special case clases
        if issubclass(type_, enum.Enum):
            return type_(value)
        elif issubclass(type_, Configurable):
            return type_.from_config(value)
        elif type_ is pygame.font.Font:
            return pygame.font.SysFont(**value)
        return None


class Loadable(abc.ABC):

    settings_file: str
    # we could infer this from the constructor signature,
    # but it's more readable to define it explicitly
    settings_type: Type[Configurable]
    __loaded = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def load(cls: Type[LoadableT], *args, **kwargs) -> LoadableT:
        if cls.__name__ in Loadable.__loaded:
            return Loadable.__loaded[cls.__name__]
        settings = cls._load_settings()
        o = cls(*args, **kwargs, settings=settings)
        Loadable.__loaded[cls.__name__] = o
        return o

    @classmethod
    def _load_settings(cls) -> Configurable:
        filename = cls.settings_file
        if filename in Loadable.__loaded:
            return Loadable.__loaded[filename]

        try:
            with open(CONF_DIR / filename) as f:
                settings = yaml.safe_load(f)
                Loadable.__loaded[filename] = settings
                return cls.settings_type.from_config(settings)
        except yaml.YAMLError as e:
            # TODO: log yaml load error
            print(f"Failed to read YAML from {filename}: {e}")
        except IOError as e:
            print(f"IO error reading {filename}: {e}")

        raise pygame.error(f"Failed to read configuration from {filename}")
