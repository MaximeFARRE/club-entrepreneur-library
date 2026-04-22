# 📚 Club Entrepreneur Library Manager

> The official library management system built by and for the members of the Club Entrepreneur student association at Pôle Léonard de Vinci.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=flat&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Project Purpose
Built as a custom tool for the Club Entrepreneur (Campus Léonard de Vinci), this application replaces chaotic spreadsheets to manage the association's private book collection. It centralizes the catalog, tracks member loans, enforces return dates, and automatically sends email reminders to late borrowers.

## Main Features
- **Catalog Management**: View, search, and filter the book collection.
- **Inventory Operations**: Add new books, archive lost ones, and manage availability.
- **Borrowing & Returns**: Track active loans and automatically calculate due dates.
- **Full Ledger**: Maintain a complete history of all past borrowing activity.
- **Automated Notifications**: Send email reminders for overdue books.
- **Dual Database Support**: Runs locally on SQLite or in the cloud via Neon PostgreSQL.

## Technologies
- **Frontend & App Framework**: [Streamlit](https://streamlit.io/)
- **Data Persistence**: SQLite (local dev) / PostgreSQL (production via `psycopg2`)
- **Data Processing**: Pandas

---

## 📸 Screenshots
*(Placeholder: Add a screenshot of the Catalog page here)*
`![Catalog View](assets/demo-catalog.png)`

*(Placeholder: Add a screenshot of the Borrowing interface here)*
`![Borrowing View](assets/demo-borrow.png)`

---

## Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MaximeFARRE/Projet-bibli-club.git
   cd Projet-bibli-club
   ```
2. **Create a virtual environment & install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```bash
   streamlit run Accueil.py
   ```

## Repository Structure
```text
.
├── Accueil.py               # Main application entry point
├── assets/                  # Static assets (logos, icons)
├── data/                    # Local SQLite database (ignored)
├── database.py              # Data access layer & DB connection factory
├── email_utils.py           # SMTP email utilities
├── notifications.py         # Business logic for late returns
├── pages/                   # Streamlit UI views
└── requirements.txt         # Project dependencies
```

## Roadmap
- [ ] Add user authentication and roles (Admin vs Member).
- [ ] Implement barcode/ISBN scanning for faster book entry.
- [ ] Deploy to Streamlit Community Cloud.

## Limitations
- Designed for single-tenant book clubs. 
- The notification system requires a configured SMTP server via Streamlit secrets.

## Contributors
- Maxime FARRE
