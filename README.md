# playwright_sdet_framework
# 🚀 Playwright SDET Hybrid Framework (Python)

## 📌 Overview

This is a **production-ready hybrid automation framework** built using:

* Playwright (UI Testing)
* Pytest (Test Runner)
* Requests (API Testing)
* MySQL (DB Validation)
* Allure (Reporting)
* Environment-based configuration

It supports **UI, API, E2E, and DB validation** in a scalable and maintainable architecture.

---

## 🧱 Framework Architecture

```
Tests → Services → API Client / Page Objects → Application
```

### Layers:

* **UI Layer** → Page Object Model (pages/)
* **API Layer** → API Client (api/)
* **Service Layer** → Business logic (services/)
* **Core Layer** → Config, Env, DB, Hooks (core/)
* **Test Layer** → UI + API + E2E tests

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```
git clone <your-repo-url>
cd playwright-sdet-framework
```

---

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
playwright install
```

---

### 3️⃣ Setup Environment

Update `.env.prod`:

```
BASE_URL=http://localhost:3000
API_BASE_URL=http://localhost:3001
USERNAME=testuser
PASSWORD=secret
```

---

### 4️⃣ Run Tests

```
ENV=prod pytest
```

---

### 5️⃣ View Allure Report

```
allure serve reports/allure-results
```

---

## 🧪 Test Types

### UI Tests

* Validate frontend interactions
* Located in `tests/ui/`

### API Tests

* Validate backend endpoints
* Located in `tests/api/`

### E2E Tests

* Combine UI + API
* Located in `tests/e2e/`

### DB Validation

* Validate data persistence
* Uses `db_client.py`

---

## 🔥 Key Features

* Hybrid framework (UI + API + DB)
* Environment-based config (.env)
* Page Object Model (POM)
* Service layer abstraction
* Allure reporting with screenshots
* Playwright tracing for debugging
* Reusable fixtures via conftest.py
* Token-based authentication
* CI/CD ready

---

## 🧠 Design Highlights

* **Separation of concerns**
* **Reusable components**
* **Fast execution using API-based login**
* **Fail-fast configuration validation**

---

## 🏆 Author

Anubhav Sikka
