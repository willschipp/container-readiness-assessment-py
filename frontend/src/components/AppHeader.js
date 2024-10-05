import React from 'react';

import { Content, Header, Heading } from '@adobe/react-spectrum';

import DataCheck from '@spectrum-icons/workflow/DataCheck';

function AppHeader() {

    return (
        <Content margin="size-200">
            <Header>
                <Heading level={2}>
                    <DataCheck/>
                    &nbsp;
                    Container Readiness Assessment Platform
                </Heading>
            </Header>
        </Content>
    )
}

export default AppHeader;