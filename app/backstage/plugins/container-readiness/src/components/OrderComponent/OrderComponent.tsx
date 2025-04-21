import React, {useState} from 'react';
import { TextField, Grid, Button, Typography, List, ListItem, ListItemText } from '@material-ui/core';
import { useApi } from '@backstage/core-plugin-api';
import { OrderApiRef } from '../../api';

export const OrderComponent = () => {

    const apiClient = useApi(OrderRefApi);

    const [order, setOrder] = useState({})


    return (
        <Grid item>
            <InfoCard title="Order">            
                <TableView aria-label="Order">
                    <TableHeader>
                        <Column>Order ID</Column>
                        <Column>{data.order_id}</Column>
                    </TableHeader>
                    <TableBody>
                        <Row>
                            <Cell>App Id</Cell>
                            <Cell>{data.app_id}</Cell>
                        </Row>
                        <Row>
                            <Cell>User ID</Cell>
                            <Cell>{data.user_id}</Cell>
                        </Row>
                        <Row>
                            <Cell>App Language</Cell>
                            <Cell>{data.job ? data.job.form.app_language : ''}</Cell>
                        </Row>
                        <Row>
                            <Cell>Status</Cell>
                            <Cell>{data.finished === true ? (<span>Finished</span>) : (<span>Running</span>)}</Cell>
                        </Row>
                        <Row>
                            <Cell>Result</Cell>
                            <Cell>{data.job ? data.job.result === 1 ? (<CheckmarkCircleOutline/>) : data.job.result === 0 ? (<CloseCircle/>) : (<SelectCircular/>) : (<SelectCircular/>)}</Cell>
                        </Row>                    
                    </TableBody>
                </TableView>
                <Well>
                    <ButtonGroup>
                        <Button variant="primary" onPress={handleFiles}>
                            <Download/>
                            <Text>Download Files</Text>
                        </Button>
                        <Button variant="secondary" onPress={handleAnswers}>
                            <Download/>
                            <Text>View Answers</Text>
                        </Button>                    
                        <Button variant="secondary" onPress={handleBack}>
                            <Back/>
                            <Text>Back</Text>
                        </Button>
                        <Button variant='primary' onPress={fetchData}>
                            <Refresh/>
                            <Text>Refresh</Text>
                        </Button>                                    
                    </ButtonGroup>
                </Well>
            </InfoCard>
        </Grid>        
    );
}