# Baiboly - Malagasy Bible & Hymnal Reader

A responsive web/mobile application for reading the Bible and evangelical hymns in Malagasy.

## 🚀 Quick Start

### Start Application (Docker)

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Access Services
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:5000
- **API Health Check:** http://localhost:5000/api/health

### Stop Application
```bash
docker-compose down
```

## 📚 Documentation

- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - Complete project documentation (READ THIS FIRST for new sessions)
- **[backend/SETUP.md](backend/SETUP.md)** - Detailed backend setup instructions
- **[specs/001-bible-hymnal-reader/spec.md](specs/001-bible-hymnal-reader/spec.md)** - Feature specification
- **[.specify/memory/constitution.md](.specify/memory/constitution.md)** - Project constitution

## 🛠 Technology Stack

- **Backend:** Python 3.9+, Flask 3.x, PostgreSQL 13+, SQLAlchemy 2.x
- **Frontend:** React 18+, TypeScript 5+, Vite, Material-UI v5
- **Infrastructure:** Docker, Docker Compose
- **Testing:** pytest (≥80% coverage), Jest + RTL (≥75% coverage)
- **Language:** Malagasy (default)

## 🏗 Project Structure

```
baiboly/
├── backend/          # Flask API
├── frontend/         # React application
├── specs/            # Project specifications
├── .specify/         # Constitution & memory
├── docker-compose.yml
├── start.sh / start.bat
└── PROJECT_OVERVIEW.md
```

## 📋 Current Status

**Phase 3 - User Story 1: Bible Reading Feature** (In Progress)

- ✅ Phase 1-2: Setup & Foundational tasks completed
- ✅ TDD tests written (80+ tests)
- ✅ Bible models & services implemented
- ⏳ API endpoints implementation (next)
- ⏳ Frontend components (pending)
- ⏳ Data import (pending)

See [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for detailed status.

## 🧪 Testing

**Backend:**
```bash
docker-compose exec backend pytest
docker-compose exec backend pytest --cov=src
```

**Frontend:**
```bash
docker-compose exec frontend npm test
docker-compose exec frontend npm test -- --coverage
```

## 🔧 Development

### View Logs
```bash
docker-compose logs -f              # All services
docker-compose logs -f backend      # Backend only
docker-compose logs -f frontend     # Frontend only
```

### Database Management
Start pgAdmin:
```bash
docker-compose --profile tools up -d pgadmin
```
Access: http://localhost:5050 (admin@baiboly.local / admin)

### Rebuild Containers
```bash
docker-compose up --build -d
```

## 📖 Features

### User Story 1: Bible Reading (Current)
- Display all Bible books (66 books)
- Filter by testament (Old/New)
- Browse chapters and verses
- Full-text search across verses
- Reference-based lookup (e.g., "Gen 1:1")
- Responsive mobile/desktop layout

### User Story 2: Fihirana (Next)
- Display hymns from 3 collections (FFPM, Fanampiny, Antema)
- Search by number or content
- Display complete hymn lyrics

### User Story 3: Navigation (Next)
- Home page navigation
- Persistent navigation bar
- Responsive menu

## 📊 Data Sources

- **Bible:** [baiboly-json](https://github.com/RaveloMevaSoavina/baiboly-json) (66 books in Malagasy)
- **Fihirana:** [Fihirana-FFPM](https://github.com/Rohan29-AN/Fihirana-FFPM) (3 collections)

## 🤝 Contributing

1. Write tests first (TDD)
2. Run tests before committing
3. Follow code style (black, ESLint, Prettier)
4. All UI text in Malagasy
5. Reference task IDs in commits

## 📜 License

[Specify license here]

---

**For detailed project information, architecture, and development guidelines, read [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)**
