import { useState, useEffect } from 'react';
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
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import { api } from '../../services/api';

interface Livre {
  id: number;
  nom: string;
  abbrev: string;
  testament: string;
  ordre: number;
}

interface Chapitre {
  id: number;
  numero: number;
  livre_id: number;
}

interface Verset {
  id: number;
  numero: number;
  texte: string;
  chapitre_id: number;
}

interface BibleReaderProps {
  livreId?: number;
  chapitreId?: number;
}

const BibleReader: React.FC<BibleReaderProps> = ({ livreId, chapitreId }) => {
  const { t } = useTranslation();
  const [livres, setLivres] = useState<Livre[]>([]);
  const [chapitres, setChapitres] = useState<Chapitre[]>([]);
  const [versets, setVersets] = useState<Verset[]>([]);
  const [selectedLivre, setSelectedLivre] = useState<Livre | null>(null);
  const [selectedChapitre, setSelectedChapitre] = useState<Chapitre | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [testamentFilter, setTestamentFilter] = useState<string | null>(null);

  // Load all books on mount
  useEffect(() => {
    loadLivres();
  }, []);

  // Load specific livre if livreId provided
  useEffect(() => {
    if (livreId) {
      loadLivreDetails(livreId);
    }
  }, [livreId]);

  // Load specific chapitre if chapitreId provided
  useEffect(() => {
    if (chapitreId) {
      loadChapitreDetails(chapitreId);
    }
  }, [chapitreId]);

  const loadLivres = async (testament?: string) => {
    setLoading(true);
    setError(null);
    try {
      const params = testament ? { testament } : {};
      const response = await api.get('/bible/livres', { params });
      setLivres(response.data);
    } catch (err: any) {
      setError(err.message || t('errors.loadFailed'));
    } finally {
      setLoading(false);
    }
  };

  const loadLivreDetails = async (id: number) => {
    setLoading(true);
    setError(null);
    try {
      const [livreRes, chapitresRes] = await Promise.all([
        api.get(`/bible/livres/${id}`),
        api.get(`/bible/livres/${id}/chapitres`),
      ]);
      setSelectedLivre(livreRes.data);
      setChapitres(chapitresRes.data);
      setVersets([]);
      setSelectedChapitre(null);
    } catch (err: any) {
      setError(err.message || t('errors.loadFailed'));
    } finally {
      setLoading(false);
    }
  };

  const loadChapitreDetails = async (id: number) => {
    setLoading(true);
    setError(null);
    try {
      const [chapitreRes, versetsRes] = await Promise.all([
        api.get(`/bible/chapitres/${id}`),
        api.get(`/bible/chapitres/${id}/versets`),
      ]);
      setSelectedChapitre(chapitreRes.data);
      setVersets(versetsRes.data);
    } catch (err: any) {
      setError(err.message || t('errors.loadFailed'));
    } finally {
      setLoading(false);
    }
  };

  const handleLivreClick = (livre: Livre) => {
    loadLivreDetails(livre.id);
  };

  const handleChapitreClick = (chapitre: Chapitre) => {
    loadChapitreDetails(chapitre.id);
  };

  const handleTestamentFilter = (testament: string | null) => {
    setTestamentFilter(testament);
    loadLivres(testament || undefined);
    setSelectedLivre(null);
    setChapitres([]);
    setVersets([]);
  };

  const handleBack = () => {
    if (versets.length > 0) {
      // Go back to chapters view
      setVersets([]);
      setSelectedChapitre(null);
    } else if (chapitres.length > 0) {
      // Go back to books view
      setChapitres([]);
      setSelectedLivre(null);
    }
  };

  if (loading && livres.length === 0) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
        <Typography ml={2}>{t('common.loading')}</Typography>
      </Box>
    );
  }

  return (
    <Box data-testid="bible-reader" sx={{ p: 2 }}>
      {/* Header */}
      <Box mb={3}>
        <Typography variant="h4" gutterBottom>
          {t('bible.title')}
        </Typography>

        {/* Testament Filter */}
        {!selectedLivre && (
          <Box display="flex" gap={1} mt={2}>
            <Chip
              label={t('bible.oldTestament')}
              onClick={() => handleTestamentFilter('AT')}
              color={testamentFilter === 'AT' ? 'primary' : 'default'}
              sx={{ minWidth: 44, minHeight: 44 }}
            />
            <Chip
              label={t('bible.newTestament')}
              onClick={() => handleTestamentFilter('NT')}
              color={testamentFilter === 'NT' ? 'primary' : 'default'}
              sx={{ minWidth: 44, minHeight: 44 }}
            />
            <Chip
              label={t('common.all') || 'Rehetra'}
              onClick={() => handleTestamentFilter(null)}
              color={!testamentFilter ? 'primary' : 'default'}
              sx={{ minWidth: 44, minHeight: 44 }}
            />
          </Box>
        )}

        {/* Breadcrumb Navigation */}
        {(selectedLivre || selectedChapitre) && (
          <Box mt={2} display="flex" alignItems="center" gap={1}>
            <Chip
              label={t('common.back')}
              onClick={handleBack}
              sx={{ minWidth: 44, minHeight: 44 }}
            />
            {selectedLivre && (
              <Typography variant="body1">
                {selectedLivre.nom}
                {selectedChapitre && ` ${t('bible.chapter')} ${selectedChapitre.numero}`}
              </Typography>
            )}
          </Box>
        )}
      </Box>

      {/* Error Message */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* Books List */}
      {!selectedLivre && livres.length > 0 && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              {t('bible.books')} ({livres.length})
            </Typography>
            <List>
              {livres.map((livre) => (
                <ListItem key={livre.id} disablePadding>
                  <ListItemButton
                    onClick={() => handleLivreClick(livre)}
                    sx={{ minHeight: 44 }}
                  >
                    <ListItemText
                      primary={livre.nom}
                      secondary={livre.abbrev}
                    />
                    <Chip
                      label={livre.testament}
                      size="small"
                      color={livre.testament === 'AT' ? 'primary' : 'secondary'}
                    />
                  </ListItemButton>
                </ListItem>
              ))}
            </List>
          </CardContent>
        </Card>
      )}

      {/* Chapters List */}
      {selectedLivre && chapitres.length > 0 && versets.length === 0 && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              {t('bible.chapters')} - {selectedLivre.nom}
            </Typography>
            <Box display="flex" flexWrap="wrap" gap={1}>
              {chapitres.map((chapitre) => (
                <Chip
                  key={chapitre.id}
                  label={chapitre.numero}
                  onClick={() => handleChapitreClick(chapitre)}
                  color="primary"
                  variant="outlined"
                  sx={{ minWidth: 44, minHeight: 44, fontSize: '1rem' }}
                />
              ))}
            </Box>
          </CardContent>
        </Card>
      )}

      {/* Verses Display */}
      {versets.length > 0 && selectedChapitre && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              {selectedLivre?.nom} {t('bible.chapter')} {selectedChapitre.numero}
            </Typography>
            <Divider sx={{ my: 2 }} />
            <Box>
              {versets.map((verset) => (
                <Box key={verset.id} display="flex" mb={2}>
                  <Typography
                    variant="caption"
                    color="primary"
                    sx={{
                      fontWeight: 'bold',
                      minWidth: 40,
                      mt: 0.5,
                    }}
                  >
                    {verset.numero}
                  </Typography>
                  <Typography variant="body1" sx={{ lineHeight: 1.8 }}>
                    {verset.texte}
                  </Typography>
                </Box>
              ))}
            </Box>
          </CardContent>
        </Card>
      )}

      {/* Loading Indicator */}
      {loading && (livres.length > 0 || chapitres.length > 0 || versets.length > 0) && (
        <Box display="flex" justifyContent="center" mt={2}>
          <CircularProgress size={24} />
        </Box>
      )}
    </Box>
  );
};

export default BibleReader;
