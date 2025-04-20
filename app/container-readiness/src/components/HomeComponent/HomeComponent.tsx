import { Typography, Grid, List, ListItem, ListItemText } from '@material-ui/core';
import {
  InfoCard,
  Header,
  Page,
  Content,
  ContentHeader,
  SupportButton
} from '@backstage/core-components';

import { OrdersComponent } from '../OrdersComponent';
import { NewRequestForm } from '../NewRequestForm';

export const HomeComponent = () => {

  return (
  <Page themeId="tool">
    <Header title="Container Readiness Platform" subtitle="A quick app to check if yours can run on Kubernetes">
    </Header>
    <Content>
      <ContentHeader title="Description">
        <SupportButton>A description of your plugin goes here.</SupportButton>
      </ContentHeader>
      <Grid container spacing={3} direction="column">
        <Grid item>
          <InfoCard title="Start an Assessment">
            <Typography variant="body1">
              Complete the form to identify your application, including the AppID, your user ID, what development language it is written in, and a copy of the build file.
              <br/>
              A build file could be;
            </Typography>
            <List>
              <ListItem>
                <ListItemText primary="pom.xml"/>
              </ListItem>
              <ListItem>
                <ListItemText primary="build.gradle"/>
              </ListItem>
              <ListItem>
                <ListItemText primary="package.json"/>
              </ListItem>
              <ListItem>
                <ListItemText primary="requirements.txt"/>
              </ListItem>
              <ListItem>
                <ListItemText primary="app.csproj"/>
              </ListItem>
              <ListItem>
                <ListItemText primary="...and others!"/>
              </ListItem>                                                                      
            </List>
            <Typography variant="body1">
               Once you've completed the form, click "Submit" and you will receive an "Order ID".  Your from will be processed in the background.
            </Typography>
            <NewRequestForm/>
          </InfoCard>
        </Grid>
        <Grid item>
          <OrdersComponent />
        </Grid>
      </Grid>
    </Content>
  </Page>
)};
