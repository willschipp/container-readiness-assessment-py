import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { Content, TableView, Column, Row, TableHeader, Cell, TableBody, Button } from '@adobe/react-spectrum';
import ViewDetail from '@spectrum-icons/workflow/ViewDetail';

function Orders() {

    const [data, setData] = useState([]);

    const navigate = useNavigate();

    const fetchData = async () => {
        try {
            const response = await fetch('/api/order');
            if (!response.ok) {
                throw new Error(`http error! status: ${response.status}`);
            }
            let result = await response.json();
            setData(result);
            console.log(result);
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
        <Content>
            <TableView aria-label="Order" width="calc(100% - size-1000)">
                <TableHeader>
                    <Column allowsResizing>Order ID</Column>
                    <Column>App ID</Column>
                    <Column>User ID</Column>
                    <Column>Language</Column>
                    <Column>Status</Column>
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