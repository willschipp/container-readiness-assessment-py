import React from 'react';

// import { Label, TextField, , } from 'react-aria-components';
import { Grid, View , defaultTheme, Provider, Content, Header, Footer, Heading, Form, TextArea, Button  } from '@adobe/react-spectrum';

function App() {
  const [data, setData] = React.useState({});

  // React.useEffect(() => {
  //   fetch('/api/languages')
  //     .then(response => response.json())
  //     .then(data => setData(data));
  // }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("invoked")
  }

  return (
    <Provider theme={defaultTheme}>
      <Grid 
        areas={['header header', 'sidebar content','footer footer']} 
        columns={['1fr','3fr']} 
        rows={['size-1000','auto','size-1000']} 
        height="100vh" 
        gap="size-100">
        <View gridArea="header">
          <Header>
            <Heading level={2}>Container Readiness Assessment Platform</Heading>
          </Header>
        </View>
        <View gridArea="sidebar">
          <Button>Check on existing Order</Button>
        </View>
        <View gridArea="content">   
        <Content>      
          <Form onSubmit={handleSubmit} maxWidth="size-5000">
            <TextArea label="Copy & Paste your build file here"/>
            <Button variant="accent" type="submit" maxWidth="size-1000">Submit</Button>
          </Form>
          </Content>
        </View>
        <View gridArea="footer">
          <Footer>v0.0.1</Footer>
        </View>
      </Grid>
    </Provider>
  );
}

export default App;