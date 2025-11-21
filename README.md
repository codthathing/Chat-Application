# 💬 Real-Time Chat Application (Python + FastAPI)
- Why: Perfect for practicing OOP with Flask or FastAPI and WebSocket integration.

## Overview
A FastAPI-based backend that enables users to send and receive real-time chat messages using WebSockets.

## Tech Stack
- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite or PostgreSQL
- WebSockets
- JWT Authentication

## Features
- User Authentication (Register/Login)
- Real-Time Messaging (WebSocket)
- One-to-One & Group Chat Support
- Message History Storage

## API Routes
| Method | Endpoint | Description |
|--------|-----------|-------------|
| POST | /auth/register | Register a user |
| POST | /auth/login | Login & receive JWT |
| GET | /users | Get all users |
| WS | /ws/chat/{room_id} | Join chat room socket |

## 🧠 Suggested Learning Path
- Python Fundamentals (if not already solid)
- FastAPI Basics: routes, request/response models, dependency injection
- SQLAlchemy: models, queries, relationships
- Database: start with SQLite (easy setup), then explore PostgreSQL
- JWT Auth: login, token generation, protected routes
- WebSockets: only if your app needs real-time features

