import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import MenuBookIcon from '@mui/icons-material/MenuBook';
import MusicNoteIcon from '@mui/icons-material/MusicNote';
import HomeIcon from '@mui/icons-material/Home';
import { useTranslation } from 'react-i18next';

const Header: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <AppBar position="static" color="primary" elevation={2}>
      <Toolbar>
        {/* Logo/Title */}
        <Typography
          variant="h5"
          component="div"
          sx={{
            flexGrow: 0,
            fontWeight: 'bold',
            mr: 4,
            cursor: 'pointer',
          }}
          onClick={() => navigate('/')}
        >
          Baiboly
        </Typography>

        {/* Navigation Buttons */}
        <Box sx={{ flexGrow: 1, display: 'flex', gap: 1 }}>
          <Button
            color="inherit"
            startIcon={<HomeIcon />}
            onClick={() => navigate('/')}
            sx={{
              backgroundColor: isActive('/') ? 'rgba(255, 255, 255, 0.2)' : 'transparent',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
              },
            }}
          >
            {t('common.home')}
          </Button>

          <Button
            color="inherit"
            startIcon={<MenuBookIcon />}
            onClick={() => navigate('/bible')}
            sx={{
              backgroundColor: isActive('/bible') ? 'rgba(255, 255, 255, 0.2)' : 'transparent',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
              },
            }}
          >
            {t('navigation.bible')}
          </Button>

          <Button
            color="inherit"
            startIcon={<MusicNoteIcon />}
            onClick={() => navigate('/fihirana')}
            sx={{
              backgroundColor: isActive('/fihirana') ? 'rgba(255, 255, 255, 0.2)' : 'transparent',
              '&:hover': {
                backgroundColor: 'rgba(255, 255, 255, 0.1)',
              },
            }}
          >
            {t('navigation.fihirana')}
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
