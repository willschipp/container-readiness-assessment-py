import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Grid, View , defaultTheme, Provider, Content } from '@adobe/react-spectrum';


import AppHeader from './components/AppHeader';
import AppFooter from './components/AppFooter';


import RequestForm from './components/RequestForm';
import Home from './components/Home';
import Menu from './components/Menu';
import Existing from './components/Existing';
import Order from './components/Order';
import Orders from './components/Orders';
import Files from './components/Files';
import Answers from './components/Answers';

function App() {

  return (
    <Provider theme={defaultTheme}>
      <Router>
        <Grid 
          areas={['header header', 'sidebar content','footer footer']} 
          columns={['1fr','3fr']} 
          rows={['size-1000','auto','size-1000']} 
          height="100vh" 
          gap="size-100"
          justifyContent="center">
          <View gridArea="header">
            <AppHeader/>
          </View>
          <View gridArea="sidebar">
            <Menu/>
          </View>
          <View gridArea="content">   
            <Content>      

                <Routes>
                  <Route exact path="/" element={<Home/>}/>
                  <Route path="/form" element={<RequestForm/>}/>
                  <Route path="/existing" element={<Existing/>}/>
                  <Route path="/order" element={<Order/>}/>
                  <Route path="/orders" element={<Orders/>}/>
                  <Route path="/files" element={<Files/>}/>
                  <Route path="/answers" element={<Answers/>}/>
                </Routes>          
              
            </Content>
          </View>
          <View gridArea="footer">
            <AppFooter/>
          </View>
        </Grid>
      </Router>    
    </Provider>
  );
}

export default App;
