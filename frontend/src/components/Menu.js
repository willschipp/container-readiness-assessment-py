import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Content,ListBox,Item,Heading } from '@adobe/react-spectrum';

function Menu() {

    const navigate = useNavigate();    

    const handleNavigation = (selected) => {
        var selection = [...selected][0];
        if (selection === 'newRequest') {
            navigate('/form');
        } else if (selection === 'allOrders') {
            navigate('/orders');
        } else if (selection === 'existingRequest') {
            navigate('/existing');
        } else {
            navigate('/');
        }
    }

    return (
        <Content margin="size-200">
            <Heading level={3}>
                Functions
            </Heading>
            <ListBox
                aria-label="Menu"
                selectionMode="single"
                onSelectionChange={handleNavigation}>
                <Item key="home">Home</Item>
                <Item key="newRequest">Create a New Request</Item>
                <Item key="existingRequest">View an existing Request</Item>
                <Item key="allOrders">View All Orders</Item>
            </ListBox>
        </Content>
    )
}


export default Menu;