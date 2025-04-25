import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { 
  Box, 
  Heading, 
  Text, 
  Button, 
  VStack, 
  HStack,
  Container, 
  Image, 
  SimpleGrid,
  Icon,
  useColorModeValue
} from '@chakra-ui/react';
import { FaUsers, FaMicrophone, FaRobot, FaChartLine } from 'react-icons/fa';

const FeatureCard = ({ icon, title, description }) => {
  const cardBg = useColorModeValue('white', 'gray.700');
  
  return (
    <Box 
      p={6} 
      boxShadow="md" 
      borderRadius="lg" 
      bg={cardBg}
      transition="all 0.3s"
      _hover={{ transform: 'translateY(-5px)', boxShadow: 'lg' }}
    >
      <Icon as={icon} w={10} h={10} mb={4} color="brand.500" />
      <Heading as="h3" size="md" mb={2}>{title}</Heading>
      <Text color="gray.600">{description}</Text>
    </Box>
  );
};

const HomePage = () => {
  const heroBg = useColorModeValue('gray.50', 'gray.900');
  
  return (
    <Box>
      {/* Hero Section */}
      <Box py={20} bg={heroBg}>
        <Container maxW="container.xl">
          <SimpleGrid columns={{ base: 1, md: 2 }} spacing={10} alignItems="center">
            <VStack spacing={6} align="flex-start">
              <Heading as="h1" size="2xl" fontFamily="heading">
                Sharpen Your Debate Skills with AI
              </Heading>
              <Text fontSize="xl" color="gray.600">
                Practice British Parliamentary debate format with intelligent AI opponents, 
                receive feedback, and track your progress over time.
              </Text>
              <HStack spacing={4}>
                <Button as={RouterLink} to="/new-debate" colorScheme="brand" size="lg">
                  Start a New Debate
                </Button>
                <Button as={RouterLink} to="/history" variant="outline" size="lg">
                  View Previous Debates
                </Button>
              </HStack>
            </VStack>
            
            <Box>
              {/* Placeholder for debate illustration - you'd replace this with an actual image */}
              <Box 
                h="300px" 
                bg="gray.200" 
                borderRadius="md" 
                display="flex" 
                alignItems="center" 
                justifyContent="center"
              >
                <Text>Debate Illustration</Text>
              </Box>
            </Box>
          </SimpleGrid>
        </Container>
      </Box>
      
      {/* Features Section */}
      <Container maxW="container.xl" py={16}>
        <VStack spacing={12}>
          <VStack spacing={4} textAlign="center">
            <Heading size="xl">Features</Heading>
            <Text fontSize="lg" color="gray.600" maxW="800px">
              Everything you need to practice and improve your debate skills in the British Parliamentary format.
            </Text>
          </VStack>
          
          <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={10} width="100%">
            <FeatureCard 
              icon={FaUsers} 
              title="British Parliamentary Format" 
              description="Practice the 8-speaker format with AI opponents filling any position you choose."
            />
            <FeatureCard 
              icon={FaMicrophone} 
              title="Speech Recognition" 
              description="Use your microphone to deliver speeches and get real-time transcriptions."
            />
            <FeatureCard 
              icon={FaRobot} 
              title="AI Opponents" 
              description="Debate against sophisticated AI that adapts to the motion and previous speeches."
            />
            <FeatureCard 
              icon={FaChartLine} 
              title="Progress Tracking" 
              description="Track your improvement over time with detailed performance metrics."
            />
          </SimpleGrid>
        </VStack>
      </Container>
      
      {/* How It Works Section */}
      <Box py={16} bg={heroBg}>
        <Container maxW="container.xl">
          <VStack spacing={12}>
            <VStack spacing={4} textAlign="center">
              <Heading size="xl">How It Works</Heading>
              <Text fontSize="lg" color="gray.600" maxW="800px">
                Getting started with Debate Stimulator is easy - create a new debate, 
                configure participants, and start practicing.
              </Text>
            </VStack>
            
            <SimpleGrid columns={{ base: 1, md: 3 }} spacing={8} width="100%">
              <VStack spacing={4} align="flex-start">
                <Heading as="h3" size="md">1. Choose a Motion</Heading>
                <Text>Select from popular debate motions or create your own to practice.</Text>
              </VStack>
              
              <VStack spacing={4} align="flex-start">
                <Heading as="h3" size="md">2. Configure Participants</Heading>
                <Text>Decide which positions you want to play and which will be filled by AI.</Text>
              </VStack>
              
              <VStack spacing={4} align="flex-start">
                <Heading as="h3" size="md">3. Deliver Speeches</Heading>
                <Text>Take turns delivering speeches following the British Parliamentary format.</Text>
              </VStack>
            </SimpleGrid>
            
            <Button as={RouterLink} to="/new-debate" colorScheme="brand" size="lg">
              Get Started Now
            </Button>
          </VStack>
        </Container>
      </Box>
    </Box>
  );
};

export default HomePage;
