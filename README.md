# Stock Portfolio Dashboard

This project is a web-based application that enables users to manage stock orders, monitor session activity, and filter order history effectively. It is an adaptation of a custom dashboard I developed while working with a startup to streamline their stock and order management processes. The project has been refined and generalized to serve a broader audience with similar needs.
[**Watch a video walkthrough of the project**](https://youtu.be/d1HKRsfV5hc)

## Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Customization](#customization)
- [Contribution](#contribution)

## About the Project

This dashboard application is built to help users interact with stock order data efficiently. It supports features like secure user login, session timeout management, and the ability to filter and view order data by user and date. The interface is designed to be user-friendly, responsive, and customizable, allowing for personalized branding.

## Features

- **User Authentication**: Secure login functionality with hashed passwords.
- **Session Management**: Automatic session timeout with visual countdown.
- **Order Filtering**: View stock orders filtered by date and user.
- **Custom Greetings**: Multi-language greetings based on session user.
- **Custom Branding**: Replaceable logos and footer images to reflect your organization's identity.

## Project Structure

The project is organized as follows:

- `app.py`: Main Flask application managing the backend logic and routes.
- `user_management.py`: Script for creating and managing users in the database.
- `data.db`: SQLite database storing user credentials and session data.
- `order_history.csv`: Example dataset for importing initial order history.
- `static/`: Contains static files like stylesheets, scripts, and images.
  - `css/`
    - `styles.css`: Main stylesheet for the dashboard.
  - `js/`
    - `script.js`: JavaScript for session timeout management.
  - `images/`: Placeholder directory for logo and footer images.
- `templates/`: HTML templates for rendering web pages.
  - `dashboard.html`: Main dashboard interface.
  - `login.html`: Login page interface.

## Technologies Used

- **Flask**: Backend web framework for managing routes and logic.
- **SQLite**: Lightweight database for user and order data.
- **HTML5**: Markup language for structuring content.
- **CSS3**: Stylesheets for layout and design.
- **JavaScript**: For interactive and dynamic client-side functionality.

## Getting Started

Follow the steps below to set up and run the application.

### Dependencies

Ensure the following libraries are installed:

- Flask
- Flask-Bcrypt
- SQLite3

Install these dependencies using pip:

```bash
pip install flask flask-bcrypt
```

### Creating/Managing Users

Run the `user_management.py` to manage and add users to the database in order to log in to the dashboard.

### Running the Web Application

Start the application using `app.py`:

```bash
python app.py
```

Open your browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000) to access the dashboard.

## Customization

### Add Custom Branding

To personalize the application, replace the following files in the `static/images/` directory:

- **Logo**: Add your organization's logo as `logo.jpg`.
- **Footer Motto**: Add your organization's motto image as `motto.jpg`.

These will be reflected automatically in the header and footer of the dashboard.

## Contribution

Feel free to fork this repository and enhance the code. Contributions are always welcome! Submit a pull request for review, and let's improve this project together.
