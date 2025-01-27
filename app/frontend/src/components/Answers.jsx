import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';

import { Content, TableView, Column, Row, TableHeader, Cell, TableBody, Button, View, Text } from '@adobe/react-spectrum';
import ViewDetail from '@spectrum-icons/workflow/ViewDetail';

function Answers() {

    const location = useLocation();
    const orderId = location.state?.orderId;
    const [data, setData] = useState([]);
    const [details, setDetails] = useState([]);
    let result = '';

    const fetchData = async () => {
        try {
            //use the order id to retrieve
            const response = await fetch('/api/order/' + orderId.trim() + '/answer');
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

    const handleDownload = async (orderId,filename) => {
        try {
            const response = await fetch('/api/order/' + orderId + '/answer/' + filename);
            if (!response.ok) {
                throw new Error(`http error! status: ${response.status}`);
            }
            result = await response.json();
            setDetails(result);
            console.log(result);
        } catch (error) {
            console.error(error);
        }
    }

    useEffect(() => {
        fetchData();
    },[]);

    return (
        <Content>                        
            <TableView width="calc(100% - size-1000)">
                <TableHeader>
                    <Column>Order ID</Column>
                    <Column>{orderId}</Column>
                </TableHeader>
                <TableBody>
                    {data.map((item,index) => (
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
                    ))}
                </TableBody>
            </TableView>
            <View>
                <Text>{JSON.stringify(details,null,2)}</Text>
            </View>            
        </Content>
    )
}

export default Answers;