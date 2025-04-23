import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { Content, TableView, Column, Row, TableHeader, Cell, TableBody, Button, Text } from '@adobe/react-spectrum';
import ViewDetail from '@spectrum-icons/workflow/ViewDetail';
import CheckmarkCircleOutline from '@spectrum-icons/workflow/CheckmarkCircleOutline';
import CloseCircle from '@spectrum-icons/workflow/CloseCircle';
import Refresh from '@spectrum-icons/workflow/Refresh';
import SelectCircular from '@spectrum-icons/workflow/SelectCircular';

function Orders() {

    const [data, setData] = useState([
        {
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
          }]);

    const navigate = useNavigate();

    const fetchData = async () => {
        try {
            const response = await fetch('/api/order');
            if (!response.ok) {
                throw new Error(`http error! status: ${response.status}`);
            }
            // let result = await response.json();
            // setData(result);
            // console.log(result);

            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                const result = await response.json();
                setData(result);
                console.log(result);
            } else {
                console.log(response)
                throw new Error('Response is not JSON');
            }            
        }
        catch (e) {
            console.error(e);
        }
    }

    const handleViewOrder = (orderId) => {
        //build the navigate with the location
        navigate('/order', { state: { orderId: orderId }});
    }

    useEffect(() => {
        fetchData();
    },[]);    

    return (
        <Content width="calc(100% - size-1000)">
            <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 10 }}>
                
                <Button variant='primary' onPress={fetchData}>
                    <Refresh/>
                    <Text>Refresh</Text>
                </Button>
            </div>

            <TableView aria-label="Order">
                <TableHeader>
                    <Column allowsResizing>Order ID</Column>
                    <Column>App ID</Column>
                    <Column>User ID</Column>
                    <Column>Language</Column>
                    <Column>Status</Column>
                    <Column>Result</Column>
                    <Column>Action</Column>
                </TableHeader>
                <TableBody>
                    {data.map((item,index) => (
                        <Row key={index}>
                            <Cell>{item.order_id}</Cell>
                            <Cell>{item.app_id}</Cell>
                            <Cell>{item.user_id}</Cell>
                            <Cell>{item.job ? item.job.form.app_language : ''}</Cell>                            
                            <Cell>{item.finished === true ? (<span>Finished</span>) : (<span>Running</span>)}</Cell>
                            <Cell>{item.job.result === 1 ? (<span><CheckmarkCircleOutline/></span>) : item.job.result === 0 ? (<span><CloseCircle/></span>) : (<span><SelectCircular/></span>)}</Cell>
                            <Cell>
                                <Button variant="primary" onPress={() => handleViewOrder(item.order_id)}>
                                    <ViewDetail/>
                                </Button>
                            </Cell>
                        </Row>
                    ))}
                </TableBody>
            </TableView>
        </Content>
    )
}

export default Orders;