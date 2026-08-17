# 🛒 E-Commerce API

A modular, production-oriented **E-Commerce REST API** built with
**FastAPI, SQLAlchemy 2.x, PostgreSQL, and JWT authentication**.

The project is designed as a learning and portfolio backend focused on
clean architecture, separation of concerns, authentication,
authorization, repository/service patterns, and transactional order
processing.

> **Status:** 🚧 Active development

## ✨ Highlights

-   🔐 JWT-based authentication
-   👥 Customer, Seller, and Admin roles
-   🏪 Seller-owned product management
-   🛍️ Shopping cart management
-   📦 Order creation and management
-   🔒 Role-based and ownership-based authorization
-   💳 Transactional order creation
-   📉 Product stock validation and decrement
-   🧩 Service + Repository architecture
-   🗄️ PostgreSQL persistence with SQLAlchemy 2.x
-   💉 FastAPI dependency injection
-   🔑 Argon2 password hashing through `pwdlib`
-   🧱 Modular domain-based project structure
-   📚 OpenAPI/Swagger documentation through FastAPI

## 🏗️ Architecture

The backend is organized into two major business domains:

-   **Identity** --- authentication and user management
-   **Commerce** --- products, carts, and orders

The application core provides shared infrastructure such as database
integration, dependency injection, security, configuration, and
exception handling.

### Architecture & Process Flows

![E-Commerce API Architecture and Process Flows](docs/architecture.png)

### Request Flow

``` text
Client
  │
  ▼
FastAPI Router
  │
  ▼
Domain Service
  │
  ▼
Repository
  │
  ▼
SQLAlchemy Model
  │
  ▼
PostgreSQL
```

The project intentionally keeps HTTP concerns, business logic,
persistence logic, and database models separated.

------------------------------------------------------------------------

## 🧩 Project Structure

``` text
app/
├── core/
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── exceptions.py
│   └── security.py
│
├── modules/
│   ├── auth/
│   │   ├── routes.py
│   │   ├── services.py
│   │   ├── repository.py
│   │   ├── hashing.py
│   │   ├── jwt_token.py
│   │   └── schemas.py
│   │
│   ├── user/
│   │   ├── routes.py
│   │   ├── services.py
│   │   ├── repository.py
│   │   ├── models.py
│   │   └── schemas.py
│   │
│   ├── products/
│   │   ├── routes.py
│   │   ├── services.py
│   │   ├── repository.py
│   │   ├── models.py
│   │   └── schemas.py
│   │
│   ├── cart/
│   │   ├── routes.py
│   │   ├── services.py
│   │   ├── repository.py
│   │   ├── models.py
│   │   └── schemas.py
│   │
│   └── orders/
│       ├── routes.py
│       ├── services.py
│       ├── repository.py
│       ├── models.py
│       └── schemas.py
│
└── main.py
```

> File names may evolve as the project develops; the important
> architectural boundary is **Route → Service → Repository → Persistence
> Model**.

------------------------------------------------------------------------

## 🔐 Authentication & Authorization

Authentication is implemented using **JWT bearer tokens**.

``` text
Request
   │
   ▼
Bearer Token
   │
   ▼
JWT Authentication
   │
   ▼
get_current_user()
   │
   ▼
Role / Ownership Check
   │
   ▼
Domain Service
```

Passwords are never stored directly. They are hashed before persistence
and verified during login.

### Roles

  -----------------------------------------------------------------------
  Role                                Responsibility
  ----------------------------------- -----------------------------------
  Customer                            Browse products, manage own cart,
                                      create orders, view own orders

  Seller                              Manage owned products and access
                                      order items related to owned
                                      products

  Admin                               Administrative access across the
                                      platform
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 🏪 Seller Ownership & Order Authorization

One of the important business rules in this project is **resource-level
authorization**.

A seller must **not** be able to view every customer's complete order.

Instead, seller access is derived from the authenticated user's
identity:

``` text
Seller
  │
  ▼
JWT Authentication
  │
  ▼
Current Seller ID
  │
  ▼
Products owned by Seller
  │
  ▼
Order Items referencing those Products
  │
  ▼
Seller-visible order data
```

This means the backend does not trust a client-provided `seller_id` to
determine ownership.

### Example

``` text
Seller A
 ├── Product A1
 ├── Product A2
 │
 └── Can access:
      ├── Order Item → Product A1
      └── Order Item → Product A2

Seller B's products/order items
 └── Not accessible to Seller A
```

This separates **authentication** ("Who are you?") from
**authorization** ("What resources are you allowed to access?").

------------------------------------------------------------------------

## 🛒 Core Business Flows

### 1. User Registration

``` text
Client
  ↓
Auth API
  ↓
Auth Service
  ↓
Check existing email
  ↓
Hash password
  ↓
Create User
  ↓
User Repository
  ↓
PostgreSQL
```

### 2. User Login

``` text
Client
  ↓
Auth API
  ↓
Auth Service
  ↓
Load user credentials
  ↓
Verify password
  ↓
JWT Token Service
  ↓
Access Token
```

### 3. Seller Creates Product

``` text
Seller
  ↓
Product API
  ↓
JWT Authentication
  ↓
Seller Role Check
  ↓
Product Service
  ↓
Product Repository
  ↓
Create Product with authenticated seller_id
  ↓
PostgreSQL
```

### 4. Customer Adds Product to Cart

``` text
Customer
  ↓
Cart API
  ↓
JWT Authentication
  ↓
Cart Service
  ↓
Validate Product
  ↓
Validate Availability / Stock
  ↓
Cart Repository
  ↓
Create or Update Cart Item
  ↓
PostgreSQL
```

### 5. Create Order

Order creation is treated as a database transaction.

``` text
Customer
  ↓
Order API
  ↓
JWT Authentication
  ↓
Order Service
  ↓
Load Cart + Cart Items
  ↓
Load Products
  ↓
Validate Availability + Stock
  ↓
Calculate Prices + Total
  ↓
Create Order
  ↓
Create Order Items
  ↓
Decrease Product Stock
  ↓
Clear Cart
  ↓
COMMIT
  │
  └──► Rollback if a transactional step fails
```

The goal is to prevent partially-created orders and inconsistent
inventory state.

### 6. Customer Views Orders

``` text
Customer
  ↓
GET Orders
  ↓
JWT Authentication
  ↓
Current Customer ID
  ↓
Order Service
  ↓
Filter by customer_id
  ↓
Return customer's orders
```

### 7. Seller Views Relevant Orders

``` text
Seller
  ↓
GET Seller Orders
  ↓
JWT Authentication
  ↓
Current Seller ID
  ↓
Find seller-owned products
  ↓
Find order items for those products
  ↓
Return only authorized order data
```

------------------------------------------------------------------------

## 🗃️ Domain Model

``` text
User
 │
 ├── owns ──► Product
 │
 ├── has ───► Cart
 │              │
 │              └── contains ──► Cart Item
 │                                  │
 │                                  └── references Product
 │
 └── creates ─► Order
                  │
                  └── contains ──► Order Item
                                      │
                                      └── references Product
```

### Main entities

-   **User** --- identity, role, and account information
-   **Product** --- seller-owned product with price and stock
-   **Cart** --- customer's active shopping cart
-   **Cart Item** --- product and quantity inside a cart
-   **Order** --- customer's order and overall status
-   **Order Item** --- product snapshot, quantity, and purchase price

------------------------------------------------------------------------

## 🛠️ Technology Stack

  Technology          Purpose
  ------------------- -----------------------------
  Python              Backend language
  FastAPI             REST API framework
  SQLAlchemy 2.x      ORM / persistence layer
  PostgreSQL          Relational database
  Pydantic            Request/response validation
  Pydantic Settings   Configuration management
  PyJWT               JWT token handling
  pwdlib + Argon2     Password hashing
  Alembic             Database migrations
  Uvicorn             ASGI server
  python-dotenv       Environment configuration

------------------------------------------------------------------------

## 🚀 Getting Started

### Prerequisites

Make sure you have:

-   Python 3.11+
-   PostgreSQL
-   Git

### 1. Clone the repository

``` bash
git clone https://github.com/aditya-kamarsu/E-Commerce-Api.git
cd E-Commerce-Api
```

### 2. Create a virtual environment

**Windows**

``` bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

Example:

``` env
DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/ecommerce
JWT_SECRET_KEY=change-this-secret
JWT_ALGORITHM=HS256
```

Use your own PostgreSQL credentials and a strong secret key.

### 5. Run database migrations

``` bash
alembic upgrade head
```

If migrations are not yet configured for your current development state,
create/apply the required migration before starting the application.

### 6. Start the API

``` bash
uvicorn app.main:app --reload
```

The API should then be available at:

``` text
http://127.0.0.1:8000
```

------------------------------------------------------------------------

## 📚 API Documentation

FastAPI automatically provides interactive API documentation.

After starting the server:

-   Swagger UI: `/docs`
-   ReDoc: `/redoc`
-   OpenAPI schema: `/openapi.json`

Use Swagger UI to register/login users, obtain a JWT, authorize
requests, and test the API.

------------------------------------------------------------------------

## 🧪 Testing

Testing is part of the planned development workflow.

Important test categories include:

-   Authentication tests
-   Password verification tests
-   JWT validation tests
-   Role authorization tests
-   Product ownership tests
-   Cart ownership tests
-   Customer order isolation tests
-   Seller order-item isolation tests
-   Stock validation tests
-   Transaction rollback tests

A particularly important security test is:

``` text
Seller A
  ↓
Attempts to access Seller B's product/order data
  ↓
Authorization check
  ↓
403 Forbidden / filtered result
```

------------------------------------------------------------------------

## 🔒 Security Principles

This project follows several backend security principles:

1.  Passwords are hashed before storage.
2.  Authentication is based on signed JWTs.
3.  Protected endpoints require an authenticated user.
4.  Roles are checked server-side.
5.  Resource ownership is checked server-side.
6.  Client-provided ownership identifiers are not trusted.
7.  Database transactions protect multi-step order creation.
8.  Environment variables are used for secrets and database
    configuration.

------------------------------------------------------------------------

## 🎯 Design Goals

The project is being built to practice real backend engineering concepts
rather than only CRUD operations.

### Current focus

-   Modular architecture
-   Authentication
-   Authorization
-   Product ownership
-   Cart management
-   Order processing
-   Transactional database operations
-   Repository/service separation

### Planned improvements

-   [ ] Refresh token flow
-   [ ] Pagination and filtering
-   [ ] More comprehensive automated tests
-   [ ] Docker / Docker Compose
-   [ ] CI/CD pipeline
-   [ ] Rate limiting
-   [ ] Structured application logging
-   [ ] Caching
-   [ ] Payment integration
-   [ ] Order status workflow
-   [ ] Production deployment

------------------------------------------------------------------------

## 🧠 What This Project Demonstrates

This project is intended to demonstrate practical understanding of:

-   REST API development
-   FastAPI dependency injection
-   Authentication vs authorization
-   JWT-based security
-   RBAC
-   Resource ownership
-   SQLAlchemy 2.x
-   Repository pattern
-   Service layer architecture
-   Relational data modeling
-   Database transactions
-   Inventory consistency
-   Modular backend design
-   API validation with Pydantic

------------------------------------------------------------------------

## 📈 Architecture Philosophy

The main architectural rule is:

``` text
HTTP / API Layer
       ↓
Business / Service Layer
       ↓
Persistence / Repository Layer
       ↓
Database
```

Routes should handle HTTP concerns.

Services should contain business rules.

Repositories should handle persistence and queries.

Models should represent persistence entities.

Shared infrastructure belongs in the application core.

This separation makes the codebase easier to test, maintain, and extend
as new commerce domains are introduced.

------------------------------------------------------------------------

## 🤝 Future Contributions

This repository is primarily a personal backend engineering project, but
suggestions and constructive feedback are welcome.

If you find an issue or have an architectural improvement, feel free to
open an issue or pull request.

------------------------------------------------------------------------

## 👨‍💻 Author

**Aditya Kamarsu**

Python Backend Developer focused on building APIs, backend systems, and
scalable software architecture.

-   GitHub: [@aditya-kamarsu](https://github.com/aditya-kamarsu)

------------------------------------------------------------------------

## ⭐ Project

If you find the architecture or implementation useful for learning
backend development, consider giving the repository a star.

**Repository:** https://github.com/aditya-kamarsu/E-Commerce-Api
