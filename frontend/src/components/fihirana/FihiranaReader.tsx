import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  CircularProgress,
  Alert,
  Chip,
  Divider,
  Grid,
  Button,
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import { api } from '../../services/api';

interface Fihirana {
  id: number;
  numero: number;
  titre: string;
  paroles: string;
  collection: string;
}

interface FihiranaReaderProps {
  fihiranaId?: number;
}

const FihiranaReader: React.FC<FihiranaReaderProps> = ({ fihiranaId }) => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [fihiranas, setFihiranas] = useState<Fihirana[]>([]);
  const [selectedFihirana, setSelectedFihirana] = useState<Fihirana | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedCollection, setSelectedCollection] = useState<string>('all');

  const collections = [
    { id: 'all', label: t('common.all') },
    { id: 'ffpm', label: t('fihirana.ffpm') },
    { id: 'fanampiny', label: t('fihirana.fanampiny') },
    { id: 'antema', label: t('fihirana.antema') },
  ];

  useEffect(() => {
    loadFihiranas();
  }, [selectedCollection]);

  useEffect(() => {
    if (fihiranaId && fihiranas.length > 0) {
      const fihirana = fihiranas.find(f => f.id === fihiranaId);
      if (fihirana) {
        setSelectedFihirana(fihirana);
      }
    }
  }, [fihiranaId, fihiranas]);

  const loadFihiranas = async () => {
    setLoading(true);
    setError(null);
    try {
      const params: any = {
        limit: 200,
        offset: 0,
      };

      if (selectedCollection !== 'all') {
        params.collection = selectedCollection.toUpperCase();
      }

      const response = await api.get('/fihirana', { params });
      setFihiranas(response.data.fihiranas);

      if (response.data.fihiranas.length === 0) {
        setError(t('fihirana.noResults') || 'Tsy hita fihirana');
      }
    } catch (err: any) {
      setError(err.message || t('errors.loadFailed'));
      setFihiranas([]);
    } finally {
      setLoading(false);
    }
  };

  const handleFihiranaClick = (fihirana: Fihirana) => {
    setSelectedFihirana(fihirana);
  };

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h4" gutterBottom>
        {t('fihirana.title')}
      </Typography>

      {/* Collection Filter */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="subtitle1" gutterBottom>
            {t('fihirana.collections')}
          </Typography>
          <Box display="flex" gap={1} flexWrap="wrap">
            {collections.map((collection) => (
              <Chip
                key={collection.id}
                label={collection.label}
                onClick={() => setSelectedCollection(collection.id)}
                color={selectedCollection === collection.id ? 'primary' : 'default'}
                sx={{ cursor: 'pointer' }}
              />
            ))}
          </Box>
        </CardContent>
      </Card>

      {/* Error Message */}
      {error && (
        <Alert severity="info" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* Loading */}
      {loading && (
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
          <CircularProgress />
          <Typography ml={2}>{t('common.loading')}</Typography>
        </Box>
      )}

      {/* Fihirana List and Display */}
      {!loading && !error && (
        <Grid container spacing={3}>
          {/* Fihirana List */}
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {t('fihirana.hymns')}
                </Typography>
                <List sx={{ maxHeight: '600px', overflow: 'auto' }}>
                  {fihiranas.length === 0 ? (
                    <ListItem>
                      <ListItemText
                        primary={t('fihirana.noResults')}
                        secondary="Tsy mbola misy angon-drakitra"
                      />
                    </ListItem>
                  ) : (
                    fihiranas.map((fihirana) => (
                      <ListItem key={fihirana.id} disablePadding>
                        <ListItemButton
                          selected={selectedFihirana?.id === fihirana.id}
                          onClick={() => navigate(`/fihirana/${fihirana.id}`)}
                        >
                          <ListItemText
                            primary={`${fihirana.numero}. ${fihirana.titre}`}
                            secondary={fihirana.collection}
                          />
                        </ListItemButton>
                      </ListItem>
                    ))
                  )}
                </List>
              </CardContent>
            </Card>
          </Grid>

          {/* Fihirana Display */}
          <Grid item xs={12} md={8}>
            {selectedFihirana ? (
              <Card>
                <CardContent>
                  <Box display="flex" alignItems="center" gap={2} mb={2}>
                    <Chip label={`N° ${selectedFihirana.numero}`} color="primary" />
                    <Typography variant="h5">{selectedFihirana.titre}</Typography>
                  </Box>
                  <Divider sx={{ my: 2 }} />
                  <Typography
                    variant="body1"
                    sx={{
                      whiteSpace: 'pre-line',
                      lineHeight: 1.8,
                      fontFamily: 'Georgia, serif',
                    }}
                  >
                    {selectedFihirana.paroles}
                  </Typography>
                </CardContent>
              </Card>
            ) : (
              <Card>
                <CardContent>
                  <Typography variant="body1" color="text.secondary" textAlign="center">
                    Safidio fihirana iray eo amin'ny lisitra
                  </Typography>
                </CardContent>
              </Card>
            )}
          </Grid>
        </Grid>
      )}
    </Box>
  );
};

export default FihiranaReader;
