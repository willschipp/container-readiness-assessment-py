import React from 'react';

import { useNavigate } from 'react-router-dom';
import { Form, TextArea, Button, Picker, Item, TextField  } from '@adobe/react-spectrum';

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
      <Form onSubmit={handleSubmit} maxWidth="size-5000">
        <TextField label="Application ID" value={app_id} onChange={setAppId}/>
        <TextField label="User ID" value={user_id} onChange={setUserId}/>
        <Picker label="Choose application language" onSelectionChange={setLangauge}>
          { data.map(item => (
            <Item key={item}>{item}</Item>
          ))}
        </Picker>
        <TextArea label="Copy & Paste your build file here" minWidth="size-3600" isRequired={true} value={config_text} onChange={setConfigText}/>
        <Button type="submit" maxWidth="size-1000">Submit</Button>
      </Form>
    );
  }
  
  export default RequestForm;