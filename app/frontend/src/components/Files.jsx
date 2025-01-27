import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';

import { Content, TableView, Column, Row, TableHeader, Cell, TableBody, Button } from '@adobe/react-spectrum';
import Download from '@spectrum-icons/workflow/Download';

function Files() {

    const location = useLocation();
    const orderId = location.state?.orderId;
    const [data, setData] = useState([]);
    let result = '';

    const fetchData = async () => {
        try {
            //use the order id to retrieve
            const response = await fetch('/api/order/' + orderId.trim() + '/files');
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
            const response = await axios.get('/api/download/' + orderId + '/' + filename, {
                responseType:'blob',
            });

            const blob = new Blob([response.data],{ type: response.headers['content-type']});

            const url = window.URL.createObjectURL(blob);

            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download',filename);

            document.body.appendChild(link);
            link.click();

            //clean up
            link.parentNode.removeChild(link);
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error(error);
        }
    }

    useEffect(() => {
        fetchData();
    });

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
                                    <Download/>
                                </Button>
                            </Cell>
                        </Row>
                    ))}
                </TableBody>
            </TableView>
        </Content>
    )
}


export default Files;