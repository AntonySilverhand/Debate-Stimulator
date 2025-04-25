import React from 'react';
import ReactDOM from 'react-dom/client';
import { ChakraProvider, extendTheme } from '@chakra-ui/react';
import App from './App';

// Extend the theme to include custom colors, fonts, etc
const theme = extendTheme({
  colors: {
    brand: {
      50: '#f0e4ff',
      100: '#d1c2ff',
      200: '#b29dff',
      300: '#9277ff',
      400: '#7551ff',
      500: '#5a2cf9',
      600: '#4c22dd',
      700: '#3c19b4',
      800: '#2d108a',
      900: '#1d0862',
    },
  },
  fonts: {
    heading: '"Times New Roman", serif',
    body: 'system-ui, sans-serif',
  },
  styles: {
    global: {
      body: {
        bg: 'gray.50',
        color: 'gray.800',
      },
    },
  },
});

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ChakraProvider theme={theme}>
      <App />
    </ChakraProvider>
  </React.StrictMode>
);
