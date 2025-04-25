import React, { useState, useEffect } from 'react';
import { Box, Button, HStack, Text, useToast } from '@chakra-ui/react';
import { FaPlay, FaPause, FaStop } from 'react-icons/fa';

// Web Speech API for text-to-speech
const TextToSpeech = ({ text, autoPlay = false }) => {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [utterance, setUtterance] = useState(null);
  const toast = useToast();

  useEffect(() => {
    // Initialize speech synthesis
    if (!text) return;
    
    const synth = window.speechSynthesis;
    const newUtterance = new SpeechSynthesisUtterance(text);
    
    // Configure voice settings
    newUtterance.rate = 1.0; // Speed of speech
    newUtterance.pitch = 1.0; // Pitch of voice
    newUtterance.volume = 1.0; // Volume
    
    // Try to get a good voice
    const voices = synth.getVoices();
    const preferredVoice = voices.find(voice => 
      voice.name.includes('English') && 
      (voice.name.includes('Male') || voice.name.includes('UK'))
    );
    
    if (preferredVoice) {
      newUtterance.voice = preferredVoice;
    }
    
    // Set up event handlers
    newUtterance.onend = () => {
      setIsSpeaking(false);
      setIsPaused(false);
    };
    
    newUtterance.onerror = (event) => {
      console.error('Speech synthesis error:', event);
      setIsSpeaking(false);
      setIsPaused(false);
      toast({
        title: "Speech Error",
        description: "There was an error playing the speech",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    };
    
    setUtterance(newUtterance);
    
    // Auto-play if enabled
    if (autoPlay) {
      synth.cancel(); // Cancel any ongoing speech
      synth.speak(newUtterance);
      setIsSpeaking(true);
    }
    
    // Clean up
    return () => {
      synth.cancel();
    };
  }, [text, autoPlay, toast]);

  const handlePlay = () => {
    if (!utterance) return;
    
    const synth = window.speechSynthesis;
    
    if (isPaused) {
      synth.resume();
      setIsPaused(false);
    } else {
      synth.cancel(); // Cancel any ongoing speech
      synth.speak(utterance);
    }
    
    setIsSpeaking(true);
  };

  const handlePause = () => {
    if (!utterance || !isSpeaking) return;
    
    const synth = window.speechSynthesis;
    synth.pause();
    setIsPaused(true);
  };

  const handleStop = () => {
    if (!utterance) return;
    
    const synth = window.speechSynthesis;
    synth.cancel();
    setIsSpeaking(false);
    setIsPaused(false);
  };

  return (
    <Box>
      <HStack spacing={2}>
        {!isSpeaking ? (
          <Button 
            leftIcon={<FaPlay />} 
            size="sm" 
            colorScheme="green" 
            onClick={handlePlay}
          >
            Play Speech
          </Button>
        ) : isPaused ? (
          <Button 
            leftIcon={<FaPlay />} 
            size="sm" 
            colorScheme="green" 
            onClick={handlePlay}
          >
            Resume
          </Button>
        ) : (
          <Button 
            leftIcon={<FaPause />} 
            size="sm" 
            colorScheme="yellow" 
            onClick={handlePause}
          >
            Pause
          </Button>
        )}
        
        {(isSpeaking || isPaused) && (
          <Button 
            leftIcon={<FaStop />} 
            size="sm" 
            colorScheme="red" 
            onClick={handleStop}
          >
            Stop
          </Button>
        )}
      </HStack>
    </Box>
  );
};

export default TextToSpeech;
