#  TeamStats - Basketball Performance Tracker

A web-based basketball team management app that helps coaches and team managers **track player stats**, **analyze game performance**, and **manage teams** with ease.

---

## Features

- Player Management (Add/Edit/Delete)
- Track stats: points, assists, rebounds, steals, blocks, etc.
- Game Scheduling & Stat Entry
- Dashboard with summary analytics
- User authentication (login/register/logout)
- Password reset & forgot password flows

---

## Screenshots

> *(You can add screenshots or GIFs here to showcase the dashboard, player pages, etc.)*

---

##  Tech Stack

- **Flask** (backend)
- **SQLite** (database)
- **Flask-Login** (authentication)
- **Bootstrap 5** (frontend)
- **SQLAlchemy** (ORM)

---

##  Project Structure

```
basketball_app/
│
├── app/
│   ├── templates/         # HTML templates
│   ├── static/            # CSS, JS, images
│   ├── routes/            # All Blueprint routes
│   ├── models.py          # Database models
│   ├── extensions.py      # Initialized extensions (db, login)
│   └── __init__.py        # App factory
│
├── run.py                 # Entry point
├── requirements.txt
├── .env                   # Environment variables
└── README.md
```

---

##  Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/basketball_app.git
cd basketball_app

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo SECRET_KEY="your-secret-key" > .env

# Run the app
python run.py
```

---

##  Usage

1. Register as a new user
2. Add players and games
3. Enter stats for each game
4. View summary analytics on the dashboard

---

##  Future Plans

- Multi-team support
- Player performance trends
- PDF/stat reports
- Admin dashboard

---

 🙋‍♂️ Contributing

Pull requests are welcome! For major changes, open an issue first to discuss what you would like to change.

---

##  License

MIT License