import { useState, useEffect, useCallback } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Typography,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  CircularProgress,
  Alert,
  Chip,
  InputAdornment,
  IconButton,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Pagination,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import ClearIcon from '@mui/icons-material/Clear';
import { useTranslation } from 'react-i18next';
import { api } from '../../services/api';

interface Fihirana {
  id: number;
  numero: number;
  lohateny: string;
  titre: string;
  isa_andininy: number;
  collection: string;
}

interface SearchResponse {
  results: Fihirana[];
  fihiranas?: Fihirana[];
  total: number;
  limit: number;
  offset: number;
}

const FihiranaList: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  const [query, setQuery] = useState(searchParams.get('q') || '');
  const [searchType, setSearchType] = useState<'all' | 'numero' | 'title'>(
    (searchParams.get('type') as any) || 'all'
  );
  const [selectedCollection, setSelectedCollection] = useState<string>(
    searchParams.get('collection') || 'all'
  );

  const [fihiranas, setFihiranas] = useState<Fihirana[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(parseInt(searchParams.get('page') || '1'));

  const itemsPerPage = 50;

  const collections = [
    { id: 'all', label: t('common.all') },
    { id: 'FFPM', label: 'FFPM' },
    { id: 'FANAMPINY', label: t('fihirana.fanampiny') },
    { id: 'ANTEMA', label: t('fihirana.antema') },
  ];

  const searchTypes = [
    { id: 'all', label: t('common.all') },
    { id: 'numero', label: t('fihirana.byNumber') },
    { id: 'title', label: t('fihirana.byTitle') },
  ];

  const loadFihiranas = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const offset = (page - 1) * itemsPerPage;

      let response;

      if (query.trim()) {
        // Search mode
        const params: any = {
          q: query,
          limit: itemsPerPage,
          offset,
        };

        if (selectedCollection !== 'all') {
          params.collection = selectedCollection;
        }

        response = await api.get<SearchResponse>('/fihirana/search', { params });
        setFihiranas(response.data.results);
      } else {
        // List mode
        const params: any = {
          limit: itemsPerPage,
          offset,
        };

        if (selectedCollection !== 'all') {
          params.collection = selectedCollection;
        }

        response = await api.get<SearchResponse>('/fihirana', { params });
        setFihiranas(response.data.fihiranas || []);
      }

      setTotal(response.data.total);

      // Update URL params
      const newParams: any = { page: page.toString() };
      if (query) newParams.q = query;
      if (searchType !== 'all') newParams.type = searchType;
      if (selectedCollection !== 'all') newParams.collection = selectedCollection;
      setSearchParams(newParams);
    } catch (err: any) {
      setError(err.message || t('errors.loadFailed'));
      setFihiranas([]);
      setTotal(0);
    } finally {
      setLoading(false);
    }
  }, [query, selectedCollection, searchType, page, itemsPerPage, t, setSearchParams]);

  useEffect(() => {
    loadFihiranas();
  }, [loadFihiranas]);

  const handleSearch = () => {
    setPage(1);
    loadFihiranas();
  };

  const handleClear = () => {
    setQuery('');
    setSearchType('all');
    setSelectedCollection('all');
    setPage(1);
    setSearchParams({});
  };

  const handlePageChange = (_event: React.ChangeEvent<unknown>, value: number) => {
    setPage(value);
  };

  const handleFihiranaClick = (fihirana: Fihirana) => {
    navigate(`/fihirana/${fihirana.id}`);
  };

  const totalPages = Math.ceil(total / itemsPerPage);

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h4" gutterBottom>
        {t('fihirana.title')}
      </Typography>

      {/* Search/Filter Card */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box display="flex" flexDirection="column" gap={2}>
            {/* Search Input */}
            <TextField
              fullWidth
              type="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              placeholder={t('fihirana.searchPlaceholder')}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon />
                  </InputAdornment>
                ),
                endAdornment: (query || selectedCollection !== 'all') && (
                  <InputAdornment position="end">
                    <IconButton onClick={handleClear} size="small">
                      <ClearIcon />
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />

            {/* Filters */}
            <Box display="flex" gap={2} flexWrap="wrap">
              {/* Collection Filter */}
              <FormControl sx={{ minWidth: 150 }}>
                <InputLabel>{t('fihirana.collection')}</InputLabel>
                <Select
                  value={selectedCollection}
                  label={t('fihirana.collection')}
                  onChange={(e) => {
                    setSelectedCollection(e.target.value);
                    setPage(1);
                  }}
                  size="small"
                >
                  {collections.map((col) => (
                    <MenuItem key={col.id} value={col.id}>
                      {col.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              {/* Total Count */}
              <Box display="flex" alignItems="center">
                <Typography variant="body2" color="text.secondary">
                  {total} {t('fihirana.hymns')} {t('common.found')}
                </Typography>
              </Box>
            </Box>
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

      {/* Fihirana List */}
      {!loading && !error && (
        <>
          <Card>
            <List>
              {fihiranas.length === 0 ? (
                <ListItem>
                  <ListItemText
                    primary={t('fihirana.noResults')}
                    secondary={
                      query
                        ? t('fihirana.tryDifferentSearch')
                        : 'Tsy mbola misy angon-drakitra'
                    }
                  />
                </ListItem>
              ) : (
                fihiranas.map((fihirana) => (
                  <ListItem key={fihirana.id} disablePadding divider>
                    <ListItemButton onClick={() => handleFihiranaClick(fihirana)}>
                      <Box
                        display="flex"
                        alignItems="center"
                        gap={2}
                        width="100%"
                        py={0.5}
                      >
                        <Chip
                          label={`N° ${fihirana.numero || fihirana.id}`}
                          color="secondary"
                          size="small"
                        />
                        <Box flex={1}>
                          <Typography variant="body1" fontWeight="medium">
                            {fihirana.lohateny || fihirana.titre}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {fihirana.collection} • {fihirana.isa_andininy}{' '}
                            {t('fihirana.verses')}
                          </Typography>
                        </Box>
                      </Box>
                    </ListItemButton>
                  </ListItem>
                ))
              )}
            </List>
          </Card>

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
    </Box>
  );
};

export default FihiranaList;
