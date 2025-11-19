import { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  Alert,
  Chip,
  Pagination,
  InputAdornment,
  IconButton,
  Divider,
  ListItemButton,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import ClearIcon from '@mui/icons-material/Clear';
import { useTranslation } from 'react-i18next';
import { api } from '../../services/api';

interface SearchResult {
  id: number;
  numero: number;
  titre: string;
  paroles: string;
  collection: string;
}

interface SearchResponse {
  results: SearchResult[];
  total: number;
  limit: number;
  offset: number;
  query: string;
}

const FihiranaSearch: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [hasSearched, setHasSearched] = useState(false);
  const resultsPerPage = 20;

  const performSearch = useCallback(async (searchQuery: string, pageNum: number = 1) => {
    if (!searchQuery.trim()) {
      setError(t('errors.searchFailed') || 'Ilaina ny query');
      return;
    }

    setLoading(true);
    setError(null);
    setHasSearched(true);

    try {
      const offset = (pageNum - 1) * resultsPerPage;
      const response = await api.get<SearchResponse>('/fihirana/search', {
        params: {
          q: searchQuery,
          limit: resultsPerPage,
          offset,
        },
      });

      setResults(response.data.results);
      setTotal(response.data.total);
      setPage(pageNum);
    } catch (err: any) {
      setError(err.message || t('errors.searchFailed'));
      setResults([]);
      setTotal(0);
    } finally {
      setLoading(false);
    }
  }, [t, resultsPerPage]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    performSearch(query, 1);
  };

  const handleClear = () => {
    setQuery('');
    setResults([]);
    setTotal(0);
    setError(null);
    setHasSearched(false);
    setPage(1);
  };

  const handlePageChange = (_event: React.ChangeEvent<unknown>, value: number) => {
    performSearch(query, value);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const highlightQuery = (text: string, searchQuery: string): JSX.Element => {
    if (!searchQuery.trim()) {
      return <>{text}</>;
    }

    const parts = text.split(new RegExp(`(${searchQuery})`, 'gi'));
    return (
      <>
        {parts.map((part, index) =>
          part.toLowerCase() === searchQuery.toLowerCase() ? (
            <Box
              key={index}
              component="span"
              sx={{
                backgroundColor: 'secondary.light',
                color: 'secondary.contrastText',
                fontWeight: 'bold',
                padding: '2px 4px',
                borderRadius: '4px',
              }}
            >
              {part}
            </Box>
          ) : (
            <span key={index}>{part}</span>
          )
        )}
      </>
    );
  };

  const totalPages = Math.ceil(total / resultsPerPage);

  return (
    <Box data-testid="fihirana-search" sx={{ p: 2 }}>
      {/* Header */}
      <Typography variant="h4" gutterBottom>
        {t('fihirana.searchPlaceholder')}
      </Typography>

      {/* Search Form */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <form onSubmit={handleSearch}>
            <Box display="flex" gap={2}>
              <TextField
                fullWidth
                type="search"
                role="searchbox"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder={t('fihirana.searchPlaceholder')}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SearchIcon />
                    </InputAdornment>
                  ),
                  endAdornment: query && (
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
                color="secondary"
                disabled={!query.trim() || loading}
                sx={{ minWidth: 44, minHeight: 44, px: 3 }}
              >
                {t('common.search')}
              </Button>
            </Box>
          </form>
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

      {/* Results Summary */}
      {!loading && hasSearched && (
        <Box mb={2}>
          <Typography variant="body1" color="text.secondary">
            {total > 0
              ? `${total} ${t('fihirana.hymns')} hita`
              : t('fihirana.noResults')}
          </Typography>
        </Box>
      )}

      {/* Search Results */}
      {!loading && results.length > 0 && (
        <>
          <List>
            {results.map((result) => (
              <Card
                key={result.id}
                sx={{
                  mb: 2,
                  cursor: 'pointer',
                  transition: 'transform 0.2s, box-shadow 0.2s',
                  '&:hover': {
                    transform: 'translateY(-2px)',
                    boxShadow: 4,
                  },
                }}
                onClick={() => navigate(`/fihirana/${result.id}`)}
              >
                <ListItemButton alignItems="flex-start">
                  <ListItemText
                    primary={
                      <Box display="flex" alignItems="center" gap={1} mb={1}>
                        <Chip
                          label={`N° ${result.numero}`}
                          size="small"
                          color="secondary"
                        />
                        <Typography variant="h6" component="span">
                          {highlightQuery(result.titre, query)}
                        </Typography>
                        <Chip
                          label={result.collection}
                          size="small"
                          variant="outlined"
                        />
                      </Box>
                    }
                    secondary={
                      <Typography
                        component="span"
                        variant="body2"
                        color="text.primary"
                        sx={{ lineHeight: 1.8, display: 'block', mt: 1 }}
                      >
                        {highlightQuery(
                          result.paroles.substring(0, 200) + (result.paroles.length > 200 ? '...' : ''),
                          query
                        )}
                      </Typography>
                    }
                  />
                </ListItemButton>
              </Card>
            ))}
          </List>

          {/* Pagination */}
          {totalPages > 1 && (
            <Box display="flex" justifyContent="center" mt={3}>
              <Pagination
                count={totalPages}
                page={page}
                onChange={handlePageChange}
                color="secondary"
                size="large"
                showFirstButton
                showLastButton
              />
            </Box>
          )}
        </>
      )}

      {/* No Results */}
      {!loading && hasSearched && results.length === 0 && !error && (
        <Card>
          <CardContent>
            <Typography variant="body1" color="text.secondary" textAlign="center">
              {t('fihirana.noResults')}
            </Typography>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default FihiranaSearch;
