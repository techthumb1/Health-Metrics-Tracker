# Health Metrics Tracker

**Health Metrics Tracker** is a Flask-based web application that allows users to log, track, and visualize health metrics such as heart rate, blood pressure, and weight. Users can create accounts, log their health data, and view trends over time, helping them monitor and manage their wellness.

![Health Metrics Tracker Banner](app/static/Health-Metrics-Tracker.png) <!-- Replace with an actual banner image path -->

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)

---

## Features

- **User Authentication**: Secure user registration, login, and logout.
- **Health Metrics Logging**: Users can log heart rate, blood pressure, and weight.
- **Data Visualization**: Trends in health metrics are displayed using interactive charts.
- **Responsive Design**: Mobile-friendly design for access across devices.
- **Automated Updates**: GitHub Actions automate data updates for dynamic README elements.

---

## Tech Stack

| Technology          | Description                                       |
|---------------------|---------------------------------------------------|
| Python              | Core programming language                         |
| Flask               | Web framework used for backend routing            |
| PostgreSQL          | Database used for storing user and metric data    |
| SQLAlchemy          | ORM for database operations                       |
| Chart.js            | JavaScript library for data visualization         |
| Bootstrap           | CSS framework for responsive styling              |
| Alembic             | Database migration tool                           |
| dotenv              | For environment variable management               |
| Docker              | Containerization for deployment                   |
| QuickChart          | API for generating dynamic charts                 |
| GitHub Actions      | CI/CD for automating data updates                 |

---

## Project Metrics

| Metrics             | Status                                                                                           |
|---------------------|--------------------------------------------------------------------------------------------------|
| Build Status        | ![Build Status](https://img.shields.io/github/actions/workflow/status/techthumb1/Health-Metrics-Tracker/ci.yml) |
| Last Commit         | ![Last Commit](https://img.shields.io/github/last-commit/techthumb1/Health-Metrics-Tracker/ci.yml)      |
| Open Issues         | ![Issues](https://img.shields.io/github/issues/techthumb1/Health-Metrics-Tracker/ci.yml)                |
| License             | ![License](https://img.shields.io/github/license/techthumb1/Health-Metrics-Tracker/ci.yml)              |


---

## Dynamic Charts

This chart shows an example of real-time heart rate trends, updated via QuickChart:

![Dynamic Heart Rate Chart](https://quickchart.io/chart?c=%7B%22type%22%3A%22line%22%2C%22data%22%3A%7B%22labels%22%3A%5B%22Day%201%22%2C%22Day%202%22%2C%22Day%203%22%5D%2C%22datasets%22%3A%5B%7B%22label%22%3A%22Heart%20Rate%22%2C%22data%22%3A%5B80%2C85%2C90%5D%7D%5D%7D%7D)

You can modify the data by replacing the labels and `data` values with actual metrics.

---

## Installation

### Prerequisites

- **Python 3.10.14+**
- **PostgreSQL** installed and running

### Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/health-metrics-tracker.git
   cd health-metrics-tracker

---
2. **Set Up Virtual Environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows, use `venv\Scripts\activate`
    ```

---
3. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

---
4. **Set Up Database**:

- Create a PostgreSQL database and user.
- Update `.env` file with your database credentials:

    ``` Plain Text
    SECRET_KEY=your_secret_key
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=health_metrics_db
    ```

---
5. **Run Database Migrations**:

    ```bash
    flask db upgrade
    ```

---
6. **Start the Application**:

    ```bash
    flask run
    ```

---
### Usage

1. Register: Go to /register to create a new account.
2. Login: Log in with your credentials at /login.
3. Dashboard: View your logged health metrics and data visualization.
4. Log Health Metrics: Add new entries for heart rate, blood pressure, and weight.

---
### Screenshots

1. Registration Page

2. Dashboard with Data Visualization

3. Log Metrics Page

---
### Future Enhancements

- Advanced Analytics: Provide health insights based on logged metrics.
- Additional Metrics: Support more health metrics, like body temperature or oxygen saturation.
- Export Data: Allow users to export their data as CSV or PDF.
- Notifications: Reminders for users to log metrics daily or weekly.

---
### Contributing

We welcome contributions to the Health Metrics Tracker project! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature.
3. Submit a pull request detailing the changes.

For any questions, feel free to reach out to the project maintainers.

---
### License

This project is licensed under the MIT License. See the LICENSE file for more information.

---
### Note

- Environment Variables: Remember to keep your .env file secure and avoid committing it to version control.
- Database Configuration: Make sure your PostgreSQL database is running and accessible for seamless operation.
