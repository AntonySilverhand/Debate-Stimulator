import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Heading,
  VStack,
  HStack,
  Text,
  Button,
  Badge,
  Progress,
  Flex,
  Textarea,
  IconButton,
  Spinner,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  useToast,
  Divider,
  Card,
  CardHeader,
  CardBody,
  Stack,
  StackDivider,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
} from '@chakra-ui/react';
import { FaMicrophone, FaStop, FaPaperPlane, FaRobot, FaUser, FaHistory, FaVolumeUp } from 'react-icons/fa';
import TextToSpeech from '../components/TextToSpeech';
import apiService from '../utils/api';

const AudioRecorder = ({ onAudioCaptured, isRecording, setIsRecording }) => {
  const [audioStream, setAudioStream] = useState(null);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioChunks, setAudioChunks] = useState([]);
  const [recordingTime, setRecordingTime] = useState(0);
  const timerRef = useRef(null);
  
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      setAudioStream(stream);
      
      const recorder = new MediaRecorder(stream);
      setMediaRecorder(recorder);
      
      const chunks = [];
      setAudioChunks(chunks);
      
      recorder.ondataavailable = e => {
        chunks.push(e.data);
      };
      
      recorder.onstop = () => {
        const audioBlob = new Blob(chunks, { type: 'audio/wav' });
        const reader = new FileReader();
        reader.readAsDataURL(audioBlob);
        reader.onloadend = () => {
          const base64Audio = reader.result.split(',')[1];
          onAudioCaptured(base64Audio);
        };
      };
      
      recorder.start();
      setIsRecording(true);
      
      // Start timer
      setRecordingTime(0);
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);
      
    } catch (err) {
      console.error("Error accessing microphone:", err);
    }
  };
  
  const stopRecording = () => {
    if (mediaRecorder && isRecording) {
      mediaRecorder.stop();
      
      // Stop all audio tracks
      if (audioStream) {
        audioStream.getTracks().forEach(track => track.stop());
      }
      
      // Clear timer
      clearInterval(timerRef.current);
      
      setIsRecording(false);
    }
  };
  
  // Format recording time as mm:ss
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60).toString().padStart(2, '0');
    const secs = (seconds % 60).toString().padStart(2, '0');
    return `${mins}:${secs}`;
  };
  
  return (
    <Box borderWidth="1px" borderRadius="lg" p={4} bg="white">
      <VStack spacing={4}>
        <Heading size="md">Speech Recording</Heading>
        
        <Text>{isRecording ? `Recording: ${formatTime(recordingTime)}` : 'Ready to record'}</Text>
        
        <HStack>
          {!isRecording ? (
            <Button
              leftIcon={<FaMicrophone />}
              colorScheme="red"
              onClick={startRecording}
            >
              Start Recording
            </Button>
          ) : (
            <Button
              leftIcon={<FaStop />}
              colorScheme="gray"
              onClick={stopRecording}
            >
              Stop Recording
            </Button>
          )}
        </HStack>
      </VStack>
    </Box>
  );
};

const SpeechInput = ({ onSubmit, currentRole, isHuman }) => {
  const [speechText, setSpeechText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [audioBase64, setAudioBase64] = useState(null);
  const toast = useToast();
  
  const handleAudioCaptured = (base64Audio) => {
    setAudioBase64(base64Audio);
    setIsProcessing(true);
    
    // Send audio to API service for transcription
    apiService.processAudio(base64Audio)
    .then(response => {
      if (response && response.text) {
        setSpeechText(response.text);
      } else {
        toast({
          title: "Transcription failed",
          description: "Could not transcribe the audio. Please try again or enter text manually.",
          status: "warning",
          duration: 5000,
          isClosable: true,
        });
      }
    })
    .catch(error => {
      console.error("Error transcribing audio:", error);
      toast({
        title: "Transcription error",
        description: "An error occurred while transcribing. Please try again or enter text manually.",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    })
    .finally(() => {
      setIsProcessing(false);
    });
  };
  
  const handleSubmit = () => {
    if (!speechText.trim()) {
      toast({
        title: "Speech required",
        description: "Please enter or record your speech",
        status: "warning",
        duration: 3000,
        isClosable: true,
      });
      return;
    }
    
    onSubmit({
      text: speechText,
      audio_base64: audioBase64
    });
    
    // Reset form
    setSpeechText('');
    setAudioBase64(null);
  };
  
  return (
    <Box>
      <VStack spacing={4} align="stretch">
        <Heading size="md">Your Speech as {currentRole}</Heading>
        
        {isHuman ? (
          <>
            <AudioRecorder 
              onAudioCaptured={handleAudioCaptured} 
              isRecording={isRecording}
              setIsRecording={setIsRecording}
            />
            
            <Box borderWidth="1px" borderRadius="lg" p={4} bg="white">
              <VStack spacing={4} align="stretch">
                <Heading size="sm">Speech Text</Heading>
                
                {isProcessing ? (
                  <Flex justify="center" py={4}>
                    <Spinner />
                    <Text ml={3}>Transcribing audio...</Text>
                  </Flex>
                ) : (
                  <Textarea
                    value={speechText}
                    onChange={(e) => setSpeechText(e.target.value)}
                    placeholder="Enter your speech or record using the microphone above..."
                    rows={8}
                  />
                )}
                
                <Button
                  rightIcon={<FaPaperPlane />}
                  colorScheme="brand"
                  onClick={handleSubmit}
                  isDisabled={isRecording || isProcessing || !speechText.trim()}
                >
                  Submit Speech
                </Button>
              </VStack>
            </Box>
          </>
        ) : (
          <Box borderWidth="1px" borderRadius="lg" p={4} bg="white">
            <VStack spacing={4}>
              <Text>This position is played by AI. Click the button to generate the AI speech.</Text>
              <Button
                leftIcon={<FaRobot />}
                colorScheme="brand"
                onClick={() => onSubmit({})}
              >
                Generate AI Speech
              </Button>
            </VStack>
          </Box>
        )}
      </VStack>
    </Box>
  );
};

const DebateProgress = ({ currentSpeakerIndex, totalSpeakers, debateStatus }) => {
  const progress = (currentSpeakerIndex / totalSpeakers) * 100;
  
  return (
    <Box borderWidth="1px" borderRadius="lg" p={4} bg="white">
      <VStack spacing={4} align="stretch">
        <Heading size="md">Debate Progress</Heading>
        
        <Box>
          <Text mb={1}>
            Speaker {currentSpeakerIndex + 1} of {totalSpeakers}
            {debateStatus === 'complete' && ' (Debate Complete)'}
          </Text>
          <Progress 
            hasStripe 
            value={progress} 
            colorScheme="brand" 
            borderRadius="md"
          />
        </Box>
        
        <HStack justify="space-between">
          <Text fontSize="sm">Opening Government</Text>
          <Text fontSize="sm">Closing Opposition</Text>
        </HStack>
      </VStack>
    </Box>
  );
};

const SpeechLog = ({ speeches }) => {
  if (!speeches || speeches.length === 0) {
    return (
      <Box textAlign="center" py={4}>
        <Text color="gray.500">No speeches yet</Text>
      </Box>
    );
  }
  
  return (
    <Card>
      <CardHeader>
        <Heading size="md">Speech Log</Heading>
      </CardHeader>
      <CardBody>
        <Stack divider={<StackDivider />} spacing={4}>
          {speeches.map((speech, index) => (
            <Box key={index}>
              <Flex justify="space-between" align="center" mb={2}>
                <Heading size="sm">{speech.role}</Heading>
                <HStack>
                  <Badge colorScheme={speech.speaker === 'AI' ? 'purple' : 'green'}>
                    {speech.speaker}
                  </Badge>
                  {speech.speaker === 'AI' && speech.speech && (
                    <TextToSpeech text={speech.speech} />
                  )}
                </HStack>
              </Flex>
              <Text pt={2} fontSize="sm" whiteSpace="pre-wrap">
                {speech.speech}
              </Text>
            </Box>
          ))}
        </Stack>
      </CardBody>
    </Card>
  );
};

const DebateSessionPage = () => {
  const { debateId } = useParams();
  const navigate = useNavigate();
  const toast = useToast();
  const [debate, setDebate] = useState(null);
  const [speeches, setSpeeches] = useState([]);
  const [nextSpeaker, setNextSpeaker] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isGeneratingAI, setIsGeneratingAI] = useState(false);
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [pollInterval, setPollInterval] = useState(null);
  
  const fetchDebateStatus = async () => {
    try {
      const response = await apiService.getDebateStatus(debateId);
      
      if (response) {
        setDebate(response);
        
        // If debate is ready and there's a current speaker, get the next speaker info
        if (response.status === 'ready' && 
            response.current_speaker_index < response.total_speakers) {
          fetchNextSpeaker();
        }
        
        // If there are speeches, fetch them
        if (response.speech_log_length > 0) {
          fetchSpeeches();
        }
        
        // If debate is complete, clear interval
        if (response.status === 'complete' || 
            response.current_speaker_index >= response.total_speakers) {
          if (pollInterval) {
            clearInterval(pollInterval);
          }
        }
        
        // If there was an error in the debate
        if (response.error) {
          setError(response.error);
        }
      }
    } catch (error) {
      console.error("Error fetching debate status:", error);
      setError("Failed to fetch debate status. Please try refreshing the page.");
    } finally {
      setIsLoading(false);
    }
  };
  
  const fetchNextSpeaker = async () => {
    try {
      const response = await apiService.getNextSpeaker(debateId);
      setNextSpeaker(response);
    } catch (error) {
      console.error("Error fetching next speaker:", error);
    }
  };
  
  const fetchSpeeches = async () => {
    try {
      const response = await apiService.getSpeeches(debateId);
      setSpeeches(response);
    } catch (error) {
      console.error("Error fetching speeches:", error);
    }
  };
  
  // Start polling for debate status on component mount
  useEffect(() => {
    fetchDebateStatus();
    
    // Poll for updates every 3 seconds
    const interval = setInterval(fetchDebateStatus, 3000);
    setPollInterval(interval);
    
    return () => {
      clearInterval(interval);
    };
  }, [debateId]);
  
  const handleSpeechSubmit = async (speechData) => {
    if (nextSpeaker) {
      try {
        setIsSubmitting(true);
        
        let response;
        if (nextSpeaker.is_human) {
          // Human speech submission
          response = await apiService.submitSpeech(debateId, {
            role: nextSpeaker.role,
            text: speechData.text,
            audio_base64: speechData.audio_base64
          });
        } else {
          // AI speech generation
          setIsGeneratingAI(true);
          response = await apiService.generateAISpeech(debateId);
        }
        
        // Fetch updated state
        await fetchDebateStatus();
        await fetchSpeeches();
        await fetchNextSpeaker();
        
        toast({
          title: "Speech submitted",
          status: "success",
          duration: 3000,
          isClosable: true,
        });
      } catch (error) {
        console.error("Error submitting speech:", error);
        toast({
          title: "Error",
          description: error.message || "Failed to submit speech",
          status: "error",
          duration: 5000,
          isClosable: true,
        });
      } finally {
        setIsSubmitting(false);
        setIsGeneratingAI(false);
      }
    }
  };
  
  if (isLoading) {
    return (
      <Container maxW="container.lg" py={8}>
        <Flex direction="column" align="center" justify="center" h="50vh">
          <Spinner size="xl" color="brand.500" />
          <Text mt={4} fontSize="lg">Initializing debate session...</Text>
        </Flex>
      </Container>
    );
  }
  
  if (error) {
    return (
      <Container maxW="container.lg" py={8}>
        <Alert status="error" borderRadius="md">
          <AlertIcon />
          <AlertTitle mr={2}>Error!</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
        <Button mt={4} onClick={() => navigate('/new-debate')}>
          Start a New Debate
        </Button>
      </Container>
    );
  }
  
  const isDebateComplete = debate?.status === 'complete' || 
                          (debate?.current_speaker_index >= debate?.total_speakers);
  
  return (
    <Container maxW="container.xl" py={8}>
      <VStack spacing={8} align="stretch">
        <Box textAlign="center">
          <Badge colorScheme="brand" fontSize="md" px={3} py={1} borderRadius="full" mb={2}>
            {debate?.status === 'initializing' ? 'Initializing' : 
             isDebateComplete ? 'Complete' : 'In Progress'}
          </Badge>
          <Heading as="h1" size="xl">
            Debate Session
          </Heading>
        </Box>
        
        {debate?.status === 'initializing' ? (
          <Box textAlign="center" py={8}>
            <Spinner size="lg" />
            <Text mt={4}>
              The debate is being initialized. We're brainstorming arguments for each team...
            </Text>
          </Box>
        ) : (
          <Tabs isFitted variant="enclosed">
            <TabList mb={4}>
              <Tab>Current Speaker</Tab>
              <Tab>Speech Log</Tab>
            </TabList>
            
            <TabPanels>
              <TabPanel>
                <Flex 
                  direction={{ base: 'column', lg: 'row' }} 
                  spacing={8} 
                  gap={8}
                  align="flex-start"
                >
                  <Box flex="1">
                    {isDebateComplete ? (
                      <Box borderWidth="1px" borderRadius="lg" p={6} bg="white" textAlign="center">
                        <Heading size="md" mb={4}>Debate Complete</Heading>
                        <Text>All speakers have delivered their speeches.</Text>
                        <Button 
                          mt={6} 
                          colorScheme="brand" 
                          onClick={() => navigate('/new-debate')}
                        >
                          Start a New Debate
                        </Button>
                      </Box>
                    ) : (
                      nextSpeaker ? (
                        <SpeechInput 
                          onSubmit={handleSpeechSubmit}
                          currentRole={nextSpeaker.role}
                          isHuman={nextSpeaker.is_human}
                        />
                      ) : (
                        <Box borderWidth="1px" borderRadius="lg" p={6} bg="white" textAlign="center">
                          <Spinner />
                          <Text mt={4}>Loading next speaker...</Text>
                        </Box>
                      )
                    )}
                  </Box>
                  
                  <VStack spacing={6} width={{ base: '100%', lg: '350px' }}>
                    <DebateProgress 
                      currentSpeakerIndex={debate?.current_speaker_index || 0}
                      totalSpeakers={debate?.total_speakers || 8}
                      debateStatus={debate?.status}
                    />
                    
                    <Box borderWidth="1px" borderRadius="lg" p={4} bg="white" width="100%">
                      <VStack align="start" spacing={3}>
                        <Heading size="md">Current Speaker</Heading>
                        {nextSpeaker ? (
                          <>
                            <HStack>
                              <Text fontWeight="bold">Role:</Text>
                              <Text>{nextSpeaker.role}</Text>
                            </HStack>
                            <HStack>
                              <Text fontWeight="bold">Speaker:</Text>
                              <Badge colorScheme={nextSpeaker.is_human ? 'green' : 'purple'}>
                                {nextSpeaker.is_human ? 
                                  (nextSpeaker.nickname || 'Human') : 'AI'}
                              </Badge>
                            </HStack>
                            <HStack>
                              <Text fontWeight="bold">Position:</Text>
                              <Text>{nextSpeaker.index + 1} of {nextSpeaker.total}</Text>
                            </HStack>
                          </>
                        ) : isDebateComplete ? (
                          <Text>All speakers have delivered their speeches</Text>
                        ) : (
                          <Text>Loading speaker information...</Text>
                        )}
                      </VStack>
                    </Box>
                    
                    <Button 
                      leftIcon={<FaHistory />}
                      width="100%"
                      onClick={onOpen}
                      variant="outline"
                    >
                      View All Speeches
                    </Button>
                  </VStack>
                </Flex>
              </TabPanel>
              
              <TabPanel>
                <SpeechLog speeches={speeches} />
              </TabPanel>
            </TabPanels>
          </Tabs>
        )}
      </VStack>
      
      {/* Modal for viewing all speeches */}
      <Modal isOpen={isOpen} onClose={onClose} size="xl" scrollBehavior="inside">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Debate Speeches</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <SpeechLog speeches={speeches} />
          </ModalBody>
          <ModalFooter>
            <Button onClick={onClose}>Close</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Container>
  );
};

export default DebateSessionPage;
