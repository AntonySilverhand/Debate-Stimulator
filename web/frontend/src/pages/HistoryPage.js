import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Heading,
  Text,
  VStack,
  HStack,
  SimpleGrid,
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Button,
  Badge,
  Divider,
  Spinner,
  Alert,
  AlertIcon,
  Flex,
  useColorModeValue,
  Select,
  IconButton,
} from '@chakra-ui/react';
import { FaCalendarAlt, FaEye, FaDownload, FaTrash } from 'react-icons/fa';
import { Link as RouterLink } from 'react-router-dom';
import axios from 'axios';

// This component would display past debate records
// In a real implementation, it would need to connect to the backend to fetch debate history
const HistoryPage = () => {
  const [debates, setDebates] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sortOrder, setSortOrder] = useState('newest');
  
  const cardBg = useColorModeValue('white', 'gray.700');
  
  // Mock data for demonstration - in a real implementation, this would come from the API
  useEffect(() => {
    const fetchDebates = async () => {
      try {
        // This would be replaced with an actual API call in production
        // const response = await axios.get('/api/debate-history');
        // setDebates(response.data);
        
        // For demo purposes, we'll create mock data
        const mockDebates = [
          {
            id: 'debate-1',
            date: '2025-04-25T10:30:00',
            motion: 'This house would legalize marijuana',
            participants: [
              { role: 'Prime Minister', speaker: 'Alice', type: 'Human' },
              { role: 'Leader of Opposition', speaker: 'AI', type: 'AI' },
              { role: 'Deputy Prime Minister', speaker: 'Bob', type: 'Human' },
              { role: 'Deputy Leader of Opposition', speaker: 'AI', type: 'AI' },
              { role: 'Member of Government', speaker: 'AI', type: 'AI' },
              { role: 'Member of Opposition', speaker: 'AI', type: 'AI' },
              { role: 'Government Whip', speaker: 'AI', type: 'AI' },
              { role: 'Opposition Whip', speaker: 'AI', type: 'AI' }
            ],
            speechCount: 8
          },
          {
            id: 'debate-2',
            date: '2025-04-24T14:15:00',
            motion: 'This house believes that social media has done more harm than good',
            participants: [
              { role: 'Prime Minister', speaker: 'AI', type: 'AI' },
              { role: 'Leader of Opposition', speaker: 'Charlie', type: 'Human' },
              { role: 'Deputy Prime Minister', speaker: 'AI', type: 'AI' },
              { role: 'Deputy Leader of Opposition', speaker: 'AI', type: 'AI' },
              { role: 'Member of Government', speaker: 'AI', type: 'AI' },
              { role: 'Member of Opposition', speaker: 'AI', type: 'AI' },
              { role: 'Government Whip', speaker: 'AI', type: 'AI' },
              { role: 'Opposition Whip', speaker: 'AI', type: 'AI' }
            ],
            speechCount: 8
          },
          {
            id: 'debate-3',
            date: '2025-04-22T09:45:00',
            motion: 'This house would ban private schools',
            participants: [
              { role: 'Prime Minister', speaker: 'David', type: 'Human' },
              { role: 'Leader of Opposition', speaker: 'Emma', type: 'Human' },
              { role: 'Deputy Prime Minister', speaker: 'AI', type: 'AI' },
              { role: 'Deputy Leader of Opposition', speaker: 'AI', type: 'AI' },
              { role: 'Member of Government', speaker: 'AI', type: 'AI' },
              { role: 'Member of Opposition', speaker: 'AI', type: 'AI' },
              { role: 'Government Whip', speaker: 'AI', type: 'AI' },
              { role: 'Opposition Whip', speaker: 'AI', type: 'AI' }
            ],
            speechCount: 8
          }
        ];
        
        setDebates(mockDebates);
      } catch (error) {
        console.error("Error fetching debate history:", error);
        setError("Failed to load debate history. Please try again later.");
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchDebates();
  }, []);
  
  const sortedDebates = [...debates].sort((a, b) => {
    const dateA = new Date(a.date);
    const dateB = new Date(b.date);
    return sortOrder === 'newest' ? dateB - dateA : dateA - dateB;
  });
  
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };
  
  if (isLoading) {
    return (
      <Container maxW="container.lg" py={8}>
        <Flex direction="column" align="center" justify="center" h="50vh">
          <Spinner size="xl" color="brand.500" />
          <Text mt={4} fontSize="lg">Loading debate history...</Text>
        </Flex>
      </Container>
    );
  }
  
  if (error) {
    return (
      <Container maxW="container.lg" py={8}>
        <Alert status="error" borderRadius="md">
          <AlertIcon />
          <Text>{error}</Text>
        </Alert>
      </Container>
    );
  }
  
  if (debates.length === 0) {
    return (
      <Container maxW="container.lg" py={8}>
        <VStack spacing={8}>
          <Heading as="h1" size="xl">Debate History</Heading>
          <Box 
            p={8} 
            borderWidth="1px" 
            borderRadius="lg" 
            bg={cardBg}
            textAlign="center"
          >
            <Heading as="h3" size="md" mb={4}>No Debates Found</Heading>
            <Text mb={6}>You haven't participated in any debates yet.</Text>
            <Button 
              as={RouterLink} 
              to="/new-debate" 
              colorScheme="brand"
            >
              Start Your First Debate
            </Button>
          </Box>
        </VStack>
      </Container>
    );
  }
  
  return (
    <Container maxW="container.lg" py={8}>
      <VStack spacing={8} align="stretch">
        <Flex justify="space-between" align="center">
          <Heading as="h1" size="xl">Debate History</Heading>
          
          <HStack>
            <Text fontSize="sm">Sort by:</Text>
            <Select 
              size="sm" 
              width="120px"
              value={sortOrder}
              onChange={(e) => setSortOrder(e.target.value)}
            >
              <option value="newest">Newest</option>
              <option value="oldest">Oldest</option>
            </Select>
          </HStack>
        </Flex>
        
        <SimpleGrid columns={{ base: 1, md: 2 }} spacing={6}>
          {sortedDebates.map(debate => (
            <Card key={debate.id} bg={cardBg} boxShadow="md">
              <CardHeader>
                <Flex justify="space-between" align="center">
                  <Heading size="md" noOfLines={2}>
                    {debate.motion}
                  </Heading>
                  <HStack>
                    <FaCalendarAlt />
                    <Text fontSize="sm">{formatDate(debate.date)}</Text>
                  </HStack>
                </Flex>
              </CardHeader>
              
              <CardBody>
                <VStack align="start" spacing={3}>
                  <Text fontWeight="bold">Participants:</Text>
                  <SimpleGrid columns={2} spacing={2} width="100%">
                    {debate.participants
                      .filter(p => p.type === 'Human')
                      .map((participant, idx) => (
                        <HStack key={idx}>
                          <Badge colorScheme="green">{participant.type}</Badge>
                          <Text fontSize="sm">{participant.role}: {participant.speaker}</Text>
                        </HStack>
                      ))}
                  </SimpleGrid>
                  
                  <Text>
                    <Badge>{debate.speechCount}</Badge> speeches delivered
                  </Text>
                </VStack>
              </CardBody>
              
              <Divider />
              
              <CardFooter>
                <HStack spacing={2}>
                  <Button 
                    size="sm" 
                    leftIcon={<FaEye />} 
                    as={RouterLink} 
                    to={`/debate/${debate.id}/review`}
                    colorScheme="brand"
                    variant="outline"
                  >
                    View
                  </Button>
                  <Button 
                    size="sm"
                    leftIcon={<FaDownload />}
                    colorScheme="gray"
                    variant="outline"
                  >
                    Export
                  </Button>
                  <IconButton
                    size="sm"
                    aria-label="Delete debate"
                    icon={<FaTrash />}
                    colorScheme="red"
                    variant="ghost"
                  />
                </HStack>
              </CardFooter>
            </Card>
          ))}
        </SimpleGrid>
      </VStack>
    </Container>
  );
};

export default HistoryPage;
