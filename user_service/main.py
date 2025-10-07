# user_service/main.py
"""
USER MICROSERVICE
Handles user registration and authentication
Port: 8001
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import sqlite3
import hashlib
import json

app = FastAPI(
    title="User Service",
    description="Microservice for user management",
    version="1.0.0"
)

# Database setup
def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Pydantic models (for request/response validation)
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: str

class UserLogin(BaseModel):
    username: str
    password: str

# Helper functions
def hash_password(password: str) -> str:
    """Simple password hashing (use bcrypt in production!)"""
    return hashlib.sha256(password.encode()).hexdigest()

def get_db():
    """Get database connection"""
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# API Endpoints

@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "service": "User Service",
        "status": "running",
        "version": "1.0.0"
    }

@app.post("/users/register", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate):
    """
    Register a new user
    
    Example:
    POST /users/register
    {
        "username": "rockstar",
        "email": "rock@music.com",
        "password": "secret123"
    }
    """
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", 
                      (user.username, user.email))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username or email already exists")
        
        # Create user
        password_hash = hash_password(user.password)
        created_at = datetime.utcnow().isoformat()
        
        cursor.execute(
            "INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (user.username, user.email, password_hash, created_at)
        )
        conn.commit()
        
        # Get created user
        user_id = cursor.lastrowid
        cursor.execute("SELECT id, username, email, created_at FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        
        return {
            "id": row['id'],
            "username": row['username'],
            "email": row['email'],
            "created_at": row['created_at']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.post("/users/login")
def login_user(credentials: UserLogin):
    """
    Login a user
    
    Example:
    POST /users/login
    {
        "username": "rockstar",
        "password": "secret123"
    }
    """
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(credentials.password)
        
        cursor.execute(
            "SELECT id, username, email FROM users WHERE username = ? AND password_hash = ?",
            (credentials.username, password_hash)
        )
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        return {
            "message": "Login successful",
            "user": {
                "id": row['id'],
                "username": row['username'],
                "email": row['email']
            }
        }
        
    finally:
        conn.close()

@app.get("/users", response_model=List[UserResponse])
def get_all_users():
    """
    Get all users (admin endpoint)
    
    Example:
    GET /users
    """
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, username, email, created_at FROM users")
        rows = cursor.fetchall()
        
        return [
            {
                "id": row['id'],
                "username": row['username'],
                "email": row['email'],
                "created_at": row['created_at']
            }
            for row in rows
        ]
        
    finally:
        conn.close()

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """
    Get a specific user by ID
    
    Example:
    GET /users/1
    """
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, username, email, created_at FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "id": row['id'],
            "username": row['username'],
            "email": row['email'],
            "created_at": row['created_at']
        }
        
    finally:
        conn.close()

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    """
    Delete a user
    
    Example:
    DELETE /users/1
    """
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="User not found")
        
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        
        return {"message": f"User {user_id} deleted successfully"}
        
    finally:
        conn.close()


# Run with: uvicorn main:app --reload --port 8001
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)