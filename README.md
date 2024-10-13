# Flask Application: Course Management System - Dragos IT Academy

![img](./application/static/images/gif.gif)

## Table of Content

- [Overview](#overview)
- [Navigation Bar Components](#navigation-bar-components)
- [Admin Features](#admin-features)
- [Installation and Setup](#installation-and-setup)
- [Database Schema](#database-schema)
  - [User Model](#user-model)
  - [Course Model](#course-model)
  - [Enrollment Model](#enrollment-model)

## Overview

This project is a Flask-based web application for managing course enrollments, registrations, and course data. The system includes the following features:

- User registration and login.
- Admin privileges for adding, editing, and deleting courses.
- Enrolling in courses and viewing enrolled courses.
- Accessible via responsive navigation bars.

## Navigation Bar Components

1. **Home**

- **URL**: `/index`
- **Access**: Public
- **Description**: This is the landing page of the website. It provides a welcoming message to users. If a user is logged in, a personalized greeting is displayed, otherwise, a prompt to login is shows.

2. **Classes**

- **URL**: `/courses`
- **Access**: Public
- **Description**: Displays the available courses. Users can browse the course offerings, and if they are logged in, they can enroll in any course.

If the user is an admin, they will see a delete button next to each course to remove them from the system.

3. **Add Course**

- **URL**: `/add_course`
- **Access**: Admin Only
- **Description**: This link is only visible to admins. It directs them admin to a form where they can add new courses to the system. The fields include `Course ID`, `Title`, `Description`, `Credits`, and `Term`. These fields are validated, and admin privileges are required to view this option in the navbar.

4. **Enrollment**

- **URL**: `/enrollment`
- **Access**: Logged-In Users Only
- **Description**: Displays the list of courses a user has enrolled in. This page will show the `Course ID`, `Title`, `Description`, `Credits`, and `Term` for each enrolled course. If a user has not enrolled in any courses, it displays a message stating "You are not enrolled in any class."

5. **Register**
`Course ID`, `Title`, `Description`, `Credits`, and `Term`

- **URL**: `/register`
- **Access**: Public
- **Description**: This allows new users to register for an account. The form contains fields for first name, last name, email, password, and a checkbox to allow users to register as admins if desired. Admin access is determined by a checkbox input during registration.

6. **Login**

- **URL**: `/login`
- **Access**: Public
- **Description**: Allows users to log into the application. After logging in, the session stores the user details, including whether they have admin privileges, and adjusts the navbar and access accordingly.

7. **Logout**

- **URL**: `/login`
- **Access**: Logged-In Users Only
- **Description**: Logs out the user and clears their session data. Once logged out, the navbar is updated to reflect the guest user experience (i.e., showing login and register options instead of user-specific features).

## Admin Features

When an admin is logged in, additional functionalities such as adding, editing, and deleting courses are available. The "Add Course" and "Delete" buttons are only visible to users with admin privileges.

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/k1lgor/flask.git
```

2. Install dependencies:

```bash
pip install uv
uv venv
uv pip install -r requirements.txt
```

3. Run the application:

```bash
flask run
```

## Database Schema

### User Model

- **Fields**: `id`, `first_name`,`last_name`,`email`,`password`,`is_admin`
- **Description**: Holds user information and determines if a user has admin privileges.

### Course Model

- **Fields**: `id`, `course_id`, `title`, `description`, `credits`, `term`.
- **Description**: Stores information about each course.

### Enrollment Model

- **Fields**: `id`, `user_id`, `course_id`.
- **Description**: Tracks which users are enrolled in which courses.
