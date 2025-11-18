import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import theme from './theme';
import HomePage from './pages/HomePage';
import BiblePage from './pages/BiblePage';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/bible" element={<BiblePage />} />
          <Route path="/fihirana" element={<div>Fihirana Page - Coming Soon</div>} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
