import {  Grid,  } from '@material-ui/core';
import {
  InfoCard,
  Header,
  Page,
  Content,
  ContentHeader,
  SupportButton
} from '@backstage/core-components';


import { RefreshWrapper } from '../../RefreshWrapper';
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
      <RefreshWrapper>
        <Grid container spacing={3} direction="column">
          <Grid item>
            <NewRequestForm />
          </Grid>
          <Grid item>
            <OrdersComponent />
          </Grid>
        </Grid>
      </RefreshWrapper>
    </Content>
  </Page>
)};
