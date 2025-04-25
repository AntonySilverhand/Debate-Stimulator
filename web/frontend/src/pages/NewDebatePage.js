import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Heading,
  FormControl,
  FormLabel,
  Input,
  Textarea,
  Button,
  VStack,
  HStack,
  SimpleGrid,
  useToast,
  Divider,
  Text,
  Flex,
  Switch,
  Badge,
  Select,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
} from '@chakra-ui/react';
import apiService from '../utils/api';

// Define the BP debate roles and their descriptions
const debateRoles = [
  {
    role: "Prime Minister",
    team: "Opening Government",
    description: "Defines the motion and presents the case for the Government."
  },
  {
    role: "Leader of Opposition",
    team: "Opening Opposition",
    description: "Responds to the Prime Minister and presents the case for the Opposition."
  },
  {
    role: "Deputy Prime Minister",
    team: "Opening Government",
    description: "Rebuilds the Government case and addresses arguments from the Leader of Opposition."
  },
  {
    role: "Deputy Leader of Opposition",
    team: "Opening Opposition",
    description: "Rebuilds Opposition case and rebuts Deputy Prime Minister."
  },
  {
    role: "Member of Government",
    team: "Closing Government",
    description: "Introduces new material for the Government and rebuts previous arguments."
  },
  {
    role: "Member of Opposition",
    team: "Closing Opposition",
    description: "Introduces new material for the Opposition and rebuts previous arguments."
  },
  {
    role: "Government Whip",
    team: "Closing Government",
    description: "Summarizes the entire debate from the Government perspective."
  },
  {
    role: "Opposition Whip",
    team: "Closing Opposition",
    description: "Summarizes the entire debate from the Opposition perspective."
  }
];

// Sample debate motions
const sampleMotions = [
  "This house would legalize marijuana",
  "This house believes that social media has done more harm than good",
  "This house would ban private schools",
  "This house would implement a universal basic income",
  "This house believes that democracy is failing"
];

const NewDebatePage = () => {
  const [motion, setMotion] = useState("");
  const [roles, setRoles] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sampleMotionIdx, setSampleMotionIdx] = useState(0);
  const navigate = useNavigate();
  const toast = useToast();

  // Initialize roles with defaults from debateRoles
  useEffect(() => {
    setRoles(debateRoles.map(role => ({
      ...role,
      is_human: false,
      nickname: "AI"
    })));
  }, []);

  const handleRoleToggle = (index) => {
    const updatedRoles = [...roles];
    updatedRoles[index].is_human = !updatedRoles[index].is_human;
    updatedRoles[index].nickname = updatedRoles[index].is_human ? "" : "AI";
    setRoles(updatedRoles);
  };

  const handleNicknameChange = (index, nickname) => {
    const updatedRoles = [...roles];
    updatedRoles[index].nickname = nickname;
    setRoles(updatedRoles);
  };

  const handleSampleMotion = () => {
    const newIdx = (sampleMotionIdx + 1) % sampleMotions.length;
    setMotion(sampleMotions[newIdx]);
    setSampleMotionIdx(newIdx);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!motion.trim()) {
      toast({
        title: "Motion required",
        description: "Please enter a debate motion",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
      return;
    }
    
    // Check if any human roles have empty nicknames
    const emptyNicknames = roles.filter(r => r.is_human && !r.nickname.trim());
    if (emptyNicknames.length > 0) {
      toast({
        title: "Nickname required",
        description: "Please provide nicknames for all human participants",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
      return;
    }
    
    try {
      setIsLoading(true);
      
      // Format the data for the API
      const debateConfig = {
        motion: motion,
        roles: roles.map(({ role, is_human, nickname }) => ({
          role,
          is_human,
          nickname: nickname || (is_human ? "Human" : "AI")
        }))
      };
      
      // Start a new debate using our API service
      const response = await apiService.startDebate(debateConfig);
      
      if (response && response.debate_id) {
        toast({
          title: "Debate created",
          description: "Setting up your debate session...",
          status: "success",
          duration: 3000,
          isClosable: true,
        });
        
        // Navigate to the debate session page
        navigate(`/debate/${response.debate_id}`);
      }
    } catch (error) {
      console.error("Error starting debate:", error);
      toast({
        title: "Error",
        description: error.message || "Failed to start debate",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const countHumanRoles = () => {
    return roles.filter(r => r.is_human).length;
  };

  return (
    <Container maxW="container.lg" py={8}>
      <VStack spacing={8} align="stretch">
        <Heading as="h1" size="xl" textAlign="center">
          Start a New Debate
        </Heading>
        
        <Box as="form" onSubmit={handleSubmit}>
          <VStack spacing={8} align="stretch">
            {/* Motion Section */}
            <Box bg="white" p={6} borderRadius="md" boxShadow="md">
              <VStack spacing={4} align="stretch">
                <Heading as="h2" size="md">
                  1. Choose a Motion
                </Heading>
                <FormControl isRequired>
                  <FormLabel>Debate Motion</FormLabel>
                  <Textarea
                    value={motion}
                    onChange={(e) => setMotion(e.target.value)}
                    placeholder="This house would..."
                    rows={3}
                  />
                </FormControl>
                <Button 
                  onClick={handleSampleMotion} 
                  variant="outline" 
                  size="sm" 
                  alignSelf="flex-end"
                >
                  Suggest a Motion
                </Button>
              </VStack>
            </Box>

            {/* Role Configuration Section */}
            <Box bg="white" p={6} borderRadius="md" boxShadow="md">
              <VStack spacing={6} align="stretch">
                <Heading as="h2" size="md">
                  2. Configure Participants
                </Heading>
                <Text>
                  Toggle which positions you want to play and which will be filled by AI.
                  You have selected {countHumanRoles()} role(s) to play yourself.
                </Text>
                
                <Accordion allowMultiple defaultIndex={[0]}>
                  {/* Opening Government */}
                  <AccordionItem>
                    <h2>
                      <AccordionButton>
                        <Box flex="1" textAlign="left" fontWeight="bold">
                          Opening Government
                        </Box>
                        <AccordionIcon />
                      </AccordionButton>
                    </h2>
                    <AccordionPanel pb={4}>
                      {roles.filter(r => r.team === "Opening Government").map((role, idx) => {
                        const roleIndex = roles.findIndex(r => r.role === role.role);
                        return (
                          <Box 
                            key={role.role} 
                            p={4} 
                            borderWidth="1px" 
                            borderRadius="md" 
                            mb={4}
                            borderColor={role.is_human ? "brand.200" : "gray.200"}
                            bg={role.is_human ? "brand.50" : "white"}
                          >
                            <Flex justifyContent="space-between" alignItems="center" mb={2}>
                              <Heading as="h3" size="sm">{role.role}</Heading>
                              <HStack>
                                <Text fontSize="sm" color="gray.600">AI</Text>
                                <Switch 
                                  isChecked={role.is_human}
                                  onChange={() => handleRoleToggle(roleIndex)}
                                  colorScheme="brand"
                                />
                                <Text fontSize="sm" color="gray.600">Human</Text>
                              </HStack>
                            </Flex>
                            <Text fontSize="sm" color="gray.600" mb={3}>
                              {role.description}
                            </Text>
                            {role.is_human && (
                              <FormControl>
                                <FormLabel fontSize="sm">Your Nickname</FormLabel>
                                <Input 
                                  size="sm"
                                  value={role.nickname}
                                  onChange={(e) => handleNicknameChange(roleIndex, e.target.value)}
                                  placeholder="Enter your nickname"
                                />
                              </FormControl>
                            )}
                          </Box>
                        );
                      })}
                    </AccordionPanel>
                  </AccordionItem>

                  {/* Opening Opposition */}
                  <AccordionItem>
                    <h2>
                      <AccordionButton>
                        <Box flex="1" textAlign="left" fontWeight="bold">
                          Opening Opposition
                        </Box>
                        <AccordionIcon />
                      </AccordionButton>
                    </h2>
                    <AccordionPanel pb={4}>
                      {roles.filter(r => r.team === "Opening Opposition").map((role, idx) => {
                        const roleIndex = roles.findIndex(r => r.role === role.role);
                        return (
                          <Box 
                            key={role.role} 
                            p={4} 
                            borderWidth="1px" 
                            borderRadius="md" 
                            mb={4}
                            borderColor={role.is_human ? "brand.200" : "gray.200"}
                            bg={role.is_human ? "brand.50" : "white"}
                          >
                            <Flex justifyContent="space-between" alignItems="center" mb={2}>
                              <Heading as="h3" size="sm">{role.role}</Heading>
                              <HStack>
                                <Text fontSize="sm" color="gray.600">AI</Text>
                                <Switch 
                                  isChecked={role.is_human}
                                  onChange={() => handleRoleToggle(roleIndex)}
                                  colorScheme="brand"
                                />
                                <Text fontSize="sm" color="gray.600">Human</Text>
                              </HStack>
                            </Flex>
                            <Text fontSize="sm" color="gray.600" mb={3}>
                              {role.description}
                            </Text>
                            {role.is_human && (
                              <FormControl>
                                <FormLabel fontSize="sm">Your Nickname</FormLabel>
                                <Input 
                                  size="sm"
                                  value={role.nickname}
                                  onChange={(e) => handleNicknameChange(roleIndex, e.target.value)}
                                  placeholder="Enter your nickname"
                                />
                              </FormControl>
                            )}
                          </Box>
                        );
                      })}
                    </AccordionPanel>
                  </AccordionItem>

                  {/* Closing Government */}
                  <AccordionItem>
                    <h2>
                      <AccordionButton>
                        <Box flex="1" textAlign="left" fontWeight="bold">
                          Closing Government
                        </Box>
                        <AccordionIcon />
                      </AccordionButton>
                    </h2>
                    <AccordionPanel pb={4}>
                      {roles.filter(r => r.team === "Closing Government").map((role, idx) => {
                        const roleIndex = roles.findIndex(r => r.role === role.role);
                        return (
                          <Box 
                            key={role.role} 
                            p={4} 
                            borderWidth="1px" 
                            borderRadius="md" 
                            mb={4}
                            borderColor={role.is_human ? "brand.200" : "gray.200"}
                            bg={role.is_human ? "brand.50" : "white"}
                          >
                            <Flex justifyContent="space-between" alignItems="center" mb={2}>
                              <Heading as="h3" size="sm">{role.role}</Heading>
                              <HStack>
                                <Text fontSize="sm" color="gray.600">AI</Text>
                                <Switch 
                                  isChecked={role.is_human}
                                  onChange={() => handleRoleToggle(roleIndex)}
                                  colorScheme="brand"
                                />
                                <Text fontSize="sm" color="gray.600">Human</Text>
                              </HStack>
                            </Flex>
                            <Text fontSize="sm" color="gray.600" mb={3}>
                              {role.description}
                            </Text>
                            {role.is_human && (
                              <FormControl>
                                <FormLabel fontSize="sm">Your Nickname</FormLabel>
                                <Input 
                                  size="sm"
                                  value={role.nickname}
                                  onChange={(e) => handleNicknameChange(roleIndex, e.target.value)}
                                  placeholder="Enter your nickname"
                                />
                              </FormControl>
                            )}
                          </Box>
                        );
                      })}
                    </AccordionPanel>
                  </AccordionItem>

                  {/* Closing Opposition */}
                  <AccordionItem>
                    <h2>
                      <AccordionButton>
                        <Box flex="1" textAlign="left" fontWeight="bold">
                          Closing Opposition
                        </Box>
                        <AccordionIcon />
                      </AccordionButton>
                    </h2>
                    <AccordionPanel pb={4}>
                      {roles.filter(r => r.team === "Closing Opposition").map((role, idx) => {
                        const roleIndex = roles.findIndex(r => r.role === role.role);
                        return (
                          <Box 
                            key={role.role} 
                            p={4} 
                            borderWidth="1px" 
                            borderRadius="md" 
                            mb={4}
                            borderColor={role.is_human ? "brand.200" : "gray.200"}
                            bg={role.is_human ? "brand.50" : "white"}
                          >
                            <Flex justifyContent="space-between" alignItems="center" mb={2}>
                              <Heading as="h3" size="sm">{role.role}</Heading>
                              <HStack>
                                <Text fontSize="sm" color="gray.600">AI</Text>
                                <Switch 
                                  isChecked={role.is_human}
                                  onChange={() => handleRoleToggle(roleIndex)}
                                  colorScheme="brand"
                                />
                                <Text fontSize="sm" color="gray.600">Human</Text>
                              </HStack>
                            </Flex>
                            <Text fontSize="sm" color="gray.600" mb={3}>
                              {role.description}
                            </Text>
                            {role.is_human && (
                              <FormControl>
                                <FormLabel fontSize="sm">Your Nickname</FormLabel>
                                <Input 
                                  size="sm"
                                  value={role.nickname}
                                  onChange={(e) => handleNicknameChange(roleIndex, e.target.value)}
                                  placeholder="Enter your nickname"
                                />
                              </FormControl>
                            )}
                          </Box>
                        );
                      })}
                    </AccordionPanel>
                  </AccordionItem>
                </Accordion>
              </VStack>
            </Box>

            {/* Submit Button */}
            <Button 
              type="submit" 
              colorScheme="brand" 
              size="lg" 
              isLoading={isLoading}
              loadingText="Starting Debate..."
            >
              Start Debate
            </Button>
          </VStack>
        </Box>
      </VStack>
    </Container>
  );
};

export default NewDebatePage;
