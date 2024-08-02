"""
VeFaaS handler
"""
import os
import json
from runtime.core import App, InvokeRequest, RunType

app = App(os.getcwd(), RunType.VEFAAS)
app.init_project()


def handler(event, context):
    """
    VeFaaS handler

    Args:
        event (dict): The event data passed to the Lambda function.
        context (VeFaaSContext): The context object passed to the VeFaaS function.
    """
    event = json.loads(event.get('body'))
    invoke_request = InvokeRequest(version=event.get('version'), protocol=event.get('protocol'),
                                   method=event.get('method'), url=event.get('url'), headers=event.get('headers'),
                                   body=event.get('body'), is_base64_encoded=event.get('isBase64Encoded'))
    invoke_response = app.entry_handler(invoke_request)
    return invoke_response.to_http_resp()
