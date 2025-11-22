import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { Box } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';
import theme from './theme';
import Header from './components/Layout/Header';
import HomePage from './pages/HomePage';
import BiblePage from './pages/BiblePage';
import FihiranaPage from './pages/FihiranaPage';
import FihiranaDetail from './components/Fihirana/FihiranaDetail';


function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
          <Header />
          <Box component="main" sx={{ flexGrow: 1 }}>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/bible" element={<BiblePage />} />
              <Route path="/fihirana" element={<FihiranaPage />} />
              <Route path="/fihirana/:id" element={<FihiranaDetail />} />
            </Routes>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
