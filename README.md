# Buy & Sell

Buy & Sell is a REST API for a classified-listings marketplace. It brings together user accounts, item listings, listing-based conversations, watchlists, transaction records, image storage, and optional AI-assisted description generation in a single FastAPI application.

This repository is a backend portfolio project. It demonstrates the core workflows and integration boundaries of a marketplace API; it is not presented as a complete payment or notification platform.

## What It Demonstrates

- REST API design with FastAPI, Pydantic request/response models, and generated OpenAPI documentation
- Relational marketplace modelling with SQLAlchemy and PostgreSQL
- OAuth2 password-flow login, bcrypt password hashing, and time-limited JWT bearer tokens
- Resource-level authorization for listing, message, image, transaction, and watchlist operations
- AWS S3-backed profile and listing image workflows
- A bounded OpenAI integration for generating a listing description when the seller omits one
- API workflow tests and a PostgreSQL-backed GitHub Actions test job

## Architecture

The application is a synchronous, layered monolith. FastAPI route modules validate HTTP input and enforce workflow rules, CRUD modules contain SQLAlchemy persistence operations, and Pydantic schemas define the API contracts. A shared SQLAlchemy session dependency connects both layers to PostgreSQL.

```mermaid
flowchart LR
    Client[API client] --> API[FastAPI routes]
    API --> Auth[JWT auth dependency]
    API --> Schemas[Pydantic schemas]
    API --> CRUD[CRUD modules]
    CRUD --> ORM[SQLAlchemy models]
    ORM --> DB[(PostgreSQL)]
    API --> S3[AWS S3\nimage storage]
    API --> AI[OpenAI Chat Completions\ndescription generation]
```

At application startup, SQLAlchemy creates missing tables and seeds the predefined parent/subcategory catalogue. The repository does not contain a migration system, so schema evolution is not versioned.

## Key Features

- Account registration, profile updates, account deletion, login, and current-user lookup
- Listing creation, browsing, category filtering, updates, deletion, availability status, quantity, pricing, and contact-preference fields
- Profile-picture and listing-picture upload, replacement, and deletion through separate S3 bucket configuration
- Buyer/seller conversations attached to a listing, including rules around who can initiate a conversation and which message can be edited or deleted
- Listing and user watchlists with duplicate-follow prevention in the application layer
- Buyer/seller transaction records with quantity and listing-price validation plus in-progress, successful, and declined states
- AI-assisted listing-description generation when a create request does not provide a description

## Technical Highlights

### Authentication and authorization

`POST /token` implements the OAuth2 password flow. Passwords are hashed with bcrypt through Passlib, and successful login returns an HS256 JWT with a 30-minute expiry. Protected operations resolve the current user from the bearer token and apply ownership or participant checks at the route boundary. Public user lookups return a reduced marketplace profile, while `/users/me` preserves the authenticated user's full account response.

### Relational marketplace model

Nine SQLAlchemy tables represent users, posts, category hierarchies, pictures, messages, transactions, and the two watchlist relationships. ORM relationships and delete-orphan cascades keep dependent marketplace records tied to their owning user or listing.

### Listing-based messaging

Messages are associated with a sender, receiver, and listing. A prospective buyer must contact the seller first; the seller can then reply in that listing context. The API limits message edits and deletions to the sender's latest message associated with the listing.

### Image lifecycle

Image endpoints use Boto3 to upload and delete S3 objects. Uploads are limited to one megabyte and require an image content type. When no custom upload exists or the last listing image is removed, the current implementation falls back to historical default-image URLs.

### Bounded AI assistance

When a listing is created without a description, the API sends the supplied keywords and listing fields to OpenAI's `gpt-3.5-turbo` chat-completions endpoint and stores the returned description. This is one optional listing workflow, not the application's decision-making core.

### Transaction workflow—not payment processing

The transaction API persists buyer, seller, listing, quantity, price, and status records. It verifies that the buyer is not the seller, requested stock is available, and the submitted total matches listing price multiplied by quantity. There is no payment-provider integration, checkout session, webhook handling, fund capture, or marketplace settlement in this repository.

## Tech Stack

| Area | Technology |
| --- | --- |
| API | Python 3.12, FastAPI |
| Validation | Pydantic 2 |
| Persistence | SQLAlchemy 2, PostgreSQL, psycopg2 |
| Authentication | PyJWT, Passlib, bcrypt, OAuth2 bearer tokens |
| Object storage | AWS S3 via Boto3 |
| AI integration | OpenAI Python SDK, Chat Completions API |
| Testing | pytest, FastAPI TestClient |
| CI | GitHub Actions, PostgreSQL 16 service |

## API Overview

The API is organized around these domains:

| Domain | Responsibilities |
| --- | --- |
| Authentication | Issue bearer tokens and return the active user |
| Users | Register, list, retrieve, update, and delete accounts |
| Listings | Create and manage listings; browse globally, by seller, or by subcategory |
| Pictures | Manage listing images; profile-image handling is part of user create/update |
| Messages | Start and manage listing-specific buyer/seller conversations |
| Transactions | Create, inspect, update, and delete internal transaction records |
| Watchlists | Follow/unfollow listings and users, and query follow relationships |

With the app running, interactive Swagger UI is served at [`http://127.0.0.1:8000/`](http://127.0.0.1:8000/). The generated OpenAPI document is available at [`http://127.0.0.1:8000/openapi.json`](http://127.0.0.1:8000/openapi.json).

## Project Structure

```text
.
├── .github/workflows/ci.yml  # Python 3.12/PostgreSQL CI test job
├── app/
│   ├── core/                 # JWT/password handling and API configuration
│   ├── crud/                 # SQLAlchemy query and persistence functions
│   ├── models/               # Relational database models
│   ├── routes/               # HTTP endpoints, authorization, and integrations
│   ├── schemas/              # Pydantic API contracts
│   ├── tests/                # API workflow tests
│   ├── database.py           # Engine, session factory, and request dependency
│   └── main.py               # App assembly, table creation, and category seeding
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.12
- PostgreSQL
- OpenAI API credentials only when using AI-assisted description generation
- AWS credentials and two S3 buckets when exercising image upload/delete flows

### Installation

1. Clone the repository and enter it:

   ```bash
   git clone https://github.com/nebielm/buy_-_sell.git
   cd buy_-_sell
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   On Windows PowerShell, activate it with `.venv\Scripts\Activate.ps1`.

3. Install the pinned-compatible dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Create a PostgreSQL database, then create a local `.env` file in the repository root:

   ```dotenv
   SQLALCHEMY_DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/buy_sell
   SECRET_KEY=replace-with-a-long-random-secret
   # Optional: required only for AI-assisted description generation
   OPENAI_API_KEY=replace-with-your-openai-api-key

   # Optional: required only for profile/listing image upload and deletion
   AWS_ACCESS_KEY_ID=replace-with-your-aws-access-key-id
   AWS_SECRET_KEY=replace-with-your-aws-secret-access-key
   BUCKET_NAME_PROFILE_PIC=replace-with-your-profile-image-bucket
   BUCKET_NAME_POST_PIC=replace-with-your-listing-image-bucket
   ```

   `.env` is ignored by Git. Do not commit real credentials.

5. Start the API:

   ```bash
   python -m uvicorn app.main:app --reload
   ```

On startup, the application creates any missing tables and seeds its category catalogue. There is no Alembic directory or migration command in this repository.

## Environment Variables

| Variable | Requirement | Purpose |
| --- | --- | --- |
| `SQLALCHEMY_DATABASE_URL` | Required | SQLAlchemy connection URL; PostgreSQL is the configured project/CI database |
| `SECRET_KEY` | Required for authentication | Signs and validates HS256 access tokens |
| `OPENAI_API_KEY` | AI integration | Lazily initializes the OpenAI client when description generation is requested |
| `AWS_ACCESS_KEY_ID` | S3 integration | AWS credential used by image upload/delete operations |
| `AWS_SECRET_KEY` | S3 integration | AWS secret used by image upload/delete operations |
| `BUCKET_NAME_PROFILE_PIC` | Profile-image integration | Target bucket for profile images |
| `BUCKET_NAME_POST_PIC` | Listing-image integration | Target bucket for listing images |

The S3 client region is fixed to `eu-north-1` in the current implementation. The repository does not include an `.env.example`; the block above mirrors every environment variable read by the application.

## Testing

Run the API test suite with:

```bash
python -m pytest -q
```

The tests cover account/authentication flows, public-user privacy, listing reads and updates, conversation rules, transaction validation, listing/user watchlists, and the external-service boundaries. Local pytest runs force a temporary SQLite database even if the application `.env` points elsewhere. In GitHub Actions, tests accept only the existing PostgreSQL service on the local CI runner and reject non-local database hosts.

No live S3 or OpenAI calls are made by the test suite. CI runs the tests on Python 3.12 against its existing PostgreSQL 16 service using repository secrets.

## Project Status and Limitations

This project is maintained primarily as a portfolio demonstration of backend API design, relational modelling, authorization rules, and external-service integration.

- Database tables are created automatically at startup; there are no versioned migrations.
- Transactions are domain records only. No external payment processor or money movement is implemented.
- Watchlists record follow relationships but do not dispatch notifications.
- The API has no frontend, Docker configuration, or current deployment configuration in the repository.
- Live S3 and OpenAI calls require real service credentials; tests cover their local boundaries without contacting either service.
- The two historical default-image S3 URLs currently return `404`. Bundled copies exist under `app/default_pictures/`, but the API does not currently serve them.

## Author

Nebiel Mohammed

- [Portfolio](https://nebielm.github.io/nebielmohammed/)
- [GitHub](https://github.com/nebielm)
- [LinkedIn](https://www.linkedin.com/in/nebiel-mohammed-a43218302/)
