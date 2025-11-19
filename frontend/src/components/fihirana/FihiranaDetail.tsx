import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Alert,
  Button,
  Chip,
  Divider,
  IconButton,
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import MusicNoteIcon from '@mui/icons-material/MusicNote';
import { useTranslation } from 'react-i18next';
import { api } from '../../services/api';

interface Tononkira {
  id: number;
  hira_id: number;
  andininy: number;
  tononkira: string;
  fiverenany: boolean;
}

interface HymnDetail {
  id: number;
  numero: number;
  lohateny: string;
  titre: string;
  isa_andininy: number;
  mpanoratra?: string;
  collection: string;
  tononkira?: Tononkira[];
  paroles?: string;
}

const FihiranaDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { t } = useTranslation();
  const [hymn, setHymn] = useState<HymnDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHymn = async () => {
      if (!id) return;

      setLoading(true);
      setError(null);

      try {
        const response = await api.get<HymnDetail>(`/fihirana/${id}`);
        setHymn(response.data);
      } catch (err: any) {
        setError(err.message || 'Erreur lors du chargement');
      } finally {
        setLoading(false);
      }
    };

    fetchHymn();
  }, [id]);

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="400px"
      >
        <CircularProgress />
        <Typography ml={2}>{t('common.loading')}</Typography>
      </Box>
    );
  }

  if (error || !hymn) {
    return (
      <Box p={2}>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate(-1)}
          sx={{ mb: 2 }}
        >
          {t('common.back')}
        </Button>
        <Alert severity="error">{error || 'Fihirana tsy hita'}</Alert>
      </Box>
    );
  }

  return (
    <Box data-testid="fihirana-detail" sx={{ p: 2 }}>
      {/* Back button */}
      <Button
        startIcon={<ArrowBackIcon />}
        onClick={() => navigate(-1)}
        sx={{ mb: 2 }}
      >
        {t('common.back')}
      </Button>

      {/* Hymn Card */}
      <Card>
        <CardContent>
          {/* Header */}
          <Box display="flex" alignItems="center" gap={2} mb={3}>
            <IconButton
              sx={{
                bgcolor: 'secondary.light',
                color: 'secondary.contrastText',
                '&:hover': { bgcolor: 'secondary.main' },
              }}
            >
              <MusicNoteIcon />
            </IconButton>
            <Box flex={1}>
              <Box display="flex" alignItems="center" gap={1} mb={1}>
                <Chip
                  label={`N° ${hymn.numero}`}
                  color="secondary"
                  size="small"
                />
                <Chip
                  label={hymn.collection}
                  variant="outlined"
                  size="small"
                />
                {hymn.isa_andininy && (
                  <Chip
                    label={`${hymn.isa_andininy} andininy`}
                    variant="outlined"
                    size="small"
                  />
                )}
              </Box>
              <Typography variant="h4" component="h1">
                {hymn.lohateny || hymn.titre}
              </Typography>
              {hymn.mpanoratra && (
                <Typography variant="body2" color="text.secondary" mt={1}>
                  Mpanoratra: {hymn.mpanoratra}
                </Typography>
              )}
            </Box>
          </Box>

          <Divider sx={{ my: 3 }} />

          {/* Verses */}
          {hymn.tononkira && hymn.tononkira.length > 0 ? (
            <Box>
              {hymn.tononkira.map((verse, index) => (
                <Box key={verse.id} mb={3}>
                  {verse.fiverenany ? (
                    /* Refrain */
                    <Box
                      sx={{
                        bgcolor: 'secondary.light',
                        p: 2,
                        borderRadius: 1,
                        borderLeft: 4,
                        borderColor: 'secondary.main',
                      }}
                    >
                      <Typography
                        variant="subtitle2"
                        color="secondary.contrastText"
                        fontWeight="bold"
                        mb={1}
                      >
                        Fiverenana:
                      </Typography>
                      <Typography
                        variant="body1"
                        sx={{
                          whiteSpace: 'pre-line',
                          lineHeight: 1.8,
                          color: 'secondary.contrastText',
                        }}
                      >
                        {verse.tononkira}
                      </Typography>
                    </Box>
                  ) : (
                    /* Regular verse */
                    <Box>
                      <Typography
                        variant="h6"
                        color="secondary.main"
                        gutterBottom
                      >
                        {verse.andininy}.
                      </Typography>
                      <Typography
                        variant="body1"
                        sx={{
                          whiteSpace: 'pre-line',
                          lineHeight: 1.8,
                          pl: 2,
                        }}
                      >
                        {verse.tononkira}
                      </Typography>
                    </Box>
                  )}

                  {/* Don't add divider after last verse */}
                  {index < hymn.tononkira.length - 1 && (
                    <Divider sx={{ mt: 3 }} />
                  )}
                </Box>
              ))}
            </Box>
          ) : (
            /* Fallback for legacy format */
            hymn.paroles && (
              <Typography
                variant="body1"
                sx={{
                  whiteSpace: 'pre-line',
                  lineHeight: 1.8,
                }}
              >
                {hymn.paroles}
              </Typography>
            )
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default FihiranaDetail;
