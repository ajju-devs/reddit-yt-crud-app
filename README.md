# Reddit & YouTube CRUD Application (Automated Socials)

Welcome to the **Reddit & YouTube CRUD Application**, a project designed to interact seamlessly with Reddit and YouTube APIs, allowing users to perform CRUD operations on both platforms.

This project was created as a **minor project** for my college, **USAR, Delhi (GGSIPU EDC)**, during my internship under **ProdigalAI** (Project- Automated Socials). Below are the detailed features and implementation details of this project.

---

#### 
- Live Link: [https://crud-project.streamlit.app/](https://crud-project.streamlit.app/)

---

## 📌 Features

### Reddit CRUD Operations
- **Create Posts**: Supports text, image, and video posts on specified subreddits.
- **Read Posts**: Fetch and display recent posts by the authenticated user from a subreddit.
- **Update Posts**: Edit the content or title of existing posts.
- **Delete Posts**: Remove posts using their unique identifiers.

### YouTube CRUD Operations
- **Upload Videos**: Upload videos with customizable title, description, tags, and category.
- **Delete Videos**: Remove videos using their unique video ID.
- **List Videos**: Fetch and display a list of popular videos from YouTube.

---

## 🛠️ Tech Stack
- **Frontend**: Streamlit for an interactive and responsive UI.
- **APIs**:
  - `praw` for Reddit API integration.
  - `googleapiclient.discovery` for YouTube API interaction.
- **Backend**: Python for implementing business logic and API handling.
- **Other Libraries**: 
  - `tempfile`, `os`, `logging` for file handling and application logging.
  - `re` for URL parsing and post ID extraction.

---

## 🚀 How to Use

### Prerequisites
1. **Install Python**: Ensure Python 3.7+ is installed on your system.
2. **Install Dependencies**: Run the following command to install required libraries:
   ```bash
   pip install streamlit praw google-api-python-client
3. **Set Up Reddit API**: Obtain credentials (client_id, client_secret, user_agent) from your [Reddit Developer Portal](https://www.reddit.com/prefs/apps).
4. **Set Up YouTube API**: Generate an API key from the [Google Cloud Console](https://console.cloud.google.com/).

### Steps to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/ajju-devs/reddit-youtube-crud-app.git
   cd reddit-youtube-crud-app
2. Run the application:
    ```bash
    streamlit run main.py
3. Follow the UI to log in and start performing CRUD operations.

---

## 📄 File Structure
    reddit-youtube-crud-app/
    │
    ├── app.py                  # Main application file
    ├── README.md               # Project documentation
    └── requirements.txt        # List of dependencies

---

## 🌟 Highlights
1. **Interactive UI**: Easy-to-use interface for performing CRUD operations.
2. **Customization**: Supports multiple content types for Reddit posts and detailed video metadata for YouTube.
3. **Error Handling**: Includes informative messages and logs to guide users.

---

## 📚 Learning Outcomes
1. Mastery in API integration for real-world platforms.
2. Hands-on experience with Python libraries and Streamlit.
3. Improved debugging and application management skills.

## 👦 Author
- **Ajay Kumar**
- AI-ML
- USAR, Delhi (GGSIPU EDC)
- Github Profile- [@ajju-devs](https://github.com/ajju-devs)
