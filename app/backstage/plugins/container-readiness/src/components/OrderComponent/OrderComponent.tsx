import React, {useEffect, useState} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Typography, Grid, Button } from '@material-ui/core';
import {
  InfoCard,
  StructuredMetadataTable
} from '@backstage/core-components';
import { useApi } from '@backstage/core-plugin-api';
import { OrderApiRef } from '../../api';
import { orderRouteRef } from '../../routes';
import { useRouteRefParams } from '@backstage/core-plugin-api';

const useStyles = makeStyles({
  avatar: {
    height: 32,
    width: 32,
    borderRadius: '50%',
  },
});

type Order = {
    order_id: 0,
    app_id: "<none>",
    user_id: "<none>",
    job: {
      form: {
        app_language: "<none>"
      },
      result: -1
    },
    finished: true
  };

type MetadataOrder = {
    order_id: string,
    app_id: string,
    user_id: string,
    status: string,
    result: string
}

export const OrderComponent = () => {

    const apiClient = useApi(OrderApiRef);

    const [metadataOrder, setMetadataOrder] = useState<MetadataOrder>()

    const params = useRouteRefParams(orderRouteRef);

    const handleFiles = () => {

    }

    const handleAnswers = () => {
        
    }
    
    const handleBack = () => {
        
    }    

    const fetchData = async (order_id:string) => {
        const order = await apiClient.getOrder(order_id)
        //convert the order to a metadataOrder
        const metadataOrder: MetadataOrder = {
            order_id: order_id,
            app_id: order.app_id,
            user_id: order.user_id,
            status: (order.finished === true ? "Finished" : "Processing"),
            result: (order.job ? order.job.result === 1 ? "Container Ready" : order.job.result === 0 ? "Not Container Ready" : "Unknown" : "Unknown"),            
        }
        setMetadataOrder(metadataOrder)
    }    

    useEffect(() => {
        fetchData(params.order_id);
    },[]);

    return (
        <Grid item>
            <InfoCard title="Order">
                <StructuredMetadataTable metadata={metadataOrder}/>
                <Button variant="outlined" onClick={handleFiles}>
                    {/* <Download/> */}
                    <Typography>Download Files</Typography>
                </Button>
                <Button variant="outlined" onClick={handleAnswers}>
                    {/* <Download/> */}
                    <Typography>View Answers</Typography>
                </Button>                    
                <Button variant="outlined" onClick={handleBack}>
                    {/* <Back/> */}
                    <Typography>Back</Typography>
                </Button>
                <Button variant="outlined" onClick={() => {fetchData(params.order_id)}}>
                    {/* <Refresh/> */}
                    <Typography>Refresh</Typography>
                </Button>                                    
            </InfoCard>
        </Grid>        
    );
}