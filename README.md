# 🧩 Enterprise-Scale Slot Lottery Prize Drawing System – Backend

This is the backend service for the **Enterprise-Scale Slot Lottery Prize Drawing System**, designed for managing prize drawings at internal corporate events. Built with **FastAPI** and **SQLite**, the backend provides business logic for prize phase execution, redraw handling, winner uniqueness enforcement, and eligibility filtering based on employee seniority. All drawing results are stored in the database with audit logs.

---

## 📌 Key Features

- 🎯 Multi-phase drawing logic with configurable prize groups
- 🔄 Redraw support: replace opted-out winners in real time
- 🧑‍💼 Seniority-based filtering for eligible participants
- ✅ Winner uniqueness enforcement across phases
- 📄 Final winner list generation per phase
- 🧾 SQLite database with audit-ready logging
- 🧪 RESTful API endpoints with auto-generated Swagger docs

---

## 🛠 Tech Stack

- **Framework:** FastAPI (Python)
- **Database:** SQLite (can be swapped with PostgreSQL)
- **Validation:** Pydantic
- **API Docs:** Swagger UI (`/docs`)
- **Dev Tools:** Uvicorn, Postman, GitHub

---

## 🚀 Getting Started

```bash
git clone https://github.com/green760223/react-slot-machine-backend.git
cd react-slot-machine-backend
pip install -r requirements.txt
uvicorn main:app --reload
```
API documentation at: http://localhost:8000/docs#

![API documentation preview](https://live.staticflickr.com/65535/54516176433_c715918f33_b.jpg)


## 🧠 Author
Developed by Yi-Hsuan (Lawrence) Chuang

## 📄 License

This backend is intended for internal event management and is not publicly distributed. Contact the author for inquiries or usage extension.
