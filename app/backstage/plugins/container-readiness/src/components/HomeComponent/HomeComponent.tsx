import { Typography, Grid } from '@material-ui/core';
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
              <p>
                  Complete the form to identify your application, including the AppID, your user ID, what development language it is written in, and a copy of the build file.
              </p>
              <p>
                  A build file could be;
              </p>
              <ul>
                  <li>pom.xml</li>
                  <li>build.gradle</li>
                  <li>package.json</li>
                  <li>requirements.txt</li>
                  <li>app.csproj</li>
                  <li>...and others!</li>
              </ul>
              <p>
                Once you've completed the form, click "Submit" and you will receive an "Order ID".  Your from will be processed in the background.
              </p>                
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
