import { useState } from 'react';
import { Box, Tabs, Tab, Container } from '@mui/material';
import MusicNoteIcon from '@mui/icons-material/MusicNote';
import SearchIcon from '@mui/icons-material/Search';
import FihiranaReader from '../components/fihirana/FihiranaReader';
import FihiranaSearch from '../components/fihirana/FihiranaSearch';
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
      id={`fihirana-tabpanel-${index}`}
      aria-labelledby={`fihirana-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );
}

const FihiranaPage: React.FC = () => {
  const { t } = useTranslation();
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <Box>
      <Container maxWidth="lg">
        {/* Tabs for switching between reader and search */}
        <Box sx={{ borderBottom: 1, borderColor: 'divider', mt: 2, mb: 2 }}>
          <Tabs
            value={tabValue}
            onChange={handleTabChange}
            aria-label="Fihirana navigation tabs"
            centered
          >
            <Tab
              icon={<MusicNoteIcon />}
              iconPosition="start"
              label={t('fihirana.title')}
              id="fihirana-tab-0"
              aria-controls="fihirana-tabpanel-0"
              sx={{ minHeight: 48, fontSize: '1rem' }}
            />
            <Tab
              icon={<SearchIcon />}
              iconPosition="start"
              label={t('common.search')}
              id="fihirana-tab-1"
              aria-controls="fihirana-tabpanel-1"
              sx={{ minHeight: 48, fontSize: '1rem' }}
            />
          </Tabs>
        </Box>

        <TabPanel value={tabValue} index={0}>
          <FihiranaReader />
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <FihiranaSearch />
        </TabPanel>
      </Container>
    </Box>
  );
};

export default FihiranaPage;
