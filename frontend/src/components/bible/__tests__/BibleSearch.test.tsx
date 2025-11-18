/**
 * TDD Tests for BibleSearch component.
 * These tests must FAIL initially, then pass after implementation.
 * Constitutional requirement: TDD workflow enforced.
 */
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrowserRouter } from 'react-router-dom';
import BibleSearch from '../BibleSearch';

// Mock API calls
jest.mock('../../../services/api', () => ({
  api: {
    get: jest.fn(),
  },
}));

import { api } from '../../../services/api';
const mockApi = api as jest.Mocked<typeof api>;

describe('BibleSearch Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  const renderWithRouter = (component: React.ReactElement) => {
    return render(<BrowserRouter>{component}</BrowserRouter>);
  };

  it('should render search input with Malagasy placeholder', () => {
    renderWithRouter(<BibleSearch />);

    const searchInput = screen.getByPlaceholderText(/karohy/i); // "Search" in Malagasy
    expect(searchInput).toBeInTheDocument();
  });

  it('should have accessible search input', () => {
    renderWithRouter(<BibleSearch />);

    const searchInput = screen.getByRole('searchbox') || screen.getByRole('textbox');
    expect(searchInput).toBeInTheDocument();
    expect(searchInput).toHaveAttribute('type', 'search');
  });

  it('should update input value on user typing', async () => {
    const user = userEvent.setup();
    renderWithRouter(<BibleSearch />);

    const searchInput = screen.getByPlaceholderText(/karohy/i) as HTMLInputElement;
    await user.type(searchInput, 'Andriamanitra');

    expect(searchInput.value).toBe('Andriamanitra');
  });

  it('should trigger search on form submit', async () => {
    const user = userEvent.setup();
    mockApi.get.mockResolvedValue({ data: { results: [], total: 0 } });

    renderWithRouter(<BibleSearch />);

    const searchInput = screen.getByPlaceholderText(/karohy/i);
    await user.type(searchInput, 'Andriamanitra');

    const searchButton = screen.getByRole('button', { name: /karohy/i });
    await user.click(searchButton);

    await waitFor(() => {
      expect(mockApi.get).toHaveBeenCalledWith('/bible/search', expect.objectContaining({
        params: expect.objectContaining({ q: 'Andriamanitra' }),
      }));
    });
  });

  it('should display search results', async () => {
    const mockResults = {
      results: [
        {
          id: 1,
          numero: 1,
          texte: "Tamin'ny voalohany Andriamanitra nahary ny lanitra sy ny tany.",
          livre: { nom: 'Genesisy', abbrev: 'Gen' },
          chapitre: { numero: 1 },
        },
      ],
      total: 1,
    };

    mockApi.get.mockResolvedValue({ data: mockResults });

    renderWithRouter(<BibleSearch />);

    const searchInput = screen.getByPlaceholderText(/karohy/i);
    fireEvent.change(searchInput, { target: { value: 'Andriamanitra' } });
    fireEvent.submit(searchInput.closest('form')!);

    await waitFor(() => {
      expect(screen.getByText(/tamin'ny voalohany andriamanitra/i)).toBeInTheDocument();
      expect(screen.getByText(/Genesisy/i)).toBeInTheDocument();
      expect(screen.getByText(/1:1/)).toBeInTheDocument(); // Reference: Gen 1:1
    });
  });

  it('should display no results message when search returns empty', async () => {
    mockApi.get.mockResolvedValue({ data: { results: [], total: 0 } });

    renderWithRouter(<BibleSearch />);

    const searchInput = screen.getByPlaceholderText(/karohy/i);
    fireEvent.change(searchInput, { target: { value: 'nonexistent' } });
    fireEvent.submit(searchInput.closest('form')!);

    await waitFor(() => {
      expect(screen.getByText(/tsy nahita vokatra/i)).toBeInTheDocument(); // "No results found"
    });
  });

  it('should display loading state during search', async () => {
    mockApi.get.mockImplementation(() => new Promise(() => {})); // Never resolves

    renderWithRouter(<BibleSearch />);

    const searchInput = screen.getByPlaceholderText(/karohy/i);
    fireEvent.change(searchInput, { target: { value: 'test' } });
    fireEvent.submit(searchInput.closest('form')!);

    expect(screen.getByText(/mahandrasa/i)).toBeInTheDocument(); // "Loading"
  });

  it('should handle search errors gracefully', async () => {
    mockApi.get.mockRejectedValue(new Error('Network error'));

    renderWithRouter(<BibleSearch />);

    const searchInput = screen.getByPlaceholderText(/karohy/i);
    fireEvent.change(searchInput, { target: { value: 'test' } });
    fireEvent.submit(searchInput.closest('form')!);

    await waitFor(() => {
      expect(screen.getByText(/nisy olana tamin'ny fikarohana/i)).toBeInTheDocument(); // "Search error"
    });
  });

  it('should prevent search with empty query', async () => {
    const user = userEvent.setup();
    renderWithRouter(<BibleSearch />);

    const searchButton = screen.getByRole('button', { name: /karohy/i });
    await user.click(searchButton);

    // Should not call API with empty query
    expect(mockApi.get).not.toHaveBeenCalled();
  });

  it('should highlight search term in results', async () => {
    const mockResults = {
      results: [
        {
          id: 1,
          numero: 1,
          texte: "Tamin'ny voalohany Andriamanitra nahary ny lanitra sy ny tany.",
          livre: { nom: 'Genesisy', abbrev: 'Gen' },
          chapitre: { numero: 1 },
        },
      ],
      total: 1,
    };

    mockApi.get.mockResolvedValue({ data: mockResults });

    renderWithRouter(<BibleSearch />);

    const searchInput = screen.getByPlaceholderText(/karohy/i);
    fireEvent.change(searchInput, { target: { value: 'Andriamanitra' } });
    fireEvent.submit(searchInput.closest('form')!);

    await waitFor(() => {
      const highlightedText = screen.getByText('Andriamanitra');
      expect(highlightedText).toHaveClass(/highlight|mark|bold/i);
    });
  });

  it('should support pagination in search results', async () => {
    const mockResults = {
      results: Array.from({ length: 20 }, (_, i) => ({
        id: i + 1,
        numero: i + 1,
        texte: `Verset ${i + 1} avec Andriamanitra`,
        livre: { nom: 'Genesisy', abbrev: 'Gen' },
        chapitre: { numero: 1 },
      })),
      total: 50,
    };

    mockApi.get.mockResolvedValue({ data: mockResults });

    renderWithRouter(<BibleSearch />);

    const searchInput = screen.getByPlaceholderText(/karohy/i);
    fireEvent.change(searchInput, { target: { value: 'Andriamanitra' } });
    fireEvent.submit(searchInput.closest('form')!);

    await waitFor(() => {
      expect(screen.getByText(/verset 1/i)).toBeInTheDocument();
    });

    // Should show pagination controls
    const nextButton = screen.getByRole('button', { name: /manaraka|next/i });
    expect(nextButton).toBeInTheDocument();
  });

  it('should load next page on pagination click', async () => {
    const user = userEvent.setup();
    const mockPage1 = {
      results: [{ id: 1, numero: 1, texte: 'Result 1', livre: { nom: 'Gen' }, chapitre: { numero: 1 } }],
      total: 20,
    };
    const mockPage2 = {
      results: [{ id: 2, numero: 2, texte: 'Result 2', livre: { nom: 'Gen' }, chapitre: { numero: 1 } }],
      total: 20,
    };

    mockApi.get.mockResolvedValueOnce({ data: mockPage1 }).mockResolvedValueOnce({ data: mockPage2 });

    renderWithRouter(<BibleSearch />);

    const searchInput = screen.getByPlaceholderText(/karohy/i);
    fireEvent.change(searchInput, { target: { value: 'test' } });
    fireEvent.submit(searchInput.closest('form')!);

    await waitFor(() => {
      expect(screen.getByText('Result 1')).toBeInTheDocument();
    });

    const nextButton = screen.getByRole('button', { name: /manaraka|next/i });
    await user.click(nextButton);

    await waitFor(() => {
      expect(screen.getByText('Result 2')).toBeInTheDocument();
    });
  });

  it('should support filtering by testament', async () => {
    const user = userEvent.setup();
    mockApi.get.mockResolvedValue({ data: { results: [], total: 0 } });

    renderWithRouter(<BibleSearch />);

    // Select testament filter
    const testamentFilter = screen.getByLabelText(/testamenta/i) || screen.getByRole('combobox');
    await user.selectOptions(testamentFilter, 'AT');

    const searchInput = screen.getByPlaceholderText(/karohy/i);
    await user.type(searchInput, 'test');
    fireEvent.submit(searchInput.closest('form')!);

    await waitFor(() => {
      expect(mockApi.get).toHaveBeenCalledWith('/bible/search', expect.objectContaining({
        params: expect.objectContaining({ testament: 'AT' }),
      }));
    });
  });

  it('should display verse reference as clickable link', async () => {
    const mockResults = {
      results: [
        {
          id: 1,
          numero: 1,
          texte: "Tamin'ny voalohany Andriamanitra nahary ny lanitra sy ny tany.",
          livre: { id: 1, nom: 'Genesisy', abbrev: 'Gen' },
          chapitre: { id: 1, numero: 1 },
        },
      ],
      total: 1,
    };

    mockApi.get.mockResolvedValue({ data: mockResults });

    renderWithRouter(<BibleSearch />);

    const searchInput = screen.getByPlaceholderText(/karohy/i);
    fireEvent.change(searchInput, { target: { value: 'Andriamanitra' } });
    fireEvent.submit(searchInput.closest('form')!);

    await waitFor(() => {
      const referenceLink = screen.getByRole('link', { name: /gen 1:1/i });
      expect(referenceLink).toBeInTheDocument();
      expect(referenceLink).toHaveAttribute('href', expect.stringContaining('/bible'));
    });
  });

  it('should meet touch target size requirements', () => {
    renderWithRouter(<BibleSearch />);

    const searchButton = screen.getByRole('button', { name: /karohy/i });
    // Constitutional requirement: ≥44px touch targets
    expect(searchButton).toHaveStyle({ minHeight: '44px', minWidth: '44px' });
  });

  it('should be responsive on mobile devices', () => {
    // Mock mobile viewport
    global.innerWidth = 375;
    global.innerHeight = 667;

    const { container } = renderWithRouter(<BibleSearch />);

    const searchContainer = container.querySelector('[data-testid="bible-search"]');
    expect(searchContainer).toHaveClass(/responsive|mobile|container/i);
  });

  it('should debounce search input', async () => {
    jest.useFakeTimers();
    const user = userEvent.setup({ delay: null });
    mockApi.get.mockResolvedValue({ data: { results: [], total: 0 } });

    renderWithRouter(<BibleSearch enableAutoSearch />);

    const searchInput = screen.getByPlaceholderText(/karohy/i);
    await user.type(searchInput, 'Andriamanitra');

    // Should not call API immediately
    expect(mockApi.get).not.toHaveBeenCalled();

    // Fast-forward time by 500ms (typical debounce delay)
    jest.advanceTimersByTime(500);

    await waitFor(() => {
      expect(mockApi.get).toHaveBeenCalledTimes(1);
    });

    jest.useRealTimers();
  });
});
