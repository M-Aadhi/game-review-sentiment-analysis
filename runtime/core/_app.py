"""
This module provides the core runtime app.
"""
import json
import os
import sys
import importlib.util
from typing import Optional, Dict
from traceback import format_exc

from . import _const, _exception, _utils, _ctx
from ._logger import get_sys_logger, get_user_logger, init_logger
from ._model import InvokeRequest, InvokeResponse, Args, ResponseBody, RunType


def trim_path(user_func_path: str) -> str:
    """
    Trims the given user_func_path by removing leading slashes 
    and replacing remaining slashes with dots.

    Args:
        user_func_path (str): The user_func_path to be trimmed.

    Returns:
        str: The trimmed user_func_path.
    """
    if user_func_path.startswith('/'):
        user_func_path = user_func_path.replace('/', '', 1)
    return user_func_path

def serialize_obj(obj):
    """
    Generic function to convert an object into a JSON serializable format.
    """
    if isinstance(obj, dict):
        return {k: serialize_obj(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_obj(x) for x in obj]
    elif isinstance(obj, tuple):
        return tuple(serialize_obj(x) for x in obj)
    elif hasattr(obj, "__dict__"):
        return serialize_obj(vars(obj))
    else:
        return obj

class Route:
    """
    Represents a route object.

    Attributes:
        route (str): The route.
        file (str): The file.
        user_function (object): The user function.
    """
    route: str
    file: str
    module_name: object
    user_function: object

    def __init__(self, route: str = '', file: str = '') -> None:
        self.route = trim_path(route)
        self.module_name = _const.MOUDLE_PREFIX + self.route.replace('/', '.')
        self.file = file
        self.user_function = None

    def invoke(self, args: Args):
        """
        Invokes the user function with the provided parameters and context.

        Args:
            input (Any): The parameters to be passed to the user function.
                        context (Any): The context object or data associated with the invocation.

        Returns:
            any: The response data returned by the user function.
        """
        if self.user_function is None:
            try:
                _ctx.get_stopwatch().fn_load_start()
                self.user_function = self.load_func_module()
            except Exception as e:
                raise e
            finally:
                _ctx.get_stopwatch().fn_load_end()

        try:
            _ctx.get_stopwatch().fn_run_start()
            data = self.user_function(args)
        except Exception as e:
            raise _exception.FunctionExecutionError(
                f'UserFuncExecErr: {e}\n{_utils.format_user_exception(2)}')
        finally:
            _ctx.get_stopwatch().fn_run_end()
        return data

    def load_func_module(self):
        """
        Loads the user function module.

        Returns:
            object: The user function module.
        """
        try:
            spec = importlib.util.spec_from_file_location(
                self.module_name, self.file)
            func_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(func_module)
        except ModuleNotFoundError as e:
            raise _exception.FunctionNotFoundError(
                f'ModuleNotFoundError: {self.module_name} {e}')
        except Exception as e:
            raise _exception.FunctionNotFoundError(
                f'SyntaxError: {self.module_name} {e}')

        try:
            user_func = func_module.handler
        except AttributeError as e:
            raise _exception.FunctionExecutionError(
                f'missing handler as entry for function({self.route})') from e

        if user_func is None:
            raise _exception.FunctionExecutionError(
                f'missing handler as entry for function({self.route})')
        elif not callable(user_func):
            raise _exception.FunctionExecutionError(
                f'handler should be as function type for function({self.route})')
        return user_func


class App:
    """
    Represents an app object.

    Attributes:
        project_path (str): The path to the project.
    """
    project_path: str
    manifest_content: str
    route_map: Dict[str, Route]
    run_type: RunType

    def __init__(self, project_path: str, run_type: RunType = RunType.PROXY) -> None:
        self.project_path = project_path
        self.route_map = {}
        self.manifest_content = ''
        self.run_type = run_type

    def init_project(self) -> None:
        """
        Initializes the project.

        Args:
            project_path (str): The path to the project.
        """

        _utils.Stopwatch.project_init_start()
        init_logger(self.run_type)
        get_sys_logger().info("project path: %s", self.project_path)

        _utils.set_functions_dir_path(
            os.path.join(self.project_path, _const.API_DIR_NAME))

        sys.path.append(os.path.join(
            self.project_path, _const.PYTHON_LIB_NAME))
        sys.path.append(os.path.join(self.project_path))

        self._load_manifest(self.project_path)
        _utils.Stopwatch.project_init_end()

    def _load_manifest(self, project_path: str) -> None:
        """
        Loads the manifest file.

        Args:
            project_path (str): The path to the project.
        """

        manifest_path = os.path.join(project_path, _const.FILE_MANIFEST)
        if os.path.exists(manifest_path) is False:
            get_sys_logger().info('%s not found', _const.FILE_MANIFEST)
            return
        try:
            with open(manifest_path, encoding="utf-8") as file:
                self.manifest_content = file.read()

            # 解析为 JSON
            json_data = json.loads(self.manifest_content)

            # 访问 JSON 数据
            apis = json_data.get(_const.MANIFEST_KEY_API, [])
            if isinstance(apis, list):
                for api in apis:
                    file = os.path.join(
                        project_path, api.get(_const.MANIFEST_KEY_FILE))
                    route = Route(
                        api.get(_const.MANIFEST_KEY_ROUTE), file)
                    self.route_map[route.route] = route
                    get_sys_logger().info('load manifest %s %s',
                                          route.route, route.file)
            else:
                get_sys_logger().info("apis is not list")
        except Exception as e:
            get_sys_logger().error('load manifest error %s', e)

    def _build_args(self, body: Optional[str]) -> Args:
        """
        Build the Args object from the provided invoke request.

        Args:
            invoke_request (InvokeRequest): The invoke request object.

        Returns:
            Args: The Args object containing the parameters and context from the invoke request.

        """
        args = Args()
        args.logger = get_user_logger()
        if body is None:
            return args

        body_dict = json.loads(body)
        input = body_dict.get('input', None)
        if isinstance(input, str):
            try:
                input = json.loads(input)
            except ValueError as e:
                get_sys_logger().info(e)
        input = _utils.dict_to_namespace(input)

        args.input = input
        return args

    def _parse_headers(self, headers: dict):
        """
        parse the headers object from the provided invoke request headers.

        Args:
            headers (dict): The invoke request headers.
        """
        try:
            if headers is not None and isinstance(headers, dict):
                _ctx.set_request_id(headers.get(
                    _const.HTTP_HEADER_X_RUNTIME_REQUEST_ID))

                if _const.HTTP_HEADER_X_RUNTIME_EVENT in headers:
                    runtime_event = json.loads(headers.get(
                        _const.HTTP_HEADER_X_RUNTIME_EVENT))
                    _ctx.add_ctx_key(
                        _const.CTX_KEY_RUNTIME_EVENT, runtime_event)
        except ValueError as e:
            get_sys_logger().error(e)

    def _invoke(self, user_func_path: str, args: Args):
        """
        Invokes the user function with the provided parameters and context.

        Args:
            input (Any): The parameters to be passed to the user function.
            context (Any): The context object or data associated with the invocation.

        Returns:
            any: The response data returned by the user function.
        """
        get_sys_logger().info('invoke %s', user_func_path)

        user_func_path = trim_path(user_func_path)
        route = self.route_map.get(user_func_path)
        if route is None:
            raise _exception.FunctionNotFoundError(
                f'function({user_func_path}) is not found')
        return route.invoke(args)

    def entry_handler(self, invoke_request: InvokeRequest) -> InvokeResponse:
        """
        Handles an invoke request.

        Args:
            request (InvokeRequest): The invoke request.

        Returns:
            InvokeResponse: The invoke response.
        """
        _ctx.init()
        user_func_path = invoke_request.url
        if user_func_path == _const.PATH_MANIFEST:
            _ctx.get_stopwatch().fn_end()
            headers = _ctx.get_stopwatch().to_time_headers()
            _ctx.clear()
            resp = InvokeResponse(body=self.manifest_content, headers=headers)
            return resp
        body = ResponseBody()
        try:
            args = self._build_args(invoke_request.body)
            self._parse_headers(invoke_request.headers)
            body.data = json.dumps(self._invoke(user_func_path, args), default=serialize_obj)
        except _exception.BaseError as e:
            get_user_logger().error('user error %s %s', user_func_path, format_exc())
            body.error(e)
        except Exception as e:
            get_sys_logger().error('SysErr %s %s', user_func_path, format_exc())
            body.error(_exception.RuntimeSystemError(
                f'SysErr: {e}'))
        finally:
            _ctx.get_stopwatch().fn_end()
            headers = _ctx.get_stopwatch().to_time_headers()
            _ctx.clear()
            resp = InvokeResponse(body=body.to_json(), headers=headers)
        return resp
