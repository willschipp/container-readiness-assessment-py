import React from 'react';
import { useNavigate } from 'react-router-dom';

import { Form, Button, TextField  } from '@adobe/react-spectrum';

function Existing() {

    let [orderId, setOrderId] = React.useState(' ');

    // const orderRef = React.useRef();

    const navigate = useNavigate();
  
    const handleSubmit = (e) => {
        e.preventDefault();        
        navigate('/order', { state: { orderId: orderId }});
    }

    return (
        <Form onSubmit={handleSubmit} maxWidth="size-5000">
            <TextField label="Order ID" value={orderId} onChange={setOrderId}/>
            <Button type="submit" maxWidth="size-1000">View</Button>
        </Form>
    )
}


export default Existing;