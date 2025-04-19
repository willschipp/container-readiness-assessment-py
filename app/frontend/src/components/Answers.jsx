import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';

import { Content, TableView, Column, Row, TableHeader, Cell, TableBody, Button, View, Well } from '@adobe/react-spectrum';
import ViewDetail from '@spectrum-icons/workflow/ViewDetail';

function Answers() {

    const location = useLocation();
    const orderId = location.state?.orderId;
    const [data, setData] = useState([]);
    const [details, setDetails] = useState([]);
    let result = '';

    const navigate = useNavigate();

    const fetchData = async () => {
        try {
            //use the order id to retrieve
            const response = await fetch('/api/order/' + orderId.toString().trim() + '/answer');
            if (!response.ok) {
                throw new Error(`http error! status: ${response.status}`);
            }
            result = await response.json();
            setData(result);
        } catch (e) {
            console.error(e);
        }
    }

    const handleDownload = async (orderId,filename) => {
        try {
            const response = await fetch('/api/order/' + orderId + '/answer/' + filename);
            if (!response.ok) {
                throw new Error(`http error! status: ${response.status}`);
            }
            result = await response.json();
            setDetails(result);
        } catch (error) {
            console.error(error);
        }
    }

    const handleViewOrder = () => {
        //build the navigate with the location
        navigate('/order', { state: { orderId: orderId }});
    }

    useEffect(() => {
        fetchData();
    },[]);

    return (
        <Content>                        
            <TableView width="calc(100% - size-1000)">
                <TableHeader>
                    <Column>Order ID</Column>
                    <Column>
                        <Button variant="secondary" alignSelf="end" onPress={handleViewOrder}>{orderId}</Button>
                    </Column>
                </TableHeader>
                <TableBody>
                    { data.length > 0 ?
                        (data.map((item,index) => (
                            <Row key={index}>
                                <Cell>
                                    {item}
                                </Cell>
                                <Cell>
                                    <Button onPress={() => handleDownload(orderId,item)}>
                                        <ViewDetail/>
                                    </Button>
                                </Cell>
                            </Row>
                        ))) : (
                            <Row>
                                <Cell colSpan={2}>No answers available</Cell>
                            </Row>
                        )}
                </TableBody>
            </TableView>
            <View>
                <Well marginTop="size-100">
                    <pre style={{
                        whiteSpace:'pre-wrap',
                        margin: 0,
                        fontFamily: 'monospace',
                        maxHeight: '500px',
                        overflow: 'auto'
                    }}>
                        {JSON.stringify(details,null,2)}
                    </pre>
                </Well>
            </View>            
        </Content>
    )
}

export default Answers;