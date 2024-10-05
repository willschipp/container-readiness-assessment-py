import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

import { Content, TableView, Column, Row, TableHeader, Cell, TableBody, Button, ButtonGroup, Text, View } from '@adobe/react-spectrum';
import Download from '@spectrum-icons/workflow/Download';

function Order() {
    const location = useLocation();
    const orderId = location.state?.orderId;
    const [data, setData] = useState([]);
    let result = '';

    const navigate = useNavigate();

    useEffect(() => {
        fetchData();
    });

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

    const handleFiles = (e) => {
        // navigate
        navigate('/files', { state: { orderId: orderId }});
    }

    return (

        <Content>
            <TableView aria-label="Order" width="calc(100% - size-1000)">
                <TableHeader>
                    <Column>Order ID</Column>
                    <Column>{data.order_id}</Column>
                </TableHeader>
                <TableBody>
                    <Row>
                        <Cell>App Id</Cell>
                        <Cell>{data.app_id}</Cell>
                    </Row>
                    <Row>
                        <Cell>User ID</Cell>
                        <Cell>{data.user_id}</Cell>
                    </Row>
                    <Row>
                        <Cell>App Language</Cell>
                        <Cell>{data.job ? data.job.form.app_language : ''}</Cell>
                    </Row>
                    <Row>
                        <Cell>Status</Cell>
                        <Cell>{data.finished === true ? (<span>Finished</span>) : (<span>Running</span>)}</Cell>
                    </Row>
                </TableBody>
            </TableView>
            <View>
                <ButtonGroup>
                    <Button variant="primary" onPress={handleFiles}>
                        <Download/>
                        <Text>Download Files</Text>
                    </Button>                
                </ButtonGroup>
            </View>
        </Content>
    )
}


export default Order;


//{JSON.stringify(data, null, 2)}