import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
// import { Label, TextField, , } from 'react-aria-components';
import { Grid, View , defaultTheme, Provider, Content, Header, Footer, Heading, Button } from '@adobe/react-spectrum';

import RequestForm from './components/RequestForm';
import Home from './components/Home';
import Menu from './components/Menu';
import Existing from './components/Existing';

function App() {

  return (
    <Provider theme={defaultTheme}>
      <Router>
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
            <Menu/>
          </View>
          <View gridArea="content">   
            <Content>      

                <Routes>
                  <Route path="/" element={<Home/>}/>
                  <Route path="/form" element={<RequestForm/>}/>
                  <Route path="/existing" element={<Existing/>}/>
                </Routes>
          
              
            </Content>
          </View>
          <View gridArea="footer">
            <Footer>v0.0.1</Footer>
          </View>
        </Grid>
      </Router>    
    </Provider>
  );
}

export default App;


{/* <Form onSubmit={handleSubmit} maxWidth="size-5000">
<TextField label="Application ID"/>
<TextField label="User ID"/>
<Picker label="Choose application language">
  { data.map(item => (
    <Item key={item}>{item}</Item>
  ))}
</Picker>
<TextArea label="Copy & Paste your build file here" minWidth="size-3600" isRequired={true}/>
<Button variant="accent" type="submit" maxWidth="size-1000">Submit</Button>
</Form> */}