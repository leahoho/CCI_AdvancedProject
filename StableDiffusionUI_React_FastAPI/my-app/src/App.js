import * as React from 'react'

import { 
  ChakraProvider, 
  Heading,
  Text,
  Input,
  Button,
  Wrap,
  Image,
  Stack,
  Flex,
  Spinner
 } from '@chakra-ui/react'
 import axios from "axios";
 import { useState } from "react";
 import theme from './theme'


const App = () => {
  const [image, updateImage] = useState();
  const [prompt, updatePrompt] = useState();
  const [loading, updateLoading] = useState();

  const generate = async prompt => {
    updateLoading(true);
    const result = await axios.get(`http://127.0.0.1:8000/?prompt=${prompt}`);
    updateImage(result.data);
    updateLoading(false);
    };


  return (


  <ChakraProvider theme={theme}>
        
      <Flex         
      height="100vh"
      direction="column"
      justifyContent="center"
      alignItems="center"
      backgroundColor="black"
      bgGradient={[
      'linear(to-tr, teal.5, yellow.400)',
      'linear(to-t, blue.500, teal.500)',
      'linear(to-b, orange.100, purple.500)', ]}
        >

      <Heading marginBottom={"10px"} color="white">Stable DIffusion 🚀  Text to Image 🖼</Heading>

      <Text marginBottom={"30px"} color="white">
          This react application leverages the model trained by Stability AI and
          Runway ML to generate images using the Stable Diffusion Deep Learning
          model. 
      </Text>


      <Wrap marginBottom={"10px"}>


      <Input value={prompt}
            onChange={(e) => updatePrompt(e.target.value)}
            width={"450px"} color="white" variant='outline' placeholder='Type here...'
            _placeholder={{ opacity: .5, color: 'white' }}>
      
      </Input>

      <Button onClick={(e) => 
      
      generate(prompt)} 

      color='white' bgGradient='linear(to-r, blue.300, purple.400, pink.200)'_hover={{bgGradient: 'linear(to-r, blue.500, purple.600, pink.400)'}}>
      Generate
      </Button>

      </Wrap>

      <br></br>

      {loading ?(
        <Stack>
          <Spinner 
          size='md'
          color='purple.500'
          speed='0.65s'
          />
        </Stack>
      ):image ? <Image src={`data:image/png;base64,${image}`} boxShadow="lg" height="556px" weight="556px" borderRadius='5px' />:null}

      </Flex> 
      
    </ChakraProvider>

  )
};


export default App;