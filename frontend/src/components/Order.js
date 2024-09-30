import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';

import { Content, TableView, Column, Row, TableHeader, Cell, TableBody } from '@adobe/react-spectrum';

function Order() {
    const location = useLocation();
    const orderId = location.state?.orderId;
    const [data, setData] = useState([]);
    let result = '';


    useEffect(() => {
        fetchData();
    },[]);

    const fetchData = async () => {
        try {
            //use the order id to retrieve
            const response = await fetch('/api/order/' + orderId.trim());
            if (!response.ok) {
                throw new Error(`http error! status: ${response.status}`);
            }
            result = await response.json();
            setData(result);
            console.log(result);
        } catch (e) {
            console.error(e);
        }
    }

    return (

        <div>
            <Content>Order</Content>
            <TableView aria-label="Order">
                <TableHeader>
                    <Column>Order ID</Column>
                    <Column>App ID</Column>
                    <Column>User ID</Column>
                    <Column>Language</Column>
                    <Column>Status</Column>
                </TableHeader>
                <TableBody>
                    <Row>
                        <Cell>{data.order_id}</Cell>
                        <Cell>{data.app_id}</Cell>
                        <Cell>{data.user_id}</Cell>
                        <Cell>{data.job.form.app_language}</Cell>
                        <Cell>{data.finished === true ? (<span>Finished</span>) : (<span>Running</span>)}</Cell>
                    </Row>
                </TableBody>
            </TableView>
        </div>
    )
}


export default Order;


//{JSON.stringify(data, null, 2)}