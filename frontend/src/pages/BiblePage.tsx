import { useState } from 'react';
import { Box, Tabs, Tab, Container } from '@mui/material';
import BibleReader from '../components/Bible/BibleReader';
import BibleSearch from '../components/Bible/BibleSearch';
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
    <Container maxWidth="lg">
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          aria-label="Bible navigation tabs"
        >
          <Tab
            label={t('bible.title')}
            id="bible-tab-0"
            aria-controls="bible-tabpanel-0"
            sx={{ minHeight: 44 }}
          />
          <Tab
            label={t('common.search')}
            id="bible-tab-1"
            aria-controls="bible-tabpanel-1"
            sx={{ minHeight: 44 }}
          />
        </Tabs>
      </Box>

      <TabPanel value={tabValue} index={0}>
        <BibleReader />
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <BibleSearch />
      </TabPanel>
    </Container>
  );
};

export default BiblePage;
