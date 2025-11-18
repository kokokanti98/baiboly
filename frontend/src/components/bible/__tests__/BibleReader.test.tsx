/**
 * TDD Tests for BibleReader component.
 * These tests must FAIL initially, then pass after implementation.
 * Constitutional requirement: TDD workflow enforced.
 */
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import BibleReader from '../BibleReader';

// Mock API calls
jest.mock('../../../services/api', () => ({
  api: {
    get: jest.fn(),
  },
}));

import { api } from '../../../services/api';
const mockApi = api as jest.Mocked<typeof api>;

describe('BibleReader Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  const renderWithRouter = (component: React.ReactElement) => {
    return render(<BrowserRouter>{component}</BrowserRouter>);
  };

  it('should render loading state initially', () => {
    mockApi.get.mockImplementation(() => new Promise(() => {})); // Never resolves

    renderWithRouter(<BibleReader />);

    expect(screen.getByText(/mahandrasa/i)).toBeInTheDocument(); // "Loading" in Malagasy
  });

  it('should display list of Bible books', async () => {
    const mockLivres = [
      { id: 1, nom: 'Genesisy', abbrev: 'Gen', testament: 'AT', ordre: 1 },
      { id: 2, nom: 'Eksodosy', abbrev: 'Exo', testament: 'AT', ordre: 2 },
    ];

    mockApi.get.mockResolvedValue({ data: mockLivres });

    renderWithRouter(<BibleReader />);

    await waitFor(() => {
      expect(screen.getByText('Genesisy')).toBeInTheDocument();
      expect(screen.getByText('Eksodosy')).toBeInTheDocument();
    });
  });

  it('should filter books by testament', async () => {
    const mockLivres = [
      { id: 1, nom: 'Genesisy', abbrev: 'Gen', testament: 'AT', ordre: 1 },
      { id: 40, nom: 'Matio', abbrev: 'Mat', testament: 'NT', ordre: 40 },
    ];

    mockApi.get.mockResolvedValue({ data: mockLivres });

    renderWithRouter(<BibleReader />);

    await waitFor(() => {
      expect(screen.getByText('Genesisy')).toBeInTheDocument();
    });

    // Click on "Testamenta Vaovao" (New Testament) filter
    const ntFilter = screen.getByText(/testamenta vaovao/i);
    fireEvent.click(ntFilter);

    await waitFor(() => {
      expect(screen.queryByText('Genesisy')).not.toBeInTheDocument();
      expect(screen.getByText('Matio')).toBeInTheDocument();
    });
  });

  it('should navigate to book when clicked', async () => {
    const mockLivres = [
      { id: 1, nom: 'Genesisy', abbrev: 'Gen', testament: 'AT', ordre: 1 },
    ];

    mockApi.get.mockResolvedValue({ data: mockLivres });

    renderWithRouter(<BibleReader />);

    await waitFor(() => {
      expect(screen.getByText('Genesisy')).toBeInTheDocument();
    });

    const bookButton = screen.getByText('Genesisy');
    fireEvent.click(bookButton);

    // Should navigate to chapters view (test will verify navigation behavior)
    await waitFor(() => {
      expect(mockApi.get).toHaveBeenCalledWith('/bible/livres/1/chapitres');
    });
  });

  it('should display chapters when book is selected', async () => {
    const mockChapitres = [
      { id: 1, numero: 1, livre_id: 1 },
      { id: 2, numero: 2, livre_id: 1 },
    ];

    mockApi.get.mockResolvedValue({ data: mockChapitres });

    renderWithRouter(<BibleReader livreId={1} />);

    await waitFor(() => {
      expect(screen.getByText(/toko 1/i)).toBeInTheDocument(); // "Chapter 1"
      expect(screen.getByText(/toko 2/i)).toBeInTheDocument(); // "Chapter 2"
    });
  });

  it('should display verses when chapter is selected', async () => {
    const mockVersets = [
      { id: 1, numero: 1, texte: "Tamin'ny voalohany Andriamanitra nahary ny lanitra sy ny tany.", chapitre_id: 1 },
      { id: 2, numero: 2, texte: "Ny tany dia tsy nisy endrika sady foana.", chapitre_id: 1 },
    ];

    mockApi.get.mockResolvedValue({ data: mockVersets });

    renderWithRouter(<BibleReader chapitreId={1} />);

    await waitFor(() => {
      expect(screen.getByText(/tamin'ny voalohany andriamanitra/i)).toBeInTheDocument();
      expect(screen.getByText(/ny tany dia tsy nisy endrika/i)).toBeInTheDocument();
    });
  });

  it('should display verse numbers', async () => {
    const mockVersets = [
      { id: 1, numero: 1, texte: "Tamin'ny voalohany Andriamanitra nahary ny lanitra sy ny tany.", chapitre_id: 1 },
    ];

    mockApi.get.mockResolvedValue({ data: mockVersets });

    renderWithRouter(<BibleReader chapitreId={1} />);

    await waitFor(() => {
      expect(screen.getByText('1')).toBeInTheDocument(); // Verse number
    });
  });

  it('should handle API errors gracefully', async () => {
    mockApi.get.mockRejectedValue(new Error('Network error'));

    renderWithRouter(<BibleReader />);

    await waitFor(() => {
      expect(screen.getByText(/nisy olana/i)).toBeInTheDocument(); // "Error" in Malagasy
    });
  });

  it('should display error message in Malagasy', async () => {
    mockApi.get.mockRejectedValue(new Error('Network error'));

    renderWithRouter(<BibleReader />);

    await waitFor(() => {
      const errorMessage = screen.getByText(/nisy olana|tsy afaka/i);
      expect(errorMessage).toBeInTheDocument();
    });
  });

  it('should have accessible navigation buttons', async () => {
    const mockLivres = [
      { id: 1, nom: 'Genesisy', abbrev: 'Gen', testament: 'AT', ordre: 1 },
    ];

    mockApi.get.mockResolvedValue({ data: mockLivres });

    renderWithRouter(<BibleReader />);

    await waitFor(() => {
      const button = screen.getByText('Genesisy');
      expect(button).toHaveAttribute('role', 'button');
      // Constitutional requirement: ≥44px touch targets
      expect(button).toHaveStyle({ minHeight: '44px', minWidth: '44px' });
    });
  });

  it('should display book abbreviations', async () => {
    const mockLivres = [
      { id: 1, nom: 'Genesisy', abbrev: 'Gen', testament: 'AT', ordre: 1 },
    ];

    mockApi.get.mockResolvedValue({ data: mockLivres });

    renderWithRouter(<BibleReader />);

    await waitFor(() => {
      expect(screen.getByText(/gen/i)).toBeInTheDocument();
    });
  });

  it('should support keyboard navigation', async () => {
    const mockLivres = [
      { id: 1, nom: 'Genesisy', abbrev: 'Gen', testament: 'AT', ordre: 1 },
    ];

    mockApi.get.mockResolvedValue({ data: mockLivres });

    renderWithRouter(<BibleReader />);

    await waitFor(() => {
      const button = screen.getByText('Genesisy');
      expect(button).toHaveAttribute('tabIndex', '0');
    });
  });

  it('should render responsive layout on mobile', async () => {
    // Mock mobile viewport
    global.innerWidth = 375;
    global.innerHeight = 667;

    const mockLivres = [
      { id: 1, nom: 'Genesisy', abbrev: 'Gen', testament: 'AT', ordre: 1 },
    ];

    mockApi.get.mockResolvedValue({ data: mockLivres });

    const { container } = renderWithRouter(<BibleReader />);

    await waitFor(() => {
      expect(screen.getByText('Genesisy')).toBeInTheDocument();
    });

    // Check that component uses responsive container
    const mainContainer = container.querySelector('[data-testid="bible-reader"]');
    expect(mainContainer).toHaveClass(/responsive|mobile|container/i);
  });
});
