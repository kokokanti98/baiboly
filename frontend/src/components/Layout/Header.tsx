import { AppBar, Toolbar, Typography, Button, Box, useMediaQuery, useTheme } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import MenuBookIcon from '@mui/icons-material/MenuBook';
import MusicNoteIcon from '@mui/icons-material/MusicNote';
import HomeIcon from '@mui/icons-material/Home';
import { useTranslation } from 'react-i18next';

const Header: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const location = useLocation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

  const isActive = (path: string) => location.pathname === path;

  return (
    <AppBar position="static" color="primary" elevation={2}>
      <Toolbar sx={{ gap: { xs: 0.5, sm: 1 } }}>
        {/* Navigation Buttons */}
        <Box sx={{ flexGrow: 1, display: 'flex', gap: { xs: 0.5, sm: 1 } }}>
          <Button
            color="inherit"
            startIcon={isMobile ? undefined : <HomeIcon />}
            onClick={() => navigate('/')}
            sx={{
              backgroundColor: isActive('/') ? 'rgba(255, 255, 255, 0.2)' : 'transparent',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
              },
              fontSize: { xs: '0.75rem', sm: '0.875rem' },
              px: { xs: 1, sm: 2 },
              minWidth: { xs: 'auto', sm: '64px' },
            }}
          >
            {t('common.home')}
          </Button>

          <Button
            color="inherit"
            startIcon={isMobile ? undefined : <MenuBookIcon />}
            onClick={() => navigate('/bible')}
            sx={{
              backgroundColor: isActive('/bible') ? 'rgba(255, 255, 255, 0.2)' : 'transparent',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
              },
              fontSize: { xs: '0.75rem', sm: '0.875rem' },
              px: { xs: 1, sm: 2 },
              minWidth: { xs: 'auto', sm: '64px' },
            }}
          >
            {t('navigation.bible')}
          </Button>

          <Button
            color="inherit"
            startIcon={isMobile ? undefined : <MusicNoteIcon />}
            onClick={() => navigate('/fihirana')}
            sx={{
              backgroundColor: isActive('/fihirana') ? 'rgba(255, 255, 255, 0.2)' : 'transparent',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
              },
              fontSize: { xs: '0.75rem', sm: '0.875rem' },
              px: { xs: 1, sm: 2 },
              minWidth: { xs: 'auto', sm: '64px' },
            }}
          >
            Fihirana
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
