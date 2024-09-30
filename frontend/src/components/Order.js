import React, { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

import { Content } from '@adobe/react-spectrum';

function Order() {
    const location = useLocation();
    const orderId = location.state?.orderId;
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
        } catch (e) {
            console.error(e);
        }
    }

    return (
        <Content>{result}</Content>
    )
}


export default Order;


//{JSON.stringify(data, null, 2)}