
import requests

from datetime import datetime
from dm_nac_service.resource.generics import response_to_dict
from fastapi.responses import JSONResponse
from dm_nac_service.data.database import insert_logs
from dm_nac_service.commons import get_env_or_fail
from dm_nac_service.resource.generics import response_to_dict



NAC_SERVER = 'northernarc-server'


async def nac_collect(context, partner_cin, data):
    """ Generic Post Method for Collect API """
    try:
        data_dict = data.dict()
        validate_url = get_env_or_fail(NAC_SERVER, 'base-url', NAC_SERVER + ' base-url not configured')
        api_key = get_env_or_fail(NAC_SERVER, 'api-key', NAC_SERVER + ' api-key not configured')
        group_key = get_env_or_fail(NAC_SERVER, 'group-key', NAC_SERVER + ' group-key not configured')
        url = validate_url + f'/{context}/uploadCollectionJSON?partnerCIN={partner_cin}'
        
        str_url = str(url)
        headers = {
            "API-KEY": api_key,
            "GROUP-KEY": group_key,
            "Content-Type": "application/json",
            "Content-Length": "0",
            "User-Agent": 'My User Agent 1.0',
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        }
        
        collect_context_response = requests.post(url, json=data_dict, headers=headers)
        print(collect_context_response)
        
        collect_context_response_dict = response_to_dict(collect_context_response)
        print("DICT",collect_context_response_dict)

        # Fake Success Response to test
        # collect_context_response_dict = disbursement_request_success_response

        result = collect_context_response
        

    except Exception as e:
        log_id = await insert_logs('GATEWAY', 'NAC', 'nac_collect', collect_context_response_dict.status_code, collect_context_response_dict.content, datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at Northern Arc Post Method - {e.args[0]}"})

    return result

