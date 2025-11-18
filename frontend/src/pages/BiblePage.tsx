import { useState } from 'react';
import { Box, Tabs, Tab, Container } from '@mui/material';
import MenuBookIcon from '@mui/icons-material/MenuBook';
import SearchIcon from '@mui/icons-material/Search';
import BookmarkIcon from '@mui/icons-material/Bookmark';
import BibleReader from '../components/Bible/BibleReader';
import BibleSearch from '../components/Bible/BibleSearch';
import BibleReferenceSearch from '../components/Bible/BibleReferenceSearch';
import { useTranslation } from 'react-i18next';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`bible-tabpanel-${index}`}
      aria-labelledby={`bible-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

const BiblePage: React.FC = () => {
  const { t } = useTranslation();
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <Box>
      <Container maxWidth="lg">
        {/* Tabs for switching between reader, search, and reference */}
        <Box sx={{ borderBottom: 1, borderColor: 'divider', mt: 2, mb: 2 }}>
          <Tabs
            value={tabValue}
            onChange={handleTabChange}
            aria-label="Bible navigation tabs"
            centered
          >
            <Tab
              icon={<MenuBookIcon />}
              iconPosition="start"
              label={t('bible.title')}
              id="bible-tab-0"
              aria-controls="bible-tabpanel-0"
              sx={{ minHeight: 48, fontSize: '1rem' }}
            />
            <Tab
              icon={<BookmarkIcon />}
              iconPosition="start"
              label="Référence"
              id="bible-tab-1"
              aria-controls="bible-tabpanel-1"
              sx={{ minHeight: 48, fontSize: '1rem' }}
            />
            <Tab
              icon={<SearchIcon />}
              iconPosition="start"
              label={t('common.search')}
              id="bible-tab-2"
              aria-controls="bible-tabpanel-2"
              sx={{ minHeight: 48, fontSize: '1rem' }}
            />
          </Tabs>
        </Box>

        <TabPanel value={tabValue} index={0}>
          <BibleReader />
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <BibleReferenceSearch />
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          <BibleSearch />
        </TabPanel>
      </Container>
    </Box>
  );
};

export default BiblePage;
