# Bicycle Shop

A web application for a bicycle shop owner, Marcus, to sell his bicycles online with customization options. The application is designed to support future expansion to other sports-related items such as skis, surfboards, roller skates, etc.

## About this project

The requirements of the project can be found [here](./scope.md).

## Features

### Public Part

- **Home Page**: Displays a list of bicycles available for sale.
- **Bicycle Detail Page**: Allows customers to customize their bicycles with various parts and options, and add the configured bicycle to their cart. It prevents adding bicycles with forbidden combinations or out-of-stock parts.
- **My Cart Page**: Displays the bicycles added to the cart with their configurations.

### Private Part (Admin Dashboard)

- **Manage Bicycles**: Allows the admin to create and delete bicycles.
- **Configure Bicycle Parts**: Allows the admin to manage the parts offered for each bicycle, including marking parts as temporarily out of stock.
- **Configure Configuration Rules**: Allows the admin to manage the parts offered for each bicycle, including marking parts as temporarily out of stock.

## Tech Stack

- **Frontend**: Built with React 18, Vite and Tailwind CSS
- **Backend**: Built with Python 3.9, FastAPI, FastAPI Users
- **Database**: MongoDB
- **Containerization**: Docker

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/bicycle-shop.git
   cd bicycle-shop
   ```

2. Start the application using Docker Compose:

   ```bash
   docker-compose up --build -d
   ```

3. Populate the database

   ```bash
    docker exec -it my-mongo-container mongosh -u admin -p password docker-entrypoint-initdb.d/init-mongo.js
   ```

4. The frontend application will be accessible at `http://0.0.0.0:5173` and backend application at `http://0.0.0.0:8001/docs`.

## API Endpoints

For detailed information on each endpoint, including request and response examples, please go to the [API documentation](http://0.0.0.0:8001/docs).

## Project Structure

## Tradeoffs and Decisions

During the development of this project, several tradeoffs and decisions were made to balance various factors such as performance, maintainability, scalability and speed of development. Below are the key tradeoffs and decisions:

### 1. Technology Stack

**Decision:** Opted for a React and FastAPI stack.
**Tradeoff:** While using React for the frontend allows for a highly interactive user interface and FastAPI for the backend offers fast performance and easy API creation, there may be a learning curve for developers unfamiliar with these technologies. Additionally, integrating the two can require additional setup and configuration compared to more traditional stacks.

### 2. Database Choice

**Decision:** Chose MongoDB as the primary database.
**Tradeoff:** MongoDB offers flexibility with its schema-less design, which is great for rapid development and basic CRUD queries. However, it may result in higher complexity for relational data queries compared to SQL databases.

### 3. State Management

**Decision:** Utilized `useContext` and `useReducer` for state management in the React application.
**Tradeoff:** `useContext` and `useReducer` provide a simpler and more localized state management solution compared to Redux but do not offer the same level of tooling and middleware support.

### 4. Styling Framework

**Decision:** Used Tailwind CSS for styling.
**Tradeoff:** Tailwind CSS allows for rapid UI development with utility-first classes, but it can lead to verbose HTML and potentially larger bundle sizes if not purged correctly.

### 5. Authentication

**Decision:** Implemented JWT (JSON Web Tokens) for authentication and use FAST API users for sign in / login.
**Tradeoff:** JWT offers stateless authentication, which is scalable and easy to implement. However, it requires careful handling of token expiration and security considerations. The use of FAST API users

### 6. Domain-Driven Design (DDD)

**Decision:** Implemented Domain-Driven Design to separate domain logic from infrastructure concerns.
**Tradeoff:** DDD provides a structured approach to managing complex and scalable applications but can introduce additional complexity, verbosity and require more upfront design.

### 7. Speed of Development

**Decision:** Prioritized rapid development and delivery.
**Tradeoff:** To achieve quick development cycles, some architectural and code quality compromises were made. This includes using pre-built components and libraries where applicable, which may not be fully optimized for specific use cases but allow for faster implementation.

These tradeoffs and decisions were made to balance the project's requirements and constraints. During our call, I will provide further explanations and insights into these choices
