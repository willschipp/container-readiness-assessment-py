import json
import os
import tempfile


from ..model.order import Order
from ..model.job import Job
from ..model.form import Form
from ..model.encoder import Encoder

from ..service.s3 import list_files, get_file, get_buckets

from ..config import config
from ..logging_config import setup_logging

logger = setup_logging()

def get_job_by_order_id(order_id):
    # retrieve the job.json
    # check if there's a finished.json
    # return the files
    current_config = config[os.getenv('RUN_MODE','dev')]

    
    # get the files
    file_names = list_files(order_id,current_config.URL,current_config.KEY,current_config.SECRET)
    
    if len(file_names) <= 0:
        # no order id exists
        logger.error(f"no {order_id} exists")
        return
    
    # create object
    order = Order(
        user_id=None,
        app_id=None,
        order_id=order_id,
        job=None,
        files=[],
        finished=False
    )

    # finished = False
    for file_name in file_names:
        # first check for 'finished.json'
        if file_name == 'finished.json':
            # done
            order.finished = True    
        elif file_name == "job.json":
            continue
        else:       
            # don't add finished
            order.files.append(file_name)

    # retrieve the job.json and hydrate it
    with tempfile.NamedTemporaryFile(mode="w+",delete=False,suffix=".json") as temp_file:
        pass
    get_file(temp_file.name,order_id,"job.json",current_config.URL,current_config.KEY,current_config.SECRET)
    # read into json
    with open(temp_file.name,'r') as job_file:
        data = json.load(job_file)
    order.job = Job.from_dict(data)
    order.user_id = order.job.form.user_id
    order.app_id = order.job.form.app_id
    # clean up
    os.remove(temp_file.name)
    
    return order

def get_all_orders():
    orders = []
    # setup access
    current_config = config[os.getenv('RUN_MODE','dev')]
    bucket_names = get_buckets(current_config.URL,current_config.KEY,current_config.SECRET)
    for bucket_name in bucket_names:
        # have the order id --> for each bucket need to get the job.json
        order = get_job_by_order_id(bucket_name)
        orders.append(order)
    
    return orders