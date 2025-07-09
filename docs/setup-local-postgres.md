# Running the App Locally with PostgreSQL Integration

This guide explains how to run the app locally using PostgreSQL. You can either connect to a **cloud-hosted pre-populated database (preferred)** or set up your own **local/custom PostgreSQL instance**.

---

## 1. Clone the Repository & Set Up the Environment

Clone the repo and navigate to the project directory.

**(Recommended)** Create and activate a Python virtual environment:

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
````

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 2. Configure the Database Connection

### Option 1 (Preferred): Use a Pre-Populated Cloud PostgreSQL on Neon.tech

If you have access to a shared Neon.tech database that is already seeded with login data, update your `.env` file with the following:

```env
DATABASE_URL=postgresql://<username>:<password>@<project-name>.neon.tech/<database_name>?sslmode=require
```

**Example:**

```env
DATABASE_URL=postgresql://readonly_user:securepass@ep-skywave-abc123.us-east-2.aws.neon.tech/myappdb?sslmode=require
```

> ✅ No setup or seeding needed. Skip to **Step 5** to run the app.

---

### Option 2: Set Up Your Own PostgreSQL Instance

#### A. Update your `.env` file:

```env
DATABASE_URL=postgresql://<username>:<password>@localhost:5432/<database_name>
```

**Example:**

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/myappdb
```

#### B. Create the database if it does not exist:

```bash
createdb myappdb
```

---

## 3. Initialize the Database

Apply database migrations to create all required tables:

```bash
flask db upgrade
```

> If `flask` is not recognized, try:

```bash
python -m flask db upgrade
```

---

## 4. Seed the Database with Login Data

Run the seed script to insert default users and required data:

```bash
python scripts/seed_db.py
```

> ⚠️ If `scripts/seed_db.py` is missing, notify the team. You may need to manually add users via the Flask shell or write a seed script.

---

## 5. Run the App

Start the Flask application:

```bash
flask run
```

or

```bash
python app.py
```

Then visit [http://localhost:5000](http://localhost:5000) in your browser.

---

## 6. Login

Use the test credentials provided in the documentation or seeded via `scripts/seed_db.py` or the Neon.tech shared database.

---