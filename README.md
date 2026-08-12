# Pronto in Tavola - Osteria d'Asporto

A full-stack web application for a traditional Italian trattoria offering takeaway service. The system manages the complete food delivery workflow: from customer authentication and menu browsing to order placement, kitchen status tracking, and automatic rider assignment based on proximity and workload.

## What the App Does

"Pronto in Tavola" is a complete food delivery management system for a traditional osteria. Customers can browse the menu, place orders, and track delivery status. The kitchen staff manages order preparation, and the system automatically assigns the most suitable rider for each delivery using a custom scoring algorithm.

### Main Features

- **Customer Authentication**: Secure registration and login system with JWT tokens and bcrypt password hashing. Role-based access control (customer, staff, admin).
- **Digital Menu**: Browse the complete trattoria menu with dishes, descriptions, and prices. Filter to show only available items.
- **Order Management**: Create orders with multiple products, automatic total calculation, and delivery address specification.
- **Order Status Tracking**: Full state machine for orders — received → in preparation → ready → in delivery → delivered. Each state transition is tracked and logged.
- **Automatic Rider Assignment**: When an order becomes "ready", the system automatically assigns the best available rider using a scoring algorithm that considers distance from delivery zone and current workload.
- **Rider Management**: Track rider status (available/occupied), delivery history, and active order count. Manual override available for staff.
- **Customer Database**: Manage customer profiles with contact information and order history.
- **Responsive UI**: Clean, modern interface built with React 19, TypeScript, and Tailwind CSS v4.

### User Flow

1. **Customer** registers/logs in with email and password.
2. Browses the digital menu and selects dishes to order.
3. Confirms the order with delivery address and sees the total price.
4. **Kitchen staff** receives the order (status: "received") and starts preparation.
5. When the order is ready (status: "ready"), the system **automatically assigns the best rider** based on proximity and workload.
6. **Rider** picks up the order (status: "in delivery") and delivers it to the customer.
7. Upon delivery confirmation, the rider becomes available again for new assignments.

## Tech Stack

### Frontend
- **React 19** — UI library with hooks and functional components
- **TypeScript** — Type-safe JavaScript for robust code
- **Vite** — Fast development build tool
- **Tailwind CSS v4** — Utility-first CSS framework
- **React Router DOM v7** — Client-side routing

### Backend
- **Flask** — Python web framework
- **Flask-SQLAlchemy** — ORM for database operations
- **Flask-JWT-Extended** — JWT authentication and authorization
- **Flask-CORS** — Cross-origin resource sharing handling
- **bcrypt** — Secure password hashing
- **SQLite** — Lightweight relational database

## Project Structure

```
pronto-in-tavola/
├── backend/
│   ├── app.py                    # Flask application entry point
│   ├── database.py               # SQLAlchemy models and database setup
│   ├── assegnazione_rider.py   # Rider assignment algorithm
│   ├── routes_auth.py            # Authentication endpoints (JWT)
│   ├── routes_clienti.py         # Customer CRUD endpoints
│   ├── routes_prodotti.py        # Menu/product endpoints
│   ├── routes_ordini.py          # Order management endpoints
│   ├── routes_rider.py           # Rider management endpoints
│   └── requirements.txt          # Python dependencies
├── frontend/
│   ├── src/                      # React components and logic
│   ├── index.html                # Main HTML entry
│   ├── package.json              # Node dependencies
│   ├── vite.config.ts            # Vite configuration with proxy
│   └── tailwind.config.*         # Tailwind CSS configuration
└── README.md
```

## Getting Started

### Prerequisites
- [Python 3.11+](https://www.python.org/)
- [Node.js](https://nodejs.org/) (LTS version)
- [Git](https://git-scm.com/)

### Backend Setup

1. Navigate to the backend folder:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the Flask server:
   ```bash
   python app.py
   ```
   The backend will be available at `http://127.0.0.1:5000`

### Frontend Setup

1. In a new terminal, navigate to the frontend folder:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173`

> The Vite dev server is configured with a proxy that forwards API requests to the Flask backend automatically.

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/registrati` | Register new account |
| POST | `/auth/login` | Login and receive JWT token |
| GET | `/auth/profilo` | Get current user profile (requires token) |

### Products (Menu)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/prodotti/` | List all menu items |
| GET | `/prodotti/disponibili` | List only available items |
| GET | `/prodotti/<id>` | Get single product details |
| POST | `/prodotti/` | Add new product (admin) |
| PUT | `/prodotti/<id>` | Update product |
| PATCH | `/prodotti/<id>/disponibilita` | Toggle product availability |
| DELETE | `/prodotti/<id>` | Remove product |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ordini/` | List all orders (filterable by status) |
| GET | `/ordini/<id>` | Get order details with products |
| GET | `/ordini/cliente/<id>` | Get orders by customer |
| POST | `/ordini/` | Create new order |
| PATCH | `/ordini/<id>/stato` | Update order status (triggers auto rider assignment when "pronto") |
| PATCH | `/ordini/<id>/assegna-rider` | Manual rider assignment |
| DELETE | `/ordini/<id>` | Delete order (only if "ricevuto") |

### Riders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/rider/` | List all riders |
| GET | `/rider/disponibili` | List available riders |
| GET | `/rider/<id>` | Get rider details |
| POST | `/rider/` | Register new rider |
| PUT | `/rider/<id>` | Update rider info |
| PATCH | `/rider/<id>/stato` | Update rider status |
| PATCH | `/rider/<id>/consegnato` | Mark delivery as completed |
| DELETE | `/rider/<id>` | Remove rider |

### Customers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/clienti/` | List all customers |
| GET | `/clienti/<id>` | Get customer details |
| POST | `/clienti/` | Create customer |
| PUT | `/clienti/<id>` | Update customer |
| DELETE | `/clienti/<id>` | Delete customer |

## Skills Demonstrated

- **Frontend Development**: React 19 with TypeScript, component architecture, state management, responsive design with Tailwind CSS v4
- **Backend Development**: Flask REST API design, SQLAlchemy ORM, database modeling with relationships
- **Authentication & Security**: JWT token-based auth, bcrypt password hashing, role-based access control, CORS protection
- **Database Design**: Relational schema with foreign keys, many-to-many relationships via junction tables, data integrity
- **Algorithm Implementation**: Custom rider assignment algorithm using distance matrix + workload scoring
- **API Integration**: Fetch API with async/await, frontend-backend communication, proxy configuration
- **State Machine Logic**: Order lifecycle management with validation and automatic triggers
- **Input Validation**: Server-side validation for all endpoints, error handling with appropriate HTTP status codes
- **Project Organization**: Modular Flask blueprints, separation of concerns, clean code documentation

## Contact

- LinkedIn: [Isaac Franck Tiensi Happi](https://www.linkedin.com/in/isaac-franck-tiensi-happi-2b647022a/)
- Email: cunegohappi@gmail.com
