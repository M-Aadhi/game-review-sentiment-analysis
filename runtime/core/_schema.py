"""
This module provides api to generate JSON Schema from function handler
"""
import os
import sys
import logging
from typing import Optional, TypedDict, Mapping, Any, get_origin

import docstring_parser

from apischema import schema, settings
from apischema.json_schema import deserialization_schema, JsonSchemaVersion
from apischema.schemas import Schema
from apischema.type_names import get_type_name

from runtime.core._utils import import_module_from_file

logger = logging.getLogger('cli')

class FunctionSchema(TypedDict, total=False):
    name: str
    description: str
    input: Mapping[str, Any]
    output: Mapping[str, Any]
    error: str

def handle_nullable(schema: dict[str, Any]):
    schema_type = schema.get("type")
    if type(schema_type) is list:
        if len(schema_type) == 2 and "null" in schema_type:
            # type: ["any", "null"] -> type: "any"
            origin_type = schema_type.pop(0)
            schema.pop("type")
            schema.setdefault("type", origin_type)
            schema.setdefault("nullable", True)
            schema_type = origin_type
        else:
            # Not supported union type yet
            raise Exception(f"Invalid schema union type {schema_type}")
    if schema_type == "object":
        # remove nullable field in properties requied
        properties: dict = schema.get("properties", {})
        required: list = schema.get("required", [])
        for key in properties.keys():
            prop: dict = properties.get(key, {})
            if "nullable" in prop:
                if prop.get("nullable") and key in required:
                    required.remove(key)

def type_base_schema(tp: Any) -> Optional[Schema]:
    if not hasattr(tp, "__doc__"):
        return None
    return schema(
        title=get_type_name(tp).json_schema,
        description=docstring_parser.parse(tp.__doc__).short_description,
        extra=handle_nullable
    )

def field_base_schema(tp: Any, name: str, alias: str) -> Optional[Schema]:
    title = alias.replace("_", " ").capitalize()
    tp = get_origin(tp) or tp  # tp can be generic
    for meta in docstring_parser.parse(tp.__doc__).meta:
        if meta.args == ["var", name]:
            return schema(title=title, description=meta.description)
    return schema(title=title)

settings.base_schema.type = type_base_schema
settings.base_schema.field = field_base_schema


def process_file(file_path: str, only_input: bool = False) -> FunctionSchema:
    result: FunctionSchema = {}
    try:
        # replace file_path to underscored
        function_name = os.path.splitext(os.path.normpath(file_path))[0].replace(os.path.sep, '_')
        result["name"] = function_name

        # import module
        function_module = import_module_from_file(function_name, file_path)

        # parse description from handler docstring
        result["description"] = docstring_parser.parse(function_module.handler.__doc__).short_description or f"function {function_name}"

        # generate json schema by apischema
        input_schema = deserialization_schema(function_module.Input, version=JsonSchemaVersion.DRAFT_7)
        output_schema = deserialization_schema(function_module.Output, version=JsonSchemaVersion.DRAFT_7)

        result["input"] = postprocess_schema(input_schema)
        if only_input:
            return result

        result["output"] = postprocess_schema(output_schema)
    except Exception as e:
        result["error"] = str(e)
        logger.error('Generate schema for %s failed: %s', file_path, e)
    return result

def postprocess_schema(schema: Mapping[str, Any]) -> Mapping[str, Any]:
    schema_dict = dict(schema)
    if "$schema" in schema_dict:
        schema_dict.pop("$schema")
    if "definitions" in schema_dict:
        definitions = schema_dict.get("definitions", {})
        raise Exception(f"Not supported recursive type ref yet, include: {definitions.keys()}")
    return schema_dict
