import json
import os
import tempfile
from loguru import logger

from server.model.order import Order
from server.model.job import Job

import server.constants as constants

from server.service.s3 import list_files, get_file, list_folders, list_files_in_folder


def get_job_by_order_id(order_id):
    # retrieve the job.json
    # check if there's a finished.json
    # return the files
    file_names = list_files_in_folder(order_id)
    if len(file_names) <= 0:
        logger.error(f"Order id {order_id} not found")
        return
    # create an order object
    order = Order(
        user_id=None,
        app_id=None,
        order_id=order_id,
        job=None,
        files=[],
        finished=False
    )
    for file_name in file_names:
        if file_name == constants.FILE_NAME_FINISHED:
            order.finished = True
        elif file_name == constants.FILE_NAME_JOB:
            continue
        else:
            order.files.append(file_name)
    #retrieve
    try:
        with tempfile.NamedTemporaryFile(
            mode="w+",delete=False,suffix=".json"
        ) as temp_file:
            pass
        
        get_file(order_id + "/" + constants.FILE_NAME_JOB,temp_file.name)

        with open(temp_file.name,"r") as job_file:
            data = json.load(job_file)

        order.job = Job.from_dict(data)
        order.user_id = order.job.form.user_id
        order.app_id = order.job.form.app_id

        os.remove(temp_file.name)
        return order
    except Exception as err:
        logger.error(err)
        return None

def get_all_orders():
    orders = []
    # setup access
    try:
        order_ids = list_folders()
        logger.debug(f"number of order_ids = {len(order_ids)}")
        for order_id in order_ids:
            order = get_job_by_order_id(order_id)
            if order is None:
                logger.info(f"Order order_id {order_id} not found")
            else:
                orders.append(order)
    except Exception as err:
        logger.error(err)
              
    return orders