import React from 'react';

import { Form, TextArea, Button, Picker, Item, TextField  } from '@adobe/react-spectrum';

function RequestForm() {
    const [data, setData] = React.useState([]);
  
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

      // submit it (POST) and get the response
    }
  
    return (     
      <Form onSubmit={handleSubmit} maxWidth="size-5000">
        <TextField label="Application ID"/>
        <TextField label="User ID"/>
        <Picker label="Choose application language">
          { data.map(item => (
            <Item key={item}>{item}</Item>
          ))}
        </Picker>
        <TextArea label="Copy & Paste your build file here" minWidth="size-3600" isRequired={true}/>
        <Button type="submit" maxWidth="size-1000">Submit</Button>
      </Form>
    );
  }
  
  export default RequestForm;