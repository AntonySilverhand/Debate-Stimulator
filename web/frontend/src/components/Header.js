import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Box, Flex, Heading, Button, HStack, useColorModeValue } from '@chakra-ui/react';
import { FaHome, FaPlus, FaHistory } from 'react-icons/fa';

const Header = () => {
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  return (
    <Box as="header" bg={bgColor} borderBottom="1px" borderColor={borderColor} py={4} px={6} boxShadow="sm">
      <Flex justify="space-between" align="center" maxW="1200px" mx="auto">
        <Flex align="center">
          <Heading as="h1" size="lg" fontFamily="heading" letterSpacing="tight">
            Debate Stimulator
          </Heading>
        </Flex>
        
        <HStack spacing={4}>
          <Button as={RouterLink} to="/" leftIcon={<FaHome />} variant="ghost" size="sm">
            Home
          </Button>
          <Button as={RouterLink} to="/new-debate" leftIcon={<FaPlus />} variant="ghost" size="sm">
            New Debate
          </Button>
          <Button as={RouterLink} to="/history" leftIcon={<FaHistory />} variant="ghost" size="sm">
            History
          </Button>
        </HStack>
      </Flex>
    </Box>
  );
};

export default Header;
