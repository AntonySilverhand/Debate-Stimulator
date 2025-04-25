import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Box } from '@chakra-ui/react';

// Pages
import HomePage from './pages/HomePage';
import NewDebatePage from './pages/NewDebatePage';
import DebateSessionPage from './pages/DebateSessionPage';
import HistoryPage from './pages/HistoryPage';

// Components
import Header from './components/Header';
import Footer from './components/Footer';

function App() {
  return (
    <Router>
      <Box minH="100vh" display="flex" flexDirection="column">
        <Header />
        <Box flex="1" py={8} px={4}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/new-debate" element={<NewDebatePage />} />
            <Route path="/debate/:debateId" element={<DebateSessionPage />} />
            <Route path="/history" element={<HistoryPage />} />
          </Routes>
        </Box>
        <Footer />
      </Box>
    </Router>
  );
}

export default App;
