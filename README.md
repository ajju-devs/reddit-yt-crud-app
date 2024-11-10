# Reddit CRUD App Interface

A Streamlit-based interface for creating, reading, updating, and deleting Reddit posts. This project was developed as part of an internship with **ProdigalAI** and serves as a functional tool for handling Reddit content efficiently via a user-friendly GUI.

## Features
- **Post Creation**: Supports text, image, and video posts to specified subreddits.
- **Post Reading**: Retrieve recent posts by the logged-in user from a chosen subreddit.
- **Post Update**: Edit content or titles of existing posts.
- **Post Deletion**: Remove posts directly from the app interface.
- **Responsive Interface**: Styled and customized with Streamlit for an intuitive user experience.

## Table of Contents
- [Setup and Installation](#setup-and-installation)
- [Usage Guide](#usage-guide)
- [Folder Structure](#folder-structure)
- [App Interface Design](#app-interface-design)
- [Acknowledgments](#acknowledgments)

---

## Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ajju-devs/reddit-crud-app.git
2. **Navigate to Project Directory**
   ```bash
   cd reddit-crud-app
3. **Install Requirements Install the necessary packages from requirements.txt:**
   ```bash
   pip install -r requirements.txt
4. **Configure Streamlit Ensure the config.toml file in .streamlit folder is correctly set:**
   ```toml
   [server]
   headless = true
   enableCORS = true
   enableXsrfProtection = true
   port = 8501
