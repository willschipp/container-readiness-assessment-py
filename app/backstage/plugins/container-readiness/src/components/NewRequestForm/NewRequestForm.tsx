import React, { useState } from 'react';
import { TextField, Grid, Button, Typography, List, ListItem, ListItemText } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { OrderApiRef } from '../../api';
import { useApi } from '@backstage/core-plugin-api';
import { InfoCard } from '@backstage/core-components';
import { useRefresh } from '../../RefreshWrapper';


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

    const apiClient = useApi(OrderApiRef);

    const [order, setOrder] = useState({})

    const { triggerRefresh } = useRefresh();

    const [formValues, setFormValues] = useState<FormValues>({
        app_id: '',
        user_id: '',
        config_text: ''
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormValues({...formValues, [e.target.name]: e.target.value});
    }

    const sendForm = async () => {
        const response = await apiClient.postForm({
            user_id: formValues.user_id,
            app_id: formValues.app_id,
            config_text: formValues.config_text                    
        })
        console.log(response)
        triggerRefresh();
    }

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        console.log("invoked")
        sendForm();
    }


    return (
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
        </InfoCard>
      </Grid>

    )
}