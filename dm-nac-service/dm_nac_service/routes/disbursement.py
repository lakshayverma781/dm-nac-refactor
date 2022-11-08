

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from datetime import datetime

from dm_nac_service.gateway.nac_disbursement import nac_disbursement
from dm_nac_service.data.database import get_database
from dm_nac_service.resource.log_config import logger
from dm_nac_service.resource.generics import hanlde_response_body, hanlde_response_status

# from dm_nac_service.app_responses.disbursement import disbursement_request_success_response, disbursement_request_error_response1, disbursement_request_error_response2, disbursement_request_error_response3, disbursement_status_success_response1, disbursement_status_success_response2, disbursement_status_error_response1, disbursement_status_error_response2, disbursement_status_error_response3


from dm_nac_service.data.disbursement_model import (
    disbursement,
    
)

from dm_nac_service.data.sanction_model import (
sanction
)

router = APIRouter()


@router.post("/find-customer-sanction", tags=["Sanction"])
async def find_customer_sanction(
        loan_id
):
    """post method for find_customer_sanction"""
    """ fetch customer_id and sanctionrefid from sanction table"""
    try:
        database = get_database()
        select_query = sanction.select().where(sanction.c.loan_id == loan_id).order_by(sanction.c.id.desc())
        raw_sanction = await database.fetch_one(select_query)
        sanction_dict = {
            "customerId": raw_sanction[1],
            "sanctionRefId": raw_sanction[2]
        }
        
        result = JSONResponse(status_code=200, content=sanction_dict)
    except Exception as e:
        logger.exception(f"Issue with find_dedupe function, {e.args[0]}")
        
        db_log_error = {"error": 'DB', "error_description": 'Dedupe Reference ID not found in DB'}
        result = JSONResponse(status_code=500, content=db_log_error)
    return result


@router.post("/disbursement", tags=["Disbursement"])
async def create_disbursement(
    
    disbursement_data
    
):
    """post method for create sanction"""
    """send disbursement data into northern_arc endpoint """
    """get response from nac_disbursement and insert data into disbursement table"""
    try:
        database = get_database()
        disbursement_data_dict = disbursement_data
        disbursement_response = await nac_disbursement('disbursement', disbursement_data_dict)
        logger.info(f'1 -Disbursement Data from Perdix and Sending the data to create disbursement function, {disbursement_data_dict}')
        disbursement_response_status = hanlde_response_status(disbursement_response)
        disbursement_response_body = hanlde_response_body(disbursement_response)

        disbursement_response_content_status = disbursement_response_body['content']['status']
        disbursement_response_message = disbursement_response_body['content']['message']
        
        
        if(disbursement_response_status == 200):
            
            
            store_record_time = datetime.now()
            disbursement_info = {
                'customer_id': disbursement_data_dict['customerId'],
                'originator_id': disbursement_data_dict['originatorId'],
                'sanction_reference_id': disbursement_data_dict['sanctionReferenceId'],
                'requested_amount': disbursement_data_dict['requestedAmount'],
                'ifsc_code': disbursement_data_dict['ifscCode'],
                'branch_name': disbursement_data_dict['branchName'],
                'processing_fees': disbursement_data_dict['processingFees'],
                'insurance_amount': disbursement_data_dict['insuranceAmount'],
                'disbursement_date': disbursement_data_dict['disbursementDate'],
                'created_date': store_record_time,
            }
           
            disbursement_info['message'] = disbursement_response_message
            disbursement_info['status'] = disbursement_response_content_status
            disbursement_info['disbursement_reference_id'] = disbursement_response_body['content']['value']['disbursementReferenceId']
            insert_query = disbursement.insert().values(disbursement_info)
            disbursement_id = await database.execute(insert_query)
            result = JSONResponse(status_code=200, content=disbursement_response_body)
            
        else:
            logger.error(f"failed inside create disbursement, {disbursement_response_message}")
            result = JSONResponse(status_code=500, content=disbursement_response_body)
            
    except Exception as e:
        logger.exception(f"Issue with find_dedupe function, {e.args[0]}")
        result = JSONResponse(status_code=500, content={"message": f"Issue with Northern Arc API, {e.args[0]}"})
    return result
