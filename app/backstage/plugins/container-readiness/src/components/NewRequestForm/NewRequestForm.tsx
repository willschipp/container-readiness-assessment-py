import React, { useState } from 'react';
import { TextField, Grid, Button } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';


interface FormValues {
    app_id: string,
    user_id: string,
    config_text: string
}

const useStyles = makeStyles((theme) => ({
    textFieldContainer: {
      width: '80%', // Make the container 80% width
      margin: '0 auto', // Center the container horizontally
    },
    multilineTextField: {
      width: '100%', // TextField now stretches to fill its container
    },
  }));
  

export const NewRequestForm = () => {

    const classes = useStyles();

    const [formValues, setFormValues] = useState<FormValues>({
        app_id: '',
        user_id: '',
        config_text: ''
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormValues({...formValues, [e.target.name]: e.target.value});
    }

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        console.log("invoked")
        // build a 'form'
        // submit it (POST) and get the response
        // fetch('/api/order',{
        //   method:'POST',
        //   headers: {
        //     'Content-type':'application/json'
        //   },
        //   body: JSON.stringify(
        //     {
        //       user_id: user_id,
        //       app_id: app_id,
        //       app_language: language,
        //       config_text: config_text
        //     }
        //   ),
        // }).then((response) => {
        //   console.log('Sent')
        //   // navigate('/orders');
        // }).catch((error) => {
        //   console.error(error);
        // });
    }


    return (
        <form onSubmit={handleSubmit}>
            <Grid container spacing={2}>
                <Grid item xs={12}> 
                    <TextField label="Application ID" name="app_id" value={formValues.app_id} onChange={handleChange} fullWidth required/>  
                </Grid>
                <Grid item xs={12}> 
                    <TextField label="User ID" name="user_id" value={formValues.user_id} onChange={handleChange} fullWidth required/>  
                </Grid>
                <Grid item xs={12}> 
                    <TextField label="Copy & Paste your build file here" name="config_text" value={formValues.config_text} onChange={handleChange} fullWidth required multiline minRows={5} variant="outlined" style={{ overflowY:'auto'}}/>  
                </Grid>                                        
                <Grid item xs={12}> 
                    <Button type="submit" variant="contained" color="primary">Submit</Button>
                </Grid>                    
            </Grid>
        </form>
    )
}