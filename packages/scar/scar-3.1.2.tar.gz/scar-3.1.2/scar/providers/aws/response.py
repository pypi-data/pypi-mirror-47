# Copyright (C) GRyCAP - I3M - UPV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from enum import Enum
from tabulate import tabulate
import json
import scar.logger as logger
import scar.utils as utils

class OutputType(Enum):
    PLAIN_TEXT = 1
    JSON = 2
    VERBOSE = 3
    BINARY = 4
    
def parse_http_response(response, function_name, asynch, output_type, output_file):
    if response.ok:
        if output_type == OutputType.BINARY:
            with open(output_file, "wb") as out:
                out.write(utils.decode_base64(response.text))
            text_message = "Output saved in file '{}'".format(output_file)
        else:
            text_message = "Request Id: {0}".format(response.headers['amz-lambda-request-id'])
            if asynch:
                text_message += "\nFunction '{0}' launched correctly".format(function_name)
            else:
                text_message += "\nLog Group Name: {0}\n".format(response.headers['amz-log-group-name']) 
                text_message += "Log Stream Name: {0}\n".format(response.headers['amz-log-stream-name'])
                text_message += json.loads(response.text)["udocker_output"]
    else:
        if asynch and response.status_code == 502:
            text_message = "Function '{0}' launched sucessfully.".format(function_name)
        else:
            error = json.loads(response.text)
            if 'message' in error:
                text_message = "Error ({0}): {1}".format(response.reason, error['message']) 
            else:
                text_message = "Error ({0}): {1}".format(response.reason, error['exception']) 
    logger.info(text_message)        
    
def _print_generic_response(response, output_type, aws_output, text_message=None, json_output=None, verbose_output=None, output_file=None):
    if output_type == OutputType.BINARY:
        with open(output_file, "wb") as out:
            out.write(utils.decode_base64(response['Payload']['body']))
    elif output_type == OutputType.PLAIN_TEXT:
        output = text_message
        logger.info(output)
    else:
        if output_type == OutputType.JSON:
            output = json_output if json_output else { aws_output : 
                                                      {'RequestId' : response['ResponseMetadata']['RequestId'],
                                                       'HTTPStatusCode' : response['ResponseMetadata']['HTTPStatusCode']}}         
        elif output_type == OutputType.VERBOSE:
            output = verbose_output if verbose_output else { aws_output : response }
        logger.info_json(output)

def parse_lambda_function_creation_response(response, function_name, access_key, output_type):
    if response:
        aws_output = 'LambdaOutput'
        text_message = "Function '%s' successfully created." % function_name
        json_message = { aws_output : {'AccessKey' : access_key,
                                        'FunctionArn' : response['FunctionArn'],
                                        'Timeout' : response['Timeout'],
                                        'MemorySize' : response['MemorySize'],
                                        'FunctionName' : response['FunctionName']}}
        _print_generic_response(response, output_type, aws_output, text_message, json_output=json_message)

def parse_log_group_creation_response(response, log_group_name, output_type):
    if response:
        text_message = "Log group '%s' successfully created." % log_group_name
        _print_generic_response(response, output_type, 'CloudWatchOutput', text_message)

def parse_delete_function_response(response, function_name, output_type):
    if response:
        text_message = "Function '%s' successfully deleted." % function_name
        _print_generic_response(response, output_type, 'LambdaOutput', text_message)

def parse_delete_log_response(response, log_group_name, output_type):
    if response:    
        text_message = "Log group '%s' successfully deleted." % log_group_name
        _print_generic_response(response, output_type, 'CloudWatchOutput', text_message)
    
def parse_delete_api_response(response, api_id, output_type):
    if response:
        text_message = "API Endpoint '%s' successfully deleted." % api_id
        _print_generic_response(response, output_type, 'APIGateway', text_message)      

def parse_ls_response(lambda_functions, output_type):
    aws_output = 'Functions'
    result = []
    text_message = ""
    if output_type == OutputType.VERBOSE:
        result = lambda_functions
    else:
        for _lambda in lambda_functions:
            result.append(_parse_lambda_function_info(_lambda))
        text_message = _get_table(result)    
    json_message = { aws_output : result }
    _print_generic_response('', output_type, aws_output, text_message, json_output=json_message, verbose_output=json_message)    
    

def _parse_lambda_function_info(function_info):
    name = function_info.get('FunctionName', "-")
    memory = function_info.get('MemorySize', "-")
    timeout = function_info.get('Timeout', "-")
    image_id = function_info['Environment']['Variables'].get('IMAGE_ID', "-")
    api_gateway = function_info['Environment']['Variables'].get('API_GATEWAY_ID', "-")
    if api_gateway != '-':
        region = function_info['FunctionArn'].split(':')[3]
        api_gateway = 'https://{0}.execute-api.{1}.amazonaws.com/scar/launch'.format(api_gateway, region)
    super_layer_arn = ['-']
    if 'Layers' in function_info:
        super_layer_arn = [":".join(layer['Arn'].split(":")[-2:]) for layer in function_info['Layers'] if 'faas-supervisor' in layer['Arn']]
        
    return {'Name' : name,
            'Memory' : memory,
            'Timeout' : timeout,
            'Image_id': image_id,
            'Api_gateway': api_gateway,
            'Sup_layer_arn': super_layer_arn[0]}
  
def _get_table(functions_info):
    headers = ['NAME', 'MEMORY', 'TIME', 'IMAGE_ID', 'API_URL', 'SUPERVISOR_LAYER_VERSION']
    table = []
    for function in functions_info:
        table.append([function['Name'],
                      function['Memory'],
                      function['Timeout'],
                      function['Image_id'],
                      function['Api_gateway'],
                      function['Sup_layer_arn']])
    return tabulate(table, headers)    

def _parse_error_invocation_response(response, function_name):
    if response:
        if "Task timed out" in response['Payload']:
            # Find the timeout time
            message = utils.find_expression(str(response['Payload']), '(Task timed out .* seconds)')
            # Modify the error message to ease the error readability
            error_msg = message.replace("Task", "Function '%s'" % function_name)
            error_log = "Error in function response: %s" % error_msg                
        else:
            error_msg = "Error in function response."
            error_log = "Error in function response: %s" % response['Payload']
        logger.error(error_msg, error_log)
        
def _parse_payload(value):
    if (('Payload' in value) and value['Payload']):
        payload = value['Payload'].read()
        if len(payload) > 0:
            value['Payload'] = json.loads(payload.decode("utf-8"))
    
def _parse_asynchronous_invocation_response(response, output_type, function_name):
    if response:
        aws_output = 'LambdaOutput'
        text_message = 'Request Id: %s\n' % response['ResponseMetadata']['RequestId']
        text_message += "Function '%s' launched correctly" % function_name
        json_message = { aws_output : {'StatusCode' : response['StatusCode'],
                                       'RequestId' : response['ResponseMetadata']['RequestId']}}        
        _print_generic_response(response, output_type, aws_output, text_message, json_output=json_message)
    
def _parse_requestresponse_invocation_response(**kwargs):
    if kwargs['Response']:
        response = kwargs['Response']
        aws_output = 'LambdaOutput'
        log_group_name = response['Payload']['headers']['amz-log-group-name']
        log_stream_name = response['Payload']['headers']['amz-log-stream-name']
        request_id = response['ResponseMetadata']['RequestId']
        if "exception" in response['Payload']['body']:
            body = "ERROR launching udocker container: \n {0}".format(json.loads(response['Payload']['body'])['exception'])
        else:
            body = utils.base64_to_utf8_string(response['Payload']['body'])
        
        text_message = 'Request Id: %s\n' % request_id
        text_message += 'Log Group Name: %s\n' % log_group_name
        text_message += 'Log Stream Name: %s\n' % log_stream_name
        text_message += body
        
        json_message = { aws_output : {'StatusCode' : response['StatusCode'],
                                       'Payload' : body,
                                       'LogGroupName' : log_group_name,
                                       'LogStreamName' : log_stream_name,
                                       'RequestId' : request_id}}
        if 'OutputFile' in kwargs and kwargs['OutputFile']:
            _print_generic_response(response, kwargs['OutputType'], aws_output, text_message, json_output=json_message, output_file=kwargs['OutputFile'])
        else:
            _print_generic_response(response, kwargs['OutputType'], aws_output, text_message, json_output=json_message)
      
def _parse_base64_response_values(value):
    value['LogResult'] = utils.base64_to_utf8_string(value['LogResult'])
    value['ResponseMetadata']['HTTPHeaders']['x-amz-log-result'] = utils.base64_to_utf8_string(value['ResponseMetadata']['HTTPHeaders']['x-amz-log-result'])

def parse_invocation_response(**kwargs):
    # Decode and parse the payload
    _parse_payload(kwargs['Response'])
    if "FunctionError" in kwargs['Response']:
        _parse_error_invocation_response(kwargs['Response'], kwargs['FunctionName'])
    if kwargs['IsAsynchronous']:        
        _parse_asynchronous_invocation_response(kwargs['Response'], kwargs['OutputType'], kwargs['FunctionName'])
    else:
        # Transform the base64 encoded results to something legible
        _parse_base64_response_values(kwargs['Response'])
        # Extract log_group_name and log_stream_name from the payload
        _parse_requestresponse_invocation_response(**kwargs)
        
