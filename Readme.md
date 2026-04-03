# Finance Dashboard Backend API

Flask backend for a role-based finance dashboard. It includes authentication, users, financial records, categories, audit logs, and dashboard summaries.

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create an `.env` file in the `app` folder:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
DATABASE_URL=sqlite:///finance.db
```

## Database

```bash
flask db init
flask db migrate -m "initial models"
flask db upgrade
```

## Run

```bash
flask run
```

The app runs at `http://127.0.0.1:5000`.

## API Routes

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/users/`
- `GET /api/records/`
- `POST /api/records/`
- `GET /api/dashboard/summary`