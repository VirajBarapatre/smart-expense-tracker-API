# AI Collaboration Notes

## 1. Code Attribution (AI-Generated vs. Human-Written)

* **AI-Generated Baseline (~60%):**
  * Scaffolded basic FastAPI application structure and standard CRUD endpoint routes in `src/main.py`.
  * Generated initial Pydantic schema model boilerplate (`ExpenseCreate`, `Expense`) in `src/models.py`.
  * Generated initial unit test templates for basic HTTP GET and POST requests in `tests/test_api.py`.

* **Human-Authored & Refactored (~40%):**
  * **Storage Architecture (`src/storage.py`):** Designed and implemented the persistence layer (`ExpenseStorage` class) from scratch to handle both in-memory caching and persistent local JSON serialization/deserialization.
  * **Type Namespace Refactoring (`src/models.py`):** Diagnosed and resolved Pydantic model construction errors caused by lazy evaluation in Python 3.14 by manually aliasing `datetime.date` to `DateType`.
  * **Aggregation Logic (`src/storage.py`):** Wrote custom grouping and aggregation routines in `get_summary()` to handle case-insensitive category filtering and `YYYY-MM` monthly date formatting.
  * **Test Environment Isolation (`tests/test_api.py`):** Wrote the `reset_storage` pytest fixture to automatically clear in-memory state and disable disk persistence during test runs, preventing unit tests from mutating production/local data.

---

## 2. Validations, Refactoring & Quality Adjustments

* **Python 3.14 Compatibility Fix:**
  * **Issue:** AI generated model fields using `date: date = Field(...)`, which caused namespace collision and building errors (`PydanticUserError`) in Python 3.14.
  * **Human Action:** Updated imports to `from datetime import date as DateType` and defined the field as `date: DateType = Field(...)`.
* **Input Data Constraints:**
  * **Human Action:** Enforced `Field(..., gt=0)` on the expense `amount` attribute to ensure negative or zero monetary amounts are rejected at the edge with HTTP 422 status codes.
* **Floating-Point Precision:**
  * **Issue:** Floating-point arithmetic during aggregation sum operations led to minor accuracy drift (e.g., `$40.000000000000004`).
  * **Human Action:** Wrapped category and monthly subtotal calculations in explicit `round(..., 2)` calls to ensure clean currency totals.

---

## 3. Rejected AI Suggestions & Architectural Choices

* **Rejection 1: SQLite / SQLAlchemy ORM Layer**
  * **AI Suggestion:** The AI initially recommended setting up SQLite database migrations using SQLAlchemy/Alembic.
  * **Reason for Rejection:** Kept the architecture lean and lightweight per the problem brief ("no database required"). A clean, file-backed JSON storage module satisfied data persistence without introducing unnecessary ORM complexity.
* **Rejection 2: Global Middleware & OAuth2 Authentication**
  * **AI Suggestion:** Suggested adding JWT bearer token auth middleware.
  * **Reason for Rejection:** Excluded to avoid breaking automated test evaluation scripts and to strictly adhere to the 4-hour target scope.
* **Rejection 3: Destructive Overwrite on Re-hydration Failure**
  * **AI Suggestion:** AI proposed overwriting corrupt JSON data with an empty array upon launch.
  * **Reason for Rejection:** Refactored storage logic to catch `JSONDecodeError` gracefully without destroying existing corrupt files unexpectedly.