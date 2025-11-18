import { Box, Container, Typography, Card, CardContent, CardActionArea, Grid } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import MenuBookIcon from '@mui/icons-material/MenuBook';
import MusicNoteIcon from '@mui/icons-material/MusicNote';

const HomePage: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();

  return (
    <Container maxWidth="md">
      <Box sx={{ py: 8, textAlign: 'center' }}>
        <Typography variant="h2" component="h1" gutterBottom color="primary">
          Baiboly
        </Typography>
        <Typography variant="h5" color="text.secondary" paragraph>
          Mamaky Baiboly sy Fihirana amin'ny teny Malagasy
        </Typography>

        <Grid container spacing={4} sx={{ mt: 4 }}>
          {/* Bible Card */}
          <Grid item xs={12} md={6}>
            <Card elevation={3}>
              <CardActionArea
                onClick={() => navigate('/bible')}
                sx={{
                  minHeight: 200,
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'center',
                  alignItems: 'center',
                  p: 4,
                }}
              >
                <MenuBookIcon sx={{ fontSize: 80, color: 'primary.main', mb: 2 }} />
                <CardContent>
                  <Typography variant="h4" component="h2" gutterBottom>
                    {t('navigation.bible')}
                  </Typography>
                  <Typography variant="body1" color="text.secondary">
                    Mamaky sy mikatsaka amin'ny Baiboly Masina
                  </Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>

          {/* Fihirana Card */}
          <Grid item xs={12} md={6}>
            <Card elevation={3}>
              <CardActionArea
                onClick={() => navigate('/fihirana')}
                sx={{
                  minHeight: 200,
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'center',
                  alignItems: 'center',
                  p: 4,
                }}
              >
                <MusicNoteIcon sx={{ fontSize: 80, color: 'secondary.main', mb: 2 }} />
                <CardContent>
                  <Typography variant="h4" component="h2" gutterBottom>
                    {t('navigation.fihirana')}
                  </Typography>
                  <Typography variant="body1" color="text.secondary">
                    Fihirana FFPM, Fanampiny, Antema
                  </Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
        </Grid>

        <Box sx={{ mt: 6 }}>
          <Typography variant="body2" color="text.secondary">
            © 2025 Baiboly - Mamaky Baiboly sy Fihirana amin'ny teny Malagasy
          </Typography>
        </Box>
      </Box>
    </Container>
  );
};

export default HomePage;
