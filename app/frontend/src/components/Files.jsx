import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

import { Content, TableView, Column, Row, TableHeader, Cell, TableBody, Button, View, Well } from '@adobe/react-spectrum';
import Download from '@spectrum-icons/workflow/Download';
import ViewDetail from '@spectrum-icons/workflow/ViewDetail';

function Files() {

    const location = useLocation();
    const orderId = location.state?.orderId;
    const [data, setData] = useState([]);
    const [details, setDetails] = useState([]);
    let result = '';

    const navigate = useNavigate();

    const fetchData = async () => {
        try {
            //use the order id to retrieve
            const response = await fetch('/api/order/' + orderId.toString().trim() + '/files');
            if (!response.ok) {
                throw new Error(`http error! status: ${response.status}`);
            }
            result = await response.json();
            setData(result);
        } catch (e) {
            console.error(e);
        }
    }

    const handleView = async (orderId,filename) => {
        try {
            const response = await fetch('/api/order/' + orderId + '/file/' + filename + '/stream');
            if (!response.ok) {
                throw new Error(`http error! status: ${response.status}`);
            }
            // result = await response.json();
            // check content type
            const contentType = response.headers.get('content-type');
            const result = contentType?.includes('application/json')
                ? await response.json()
                : await response.text();            

            setDetails(result);
            console.log(result);
        } catch (error) {
            console.error(error);
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
                    {data.length > 0 ? 
                        (data.map((item,index) => (
                            <Row key={index}>
                                <Cell>
                                    {item}
                                </Cell>
                                <Cell>
                                    <Button onPress={() => handleView(orderId,item)}>
                                        <ViewDetail/>
                                    </Button>                                    
                                    &nbsp;&nbsp;
                                    <Button onPress={() => handleDownload(orderId,item)}>
                                        <Download/>
                                    </Button>
                                </Cell>
                            </Row>
                        ))) : (
                            <Row>
                                <Cell colSpan={2}>No files available</Cell>
                            </Row>
                        )
                    }
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
                        {/* {typeof details === 'string' ? details : JSON.stringify(details,null,2)} */}
                        {details}
                    </pre>
                </Well>
            </View>            
        </Content>
    )
}


export default Files;