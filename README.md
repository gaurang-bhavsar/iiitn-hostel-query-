# 🏫 Hostel Student Grievance System

A web application designed for hostel students to easily upload **queries** or **complaints** and track their resolution progress.

## ✨ Features

* **Complaint Submission:** A simple form on the landing page for students to submit new complaints/queries.
* **Complaint Tracking:** A personal **Dashboard** where students can see the status and progress of their submitted issues.
* **Secure Logout:** A dedicated button to securely end the user session.

---

## 💻 Technologies Used

This project is built using the following core technologies:

| Technology | Purpose |
| :--- | :--- |
| **Django** (Python) | Backend framework for routing, database interaction, and business logic. |
| **HTML** | Structuring the web pages. |
| **CSS** | Styling and layout of the user interface. |

---

## 🚀 Getting Started

Follow these steps to get a local copy of the project up and running on your machine.

### Prerequisites

You will need the following installed on your system:

* **Python 3.x**
* **Git**

### Installation

1.  **Clone the Repository**
    Open your terminal or command prompt and run the following command to download the project from GitHub:

    ```bash
    git clone [YOUR_GITHUB_REPO_URL]
    cd [YOUR_PROJECT_DIRECTORY_NAME]
    ```

    > **Note:** Replace `[YOUR_GITHUB_REPO_URL]` and `[YOUR_PROJECT_DIRECTORY_NAME]` with your actual repository URL and project folder name.

2.  **Create a Virtual Environment**
    It's best practice to use a virtual environment to manage dependencies.

    ```bash
    # Create the environment
    python3 -m venv venv 
    
    # Activate the environment (Linux/macOS)
    source venv/bin/activate 
    
    # Activate the environment (Windows)
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies**
    Install all required Python packages using `pip`. You'll need a `requirements.txt` file in your project root containing packages like `django`.

    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Migrations**
    Apply the database schema changes to create the necessary tables.

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create a Superuser (Optional but Recommended)**
    Create an administrative user to access the Django admin panel.

    ```bash
    python manage.py createsuperuser
    ```

### Running the Application

Start the Django development server:

```bash
python manage.py runserver
