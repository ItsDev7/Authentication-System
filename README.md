# Authentication System

A modern authentication system built with FastAPI backend and CustomTkinter frontend, featuring user registration, login, and license management.

## 🎥 Demo

[![Watch the video](https://img.youtube.com/vi/oIKoWrUiLvI/0.jpg)](https://www.youtube.com/watch?v=oIKoWrUiLvI)

## Features

- 🔐 Secure user authentication
- 📝 User registration with validation
- 🔑 License key management
- 🎨 Modern UI with CustomTkinter
- 🐳 Docker containerization
- 📊 PostgreSQL database
- 🔄 Database migrations with Alembic

## Prerequisites

Before you begin, ensure you have the following installed:

- [Python 3.9+](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/downloads)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ItsDev7/Authentication-System.git
cd Authentication-System
```

2. Create and configure environment files:

```bash
# Create .env file in the root directory
cp .env.example .env

# Edit .env with your database credentials
# Example:
# POSTGRES_DB=mydb
# POSTGRES_USER=myuser
# POSTGRES_PASSWORD=mypassword
# POSTGRES_PORT=5432
# DATABASE_URL=postgresql+psycopg2://myuser:mypassword@db:5432/mydb
```

## Running the Application

### Backend Setup

1. Start the backend services using Docker:

```bash
# Windows
./start.backend.bat

# Linux/Mac
chmod +x start.backend.sh
./start.backend.sh
```

2. Verify backend is running:

- API Documentation: http://localhost:8000/docs
- API Base URL: http://localhost:8000

### Frontend Setup

1. Create and activate virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the frontend application:

```bash
# Windows
./start.ui.bat

# Linux/Mac
chmod +x start.ui.sh
./start.ui.sh
```

## License Management

To manage license codes, visit the API documentation at http://localhost:8000/docs and use the following endpoints:

### Generate License Codes

1. **Generate Single Code**:

   - Go to `/license/generate`
   - Click "Try it out"
   - Set `duration_days` (default: 30)
   - Click "Execute"
   - Copy the generated code

2. **Generate Multiple Codes**:
   - Go to `/license/generate-batch`
   - Click "Try it out"
   - Set `count` (number of codes)
   - Set `duration_days` (default: 30)
   - Click "Execute"
   - Copy the generated codes

### View License Codes

- Go to `/license/list`
- Click "Try it out"
- Click "Execute"
- View all available license codes

## Development

### Database Migrations

To create a new migration:

```bash
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Adding New Features

1. Backend:

   - Add new models in `backend/app/models/`
   - Create schemas in `backend/app/schemas/`
   - Add routes in `backend/app/routes/`
   - Implement services in `backend/app/services/`

2. Frontend:
   - Create new UI components in `frontend/`
   - Update existing views as needed

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
