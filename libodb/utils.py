from functools import wraps
from typing import Any, Callable, Coroutine, ParamSpec, Type, TypeVar

from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)
P = ParamSpec("P")


def model(
    mod: Type[ModelType],
) -> Callable[
    [Callable[P, Coroutine[Any, Any, dict]]],
    Callable[P, Coroutine[Any, Any, ModelType]],
]:
    def decorator(
        func: Callable[..., Coroutine[Any, Any, dict]]
    ) -> Callable[..., Coroutine[Any, Any, ModelType]]:
        @wraps(func)
        async def wrapper(self, *args, **kwargs) -> ModelType:
            return mod(**await func(self, *args, **kwargs))

        return wrapper

    return decorator
