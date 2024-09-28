import React from 'react';

import { Form, Button, TextField  } from '@adobe/react-spectrum';

function Existing() {

    const handleSubmit = (e) => {
        e.preventDefault();
    }

    return (
        <Form onSubmit={handleSubmit} maxWidth="size-5000">
            <TextField label="Order ID"/>
            <Button type="submit" maxWidth="size-1000">View</Button>
        </Form>
    )
}


export default Existing;