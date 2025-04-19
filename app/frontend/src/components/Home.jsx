import React from 'react';
import { useNavigate } from 'react-router-dom';

import { Content, Heading, Link } from '@adobe/react-spectrum';

function Home() {

    const navigate = useNavigate();

    return (
        <Content width="calc(100% - size-1000)">
            <Heading level={3}>The App!</Heading>
            <p>
                The <b>C</b>ontainer <b>R</b>eadiness {/*<b>A</b>ssessment*/} <b>P</b>latform is a simple tool to assess if
                an application can readily be deployed - in it's current state - to a kubernetes environment.</p>            
            <p>
                The application uses a Large Language Model (LLM) to perform an assessment and generate starter files
                to help users get started with deploying on Kubernetes.
            </p>
            <Heading level={4}>The Process</Heading>
            <p>
                Click on the <Link onPress={() => navigate('/form')}>"Create a New Request"</Link> option on the menu and complete the form.  You will then received an Order number.
                In the background, the backend will then analyze the application build file to assess if it can be deployed - as is - 
                to Kubernetes.  If it can, a series of starter files will be created (e.g. Dockerfile, deployment.yaml, and service.yaml).
            </p>
            <p>
                The process is asynchronous so to check on the progress, go to the <Link onPress={() => navigate('/existing')}>"View an existing Request"</Link> and enter your Order number,
                or click on <Link onPress={() => navigate('/orders')}>"View All Orders"</Link> and find your application there.
            </p>
            <p>
                Once your application has been assessed, if it can be deployed, you can download the helper files to get you started.
            </p>
            <Heading level={3}>Good Luck!</Heading>
        </Content>
    )
}


export default Home;