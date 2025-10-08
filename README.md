# 🎵 Music Microservices Platform

A microservices-based music platform built with FastAPI, demonstrating modern backend architecture patterns.

## 🏗️ Architecture

This project consists of three independent microservices:

### 1. User Service (Port 8001)
Handles user authentication and management.
- User registration
- User login
- Profile management

### 2. Music Service (Port 8002)
Manages music catalog including songs, artists, and albums.
- Add/remove songs
- Artist management
- Album cataloging

### 3. Playlist Service (Port 8003)
Creates and manages user playlists.
- Create playlists
- Add/remove songs from playlists
- Share playlists

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Database:** SQLite (can be upgraded to PostgreSQL)
- **Language:** Python 3.9+
- **API Documentation:** Swagger UI (auto-generated)

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/music-microservices.git
cd music-microservices
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running Services

**User Service:**
```bash
cd user-service
uvicorn main:app --reload --port 8001
```
Access API docs: http://localhost:8001/docs

**Music Service:**
```bash
cd music-service
uvicorn main:app --reload --port 8002
```
Access API docs: http://localhost:8002/docs

**Playlist Service:**
```bash
cd playlist-service
uvicorn main:app --reload --port 8003
```
Access API docs: http://localhost:8003/docs

## 📚 API Documentation

Each service has auto-generated interactive API documentation available at `/docs` endpoint.

### User Service Endpoints
- `POST /users/register` - Register new user
- `POST /users/login` - Login user
- `GET /users` - Get all users
- `GET /users/{id}` - Get user by ID
- `DELETE /users/{id}` - Delete user

### Music Service Endpoints
- `POST /songs` - Add new song
- `GET /songs` - Get all songs
- `GET /songs/{id}` - Get song by ID
- `PUT /songs/{id}` - Update song
- `DELETE /songs/{id}` - Delete song

### Playlist Service Endpoints
- `POST /playlists` - Create playlist
- `GET /playlists` - Get all playlists
- `GET /playlists/{id}` - Get playlist by ID
- `POST /playlists/{id}/songs` - Add song to playlist
- `DELETE /playlists/{id}` - Delete playlist

## 🧪 Testing

Run tests for each service:
```bash
pytest user-service/tests
pytest music-service/tests
pytest playlist-service/tests
```

## 🐳 Docker Support (Coming Soon)

Run all services with Docker Compose:
```bash
docker-compose up
```

## 📂 Project Structure

```
music-microservices/
├── user-service/          # User authentication service
├── music-service/         # Music catalog service
├── playlist-service/      # Playlist management service
├── shared/               # Shared utilities
├── docs/                 # Documentation
├── README.md
└── requirements.txt
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Christyan Simbolon**
- GitHub: [@chrisimbolon](https://github.com/chrisimbolon)
- Portfolio: [chrisimbolon.dev](https://chrisimbolon.dev)

## 🎯 Learning Goals

This project demonstrates:
- ✅ Microservices architecture
- ✅ RESTful API design
- ✅ FastAPI framework
- ✅ Service-to-service communication
- ✅ Database design per service
- ✅ API documentation
- ✅ Modern Python development practices

---

Built with ❤️ and 🎸 by Christyan Simbolon