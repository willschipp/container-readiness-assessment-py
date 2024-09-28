import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Content,ListBox,Item } from '@adobe/react-spectrum';

function Menu() {

    const navigate = useNavigate();    

    const handleNavigation = (selected) => {
        var selection = [...selected][0];
        if (selection == 'newRequest') {
            navigate('/form');
        } else {
            navigate('/existing');
        }
        // navigate('/form'); //nothing to pass
    }

    return (
        <div>
            <Content>Functions</Content>
            <ListBox
                aria-label="Menu"
                selectionMode="single"
                onSelectionChange={handleNavigation}>
                <Item key="newRequest">Create a New Request</Item>
                <Item key="existingRequest">View an existing Request</Item>
            </ListBox>
        </div>
    )
}


export default Menu;