import os
import requests
from datetime import datetime
import time
from dm_nac_service.resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from dm_nac_service.data.database import insert_logs
from dm_nac_service.commons import get_env_or_fail
from dm_nac_service.resource.generics import response_to_dict
from dm_nac_service.resource.log_config import logger
import json
from dm_nac_service.app_responses.sanction import sanction_response_success_data, sanction_response_error_data, sanction_status_response_not_found, sanction_status_response_in_progress, sanction_status_response_eligible, sanction_status_response_rejected_bureau, sanction_status_response_rejected_bre, sanction_status_response_rejected_server


NAC_SERVER = 'northernarc-server'


async def nac_sanction(context, data):
    """ Generic Post Method for sanction """
    """get data from perdix and post into northern_arc sanction endpoint"""
    try:
        validate_url = get_env_or_fail(NAC_SERVER, 'base-url', NAC_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(NAC_SERVER, 'api-key', NAC_SERVER + ' api-key not configured')
        group_key = get_env_or_fail(NAC_SERVER, 'group-key', NAC_SERVER + ' group-key not configured')
        originator_id = get_env_or_fail(NAC_SERVER, 'originator-id', NAC_SERVER + 'originator ID not configured')
        sector_id = get_env_or_fail(NAC_SERVER, 'sector-id', NAC_SERVER + 'Sector ID not configured')
        url = validate_url + f'/po/{context}?originatorId={originator_id}&sectorId={sector_id}'
       
        str_url = str(url)
       
        headers = {
            "API-KEY": api_key,
            "GROUP-KEY": group_key,
            "Content-Type": "application/json",
            "Content-Length": "0",
            "User-Agent": 'My User Agent 1.0',
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        
        sanction_context_response = requests.post(url, json=data, headers=headers)
        sanction_context_response_dict = response_to_dict(sanction_context_response)
        if (sanction_context_response.status_code == 200):
            log_id = await insert_logs(str_url, 'NAC', str(data), sanction_context_response.status_code,
                                       sanction_context_response.content, datetime.now())
            response_content = sanction_context_response.content

            res = json.loads(response_content.decode('utf-8'))
            log_id = await insert_logs(str_url, 'NAC', str(data), sanction_context_response.status_code,
                                       sanction_context_response.content, datetime.now())
            result = JSONResponse(status_code=200, content=sanction_context_response_dict)
        else:
            log_id = await insert_logs(str_url, 'NAC', str(data), sanction_context_response.status_code,
                                       sanction_context_response.content, datetime.now())

            result = JSONResponse(status_code=500, content=sanction_context_response_dict)
       
       
    except Exception as e:
        logger.exception(f"Issue with nac_sanction function, {e.args[0]}")
        result = JSONResponse(status_code=500,content={"message": f"Error Occurred at Northern Arc Post Method - {e.args[0]}"})

    return result


async def nac_sanction_fileupload(context, data):
    """genric post method for fileupload"""
    try:
        validate_url = get_env_or_fail(NAC_SERVER, 'base-url', NAC_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(NAC_SERVER, 'api-key', NAC_SERVER + ' api-key not configured')
        group_key = get_env_or_fail(NAC_SERVER, 'group-key', NAC_SERVER + ' group-key not configured')
        originator_id = get_env_or_fail(NAC_SERVER, 'originator-id', NAC_SERVER + 'originator ID not configured')
        sector_id = get_env_or_fail(NAC_SERVER, 'sector-id', NAC_SERVER + 'Sector ID not configured')
        url = validate_url + f'/po/{context}?originatorId={originator_id}&sectorId={sector_id}'
       
        str_url = str(url)
       
    except Exception as e:
        log_id = await insert_logs('GATEWAY', 'NAC', 'nac_sanction_fileupload', {e.args[0]},
                                   '', datetime.now())
        result = JSONResponse(status_code=500,
                              content={"message": f"Error Occurred at Northern Arc Post Method - {e.args[0]}"})


async def nac_get_sanction(context, customer_id):
    try:
        """genric post method for get sanction details"""
        validate_url = get_env_or_fail(NAC_SERVER, 'base-url', NAC_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(NAC_SERVER, 'api-key', NAC_SERVER + ' api-key not configured')
        group_key = get_env_or_fail(NAC_SERVER, 'group-key', NAC_SERVER + ' group-key not configured')
        originator_id = get_env_or_fail(NAC_SERVER, 'originator-id', NAC_SERVER + 'originator ID not configured')
        url = validate_url + f'/po/{context}?originatorId={originator_id}&customerId={customer_id}'
        str_url = str(url)
        headers = {
            "API-KEY": api_key,
            "GROUP-KEY": group_key,
            "Content-Type": "application/json",
            "Content-Length": "0",
            "User-Agent": 'My User Agent 1.0',
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "accept": "*/*"
        }
        sanction_get_response = requests.get(url, headers=headers)

        sanction_get_context_response_dict = response_to_dict(sanction_get_response)
        # Below are the fake resonses
        # sanction_get_context_response_dict = sanction_status_response_not_found
        # sanction_get_context_response_dict = sanction_status_response_in_progress
        sanction_get_context_response_dict = sanction_status_response_eligible
        # sanction_get_context_response_dict = sanction_status_response_rejected_bureau
        # sanction_get_context_response_dict = sanction_status_response_rejected_bre
        # sanction_get_context_response_dict = sanction_status_response_rejected_server
        if (sanction_get_response.status_code == 200):
            log_id = await insert_logs(str_url, 'NAC', str(customer_id), sanction_get_response.status_code,
                                       sanction_get_response.content, datetime.now())
            result = JSONResponse(status_code=200, content=sanction_get_context_response_dict)
        else:
            log_id = await insert_logs(str_url, 'NAC', str(customer_id), sanction_get_response.status_code,
                                       sanction_get_response.content, datetime.now())

            result = JSONResponse(status_code=200, content=sanction_get_context_response_dict)
    except Exception as e:
        logger.exception(f"Issue with nac_sanction function, {e.args[0]}")
        result = JSONResponse(status_code=500,
                              content={"message": f"Error Occurred at Northern Arc Post Method - {e.args[0]}"})
    return result


async def upload_file_to_nac(context, file_name, file_type, customer_id,flag=False):
    try:
        """genric post method for file_upload"""
        validate_url = get_env_or_fail(NAC_SERVER, 'base-url', NAC_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(NAC_SERVER, 'api-key', NAC_SERVER + ' api-key not configured')
        group_key = get_env_or_fail(NAC_SERVER, 'group-key', NAC_SERVER + ' group-key not configured')
        originator_id = get_env_or_fail(NAC_SERVER, 'originator-id', NAC_SERVER + 'originator ID not configured')
        url = validate_url + f'/po/{context}?originatorId={originator_id}&fileType={file_type}&customerId={customer_id}'
        str_url = str(url)
        headers = {
            "API-KEY": api_key,
            "GROUP-KEY": group_key,
            "Content-Type": "application/json",
            "Content-Length": "0",
            "User-Agent": 'My User Agent 1.0',
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "accept": "*/*"
        }
        file_path = os.path.abspath(('./static/'))
        file_to_upload = file_path + '/' + file_name
        logger.info(f'file_to_upload, {file_to_upload}')
        files = {'upload_file': open(file_to_upload, 'rb')}
        upload_file = requests.post(url, headers, files=files)
        if(upload_file.status_code == 200):
            flag=True
            logger.info(f'UPLOAD FILE RESPONSE , {upload_file.status_code}, {upload_file.content}')
            upload_file_message = json.loads(upload_file.content.decode('utf-8'))
            result = JSONResponse(status_code=200, content={"message": file_name})
            
            result = JSONResponse(status_code=200, content=upload_file_message)
        else:
            upload_file_message = upload_file.content.decode('utf-8')
            logger.info(f'UPLOAD FILE RESPONSE , {upload_file.status_code}, {upload_file.content}')
            result = JSONResponse(status_code=500, content=upload_file_message)
    except Exception as e:
        logger.exception(f"{datetime.now()} - Issue with upload_file_to_nac function, {e.args[0]}")
        result = JSONResponse(status_code=500,
                              content={"message": f"Error Occurred at Northern Arc Post Method - {e.args[0]}"})
    return result


