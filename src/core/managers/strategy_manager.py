import uuid
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
from typing import Callable
import inspect
from core.exceptions.http_exceptions import BuildException
from core.settings import settings

STRATEGY_FUNCTION_NAME = 'strategy'


class StrategyManager:
    @staticmethod
    def get_function(
        file_uuid: uuid.UUID, path: Path
    ) -> Callable[[dict, dict], dict]:
        spec = spec_from_file_location(f"{file_uuid}.py", path)

        if not Path(spec.origin).exists():
            raise BuildException(
                detail=f"No file with given file ID (name) : {file_uuid}"
            )

        module = module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, STRATEGY_FUNCTION_NAME):
            raise BuildException(
                detail=f"No <{STRATEGY_FUNCTION_NAME}> function in file"
            )

        func: Callable = getattr(module, STRATEGY_FUNCTION_NAME)
        return func

    @staticmethod
    def validate_function(func: Callable[[dict, dict], dict]) -> bool:

        if not inspect.isfunction(func):
            raise BuildException(detail="Your feature is not callable")

        signature = inspect.signature(func)
        parameters = signature.parameters.values()
        if len(parameters) != 2:
            raise BuildException(
                detail=f"The function must accept the variables '{settings.strategy_manager.data}: pd.Dataframe' and '{settings.strategy_manager.params}: dict'",
            )

        for param in zip(
            (settings.strategy_manager.data, settings.strategy_manager.params),
            parameters,
        ):
            if str(param[0]) != str(param[1]):
                raise BuildException(
                    detail=f"Unexpected argument <{param[1]}>. Expected: <{param[0]}>"
                )
        return True

    @staticmethod
    def execute(func: Callable[[dict, dict], dict],
                data: dict, params: dict):
        try:
            result = func(data, params)
            if not isinstance(result, list):
                raise BuildException(
                    detail=f"Unexpected return value: {type(result)}. Expected: <list>"
                )
        except BuildException as e:
            raise e
        except Exception as e:
            raise BuildException from e

        return result

