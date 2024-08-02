"""
Lambda Runtime handler
"""
import json
import os
from runtime.core import App, InvokeRequest, RunType


app = App(os.getcwd(), RunType.AWS)
app.init_project()


def handler(event, context):
    """
    Lambda handler

    Args:
        event (dict): The event data passed to the Lambda function.
        context (LambdaContext): The context object passed to the Lambda function.

    Returns:
        dict: The response data returned by the Lambda function.
    """
    event = json.loads(event.get('body'))
    invoke_request = InvokeRequest(version=event.get('version'), protocol=event.get('protocol'),
                                   method=event.get('method'), url=event.get('url'), headers=event.get('headers'),
                                   body=event.get('body'), is_base64_encoded=event.get('isBase64Encoded'))
    invoke_response = app.entry_handler(invoke_request)
    return invoke_response.to_dict()
