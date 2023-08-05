import functools
import inspect
from typing import Dict, Type, Union, Any, TypeVar, Callable

from .exceptions import UnresolvableType
from .definitions import Resolver, Construction, Singleton, Alias, DEFINITION_TYPES

UNRESOLVABLE_TYPES = [str, int, float, bool]

X = TypeVar("X")


class Container:
    _registered_types: Dict[Type, Resolver] = {}

    def define(self, dep_type: Union[Type[X], Type], dep_resolver: Resolver) -> None:
        self._registered_types[dep_type] = dep_resolver

    def resolve(self, dep_type: Type[X], suppress_error=False) -> X:
        try:
            if dep_type in UNRESOLVABLE_TYPES:
                raise UnresolvableType(f"Cannot construct type {dep_type}")
            registered_type = self._registered_types.get(dep_type, dep_type)
            if isinstance(registered_type, Singleton):
                return self._load_singleton(registered_type)
            return self._build(registered_type)
        except UnresolvableType as inner_error:
            if not suppress_error:
                raise UnresolvableType(
                    f"Cannot construct type {dep_type.__name__}"
                ) from inner_error
            return None  # type: ignore

    def partial(self, func: Callable) -> Callable:
        spec = inspect.getfullargspec(func)
        bindable_deps = self._infer_dependencies(spec, suppress_error=True)
        return functools.partial(func, **bindable_deps)

    def __getitem__(self, dep: Type[X]) -> X:
        return self.resolve(dep)

    def __setitem__(self, dep: Type, resolver):
        if type(resolver) in DEFINITION_TYPES:
            return self.define(dep, resolver)
        if inspect.isfunction(resolver):
            return self.define(dep, Construction(resolver))
        if not inspect.isclass(resolver):
            return self.define(dep, Singleton(lambda: resolver))  # type: ignore
        return self.define(dep, Alias(resolver))

    def _build(self, dep_type: Any) -> Any:
        if isinstance(dep_type, Alias):
            return self.resolve(dep_type.alias_type)
        if isinstance(dep_type, Construction):
            return dep_type.construct()
        return self._reflection_build(dep_type)

    def _reflection_build(self, dep_type: Type[X]) -> X:
        spec = inspect.getfullargspec(dep_type.__init__)
        sub_deps = self._infer_dependencies(spec)
        return dep_type(**sub_deps)  # type: ignore

    def _infer_dependencies(self, spec: inspect.FullArgSpec, suppress_error=False):
        sub_deps = {
            key: self.resolve(sub_dep_type, suppress_error=suppress_error)
            for (key, sub_dep_type) in spec.annotations.items()
        }
        filtered_deps = {key: dep for (key, dep) in sub_deps.items() if dep is not None}
        return filtered_deps

    def _load_singleton(self, singleton: Singleton):
        if singleton.has_instance:
            return singleton.instance
        return singleton.set_instance(self._build(singleton.singleton_type))
