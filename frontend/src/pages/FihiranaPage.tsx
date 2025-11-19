import { Box, Container } from '@mui/material';
import FihiranaList from '../components/Fihirana/FihiranaList';

const FihiranaPage: React.FC = () => {
  return (
    <Box>
      <Container maxWidth="lg">
        <FihiranaList />
      </Container>
    </Box>
  );
};

export default FihiranaPage;
