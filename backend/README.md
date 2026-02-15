# HuaxiaTCM Backend

## Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

## Setup

1. Create and activate a virtual environment
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create `var.env` in the backend folder:

```env
COZE_CLIENT_ID=your_coze_client_id
COZE_CLIENT_SECRET=your_coze_client_secret
COZE_REDIRECT_URI=your_redirect_uri

OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://api.deepseek.com

JWT_SECRET_KEY=your_jwt_secret_key

DATABASE_URI=sqlite:///database.db
```

Update any required keys in [config.py](config.py).

## Run

Development:

```bash
python app.py
```

Production:

```bash
gunicorn -c gunicorn.conf.py app:app
```