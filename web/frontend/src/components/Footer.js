import React from 'react';
import { Box, Text, Link, Flex, useColorModeValue } from '@chakra-ui/react';

const Footer = () => {
  const bgColor = useColorModeValue('white', 'gray.800');
  const borderColor = useColorModeValue('gray.200', 'gray.700');

  return (
    <Box as="footer" bg={bgColor} borderTop="1px" borderColor={borderColor} py={4} px={6}>
      <Flex direction="column" align="center" maxW="1200px" mx="auto">
        <Text fontSize="sm" color="gray.500">
          Debate Stimulator - Practice British Parliamentary debate with AI opponents
        </Text>
        <Text fontSize="xs" color="gray.400" mt={1}>
          &copy; {new Date().getFullYear()} - Created by Antony
        </Text>
      </Flex>
    </Box>
  );
};

export default Footer;
