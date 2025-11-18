import { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Alert,
  CircularProgress,
  Chip,
  Divider,
  InputAdornment,
  IconButton,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import ClearIcon from '@mui/icons-material/Clear';
import { useTranslation } from 'react-i18next';
import { api } from '../../services/api';

interface Verset {
  id: number;
  numero: number;
  texte: string;
  chapitre: {
    id: number;
    numero: number;
  };
  livre: {
    id: number;
    nom: string;
    abbrev: string;
    testament: string;
  };
}

interface ReferenceResult {
  versets: Verset[];
  reference: string;
  livre: {
    id: number;
    nom: string;
    abbrev: string;
    testament: string;
    ordre: number;
  };
  chapitre: number;
  verset_debut: number;
  verset_fin: number;
  count: number;
}

const BibleReferenceSearch: React.FC = () => {
  const { t } = useTranslation();
  const [reference, setReference] = useState('');
  const [result, setResult] = useState<ReferenceResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!reference.trim()) {
      setError('Ampidiro ny référence (ohatra: Genesis 1:1-3)');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await api.get<ReferenceResult>('/bible/reference-range', {
        params: { ref: reference },
      });

      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.error || err.message || t('errors.searchFailed'));
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setReference('');
    setResult(null);
    setError(null);
  };

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h4" gutterBottom>
        Karohy amin'ny référence
      </Typography>

      {/* Search Form */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <form onSubmit={handleSearch}>
            <Box display="flex" gap={2}>
              <TextField
                fullWidth
                type="text"
                value={reference}
                onChange={(e) => setReference(e.target.value)}
                placeholder="Ohatra: Genesis 1:1-3, Genesisy 1:5-7, Mat 5:1-10"
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon />
                    </InputAdornment>
                  ),
                  endAdornment: reference && (
                    <InputAdornment position="end">
                      <IconButton onClick={handleClear} size="small">
                        <ClearIcon />
                      </IconButton>
                    </InputAdornment>
                  ),
                  sx: { minHeight: 44 },
                }}
              />
              <Button
                type="submit"
                variant="contained"
                color="primary"
                disabled={!reference.trim() || loading}
                sx={{ minWidth: 44, minHeight: 44, px: 3 }}
              >
                {t('common.search')}
              </Button>
            </Box>
          </form>

          {/* Help text */}
          <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
            Format: Boky Toko:Andininy-Andininy (ohatra: "Genesis 1:1-5" na "Genesisy 1:1-3")
          </Typography>
        </CardContent>
      </Card>

      {/* Error Message */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
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

      {/* Results */}
      {result && !loading && (
        <Card>
          <CardContent>
            {/* Reference Header */}
            <Box display="flex" alignItems="center" gap={2} mb={3}>
              <Chip
                label={result.livre.testament}
                color={result.livre.testament === 'AT' ? 'primary' : 'secondary'}
                size="small"
              />
              <Typography variant="h5" component="h2">
                {result.reference}
              </Typography>
              <Chip
                label={`${result.count} andininy`}
                size="small"
                variant="outlined"
              />
            </Box>

            <Divider sx={{ mb: 3 }} />

            {/* Verses */}
            <Box>
              {result.versets.map((verset, index) => (
                <Box
                  key={verset.id}
                  sx={{
                    mb: 2,
                    pb: 2,
                    borderBottom: index < result.versets.length - 1 ? '1px solid' : 'none',
                    borderColor: 'divider'
                  }}
                >
                  <Box display="flex" alignItems="flex-start" gap={2}>
                    <Chip
                      label={verset.numero}
                      size="small"
                      color="primary"
                      sx={{ mt: 0.5 }}
                    />
                    <Typography
                      variant="body1"
                      sx={{
                        lineHeight: 1.8,
                        flex: 1,
                        fontFamily: 'Georgia, serif',
                        fontSize: '1.1rem'
                      }}
                    >
                      {verset.texte}
                    </Typography>
                  </Box>
                </Box>
              ))}
            </Box>

            {/* Book info footer */}
            <Divider sx={{ my: 2 }} />
            <Typography variant="caption" color="text.secondary">
              {result.livre.nom} - {result.livre.testament === 'AT' ? 'Testamenta Taloha' : 'Testamenta Vaovao'}
            </Typography>
          </CardContent>
        </Card>
      )}

      {/* No results placeholder when nothing searched yet */}
      {!result && !loading && !error && (
        <Card>
          <CardContent>
            <Typography variant="body1" color="text.secondary" textAlign="center">
              Ampidiro ny référence Bible eo ambony (ohatra: "Genesis 1:1-3")
            </Typography>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default BibleReferenceSearch;
