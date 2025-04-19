import React from 'react';

import { useNavigate } from 'react-router-dom';
import { Form, TextArea, Button, Picker, Item, TextField, Content, Heading  } from '@adobe/react-spectrum';

function RequestForm() {
    const [data, setData] = React.useState([]);
    const [language,setLangauge] = React.useState(null);
    const [app_id,setAppId] = React.useState(null);
    const [user_id,setUserId] = React.useState(null);
    const [config_text,setConfigText] = React.useState(null);

    const navigate = useNavigate();    
  
    const fetchData = async () => {
      try {
        const response = await fetch('/api/languages');
        const jsonData = await response.json();
        let arr = jsonData['languages']
        setData(arr)
      } catch (error) {
        console.error(error)
      }
    }
  
    React.useEffect(() => {
      fetchData();      
    }, []);
  
    const handleSubmit = (e) => {
      e.preventDefault();
      console.log("invoked")
      // build a 'form'
      let requestForm = 
      // submit it (POST) and get the response
      fetch('/api/order',{
        method:'POST',
        headers: {
          'Content-type':'application/json'
        },
        body: JSON.stringify(
          {
            user_id: user_id,
            app_id: app_id,
            app_language: language,
            config_text: config_text
          }
        ),
      }).then((response) => {
        console.log('Sent')
        navigate('/orders');
      }).catch((error) => {
        console.error(error);
      });
    }
  
    return (  
      <Content width="calc(100% - size-1000)">
        <Heading level={4}>The Process</Heading>
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
        <Form onSubmit={handleSubmit}>
          <TextField label="Application ID" value={app_id} onChange={setAppId}/>
          <TextField label="User ID" value={user_id} onChange={setUserId}/>
          <Picker label="Choose application language" onSelectionChange={setLangauge}>
            { data.map(item => (
              <Item key={item}>{item}</Item>
            ))}
          </Picker>
          <TextArea label="Copy & Paste your build file here" isRequired={true} value={config_text} onChange={setConfigText} height="size-3000"/>
          <Button type="submit" maxWidth="size-1000">Submit</Button>
        </Form>
      </Content>
    );
  }
  
  export default RequestForm;