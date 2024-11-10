import streamlit as st
import praw
import os
import logging
import time
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initial state for credentials and Reddit instance
if 'credentials_entered' not in st.session_state:
    st.session_state['credentials_entered'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None

# Define CRUD functions
def post_content(reddit, subreddit_name, title, content_type, content_body=None, content_path=None):
    subreddit = reddit.subreddit(subreddit_name)
    if content_type == "text":
        post = subreddit.submit(title, selftext=content_body)
    elif content_type == "image" and content_path:
        post = subreddit.submit_image(title, image_path=content_path)
    elif content_type == "video" and content_path:
        post = subreddit.submit_video(title, video_path=content_path)
    return post.id if post else None

def read_recent_posts(reddit, subreddit_name, limit=5, username=None):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    count = 0
    
    # If limit is None, set it to a very large number
    if limit is None:
        limit = float('inf')
    
    for post in subreddit.new(limit=limit):
        # Only add posts from the logged-in username
        if post.author and post.author.name == username:
            posts.append({
                "post_id": post.id,
                "title": post.title,
                "url": post.url
            })
            count += 1
        if count >= limit:
            break
    return posts

def update_or_delete_post(reddit, action, post_id, new_title=None, new_body=None):
    try:
        post = reddit.submission(id=post_id)
        if action == "update":
            if new_title:
                post.edit(new_body)
                return "Post updated successfully"
        elif action == "delete":
            post.delete()
            return "Post deleted successfully"
    except Exception as e:
        return f"Error: {e}"

# Function to login to Reddit with provided credentials
def login_to_reddit(client_id, client_secret, user_agent, username, password):
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password
        )
        reddit.user.me()  # Test login
        return reddit
    except Exception as e:
        st.error(f"Login failed: {e}")
        return None

# Titles and hyperlink display with color customization
st.markdown("""
<style>
    .title {
        font-size: 40px;
        color: #FF5733;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 20px;
        color: #0D98BA;
        font-weight: bold;
        margin-top: -10px;
    }
    .link {
        font-size: 16px;
        color: #FF7F50;
        font-weight: bold;
        margin-top: -15px;
    }
    .username-display {
        font-size: 18px;
        color: #04ba2b;
        margin-top: -10px;
    }
    .action-button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        border-radius: 8px;
        padding: 10px 20px;
        cursor: pointer;
    }
    .action-button:hover {
        background-color: #45a049;
    }
    .footer {
        color: white;
        text-align: center;
        padding: 10px;
        background-color: #525151;
        margin-top: 20px;
        font-size: 14px;
    }
    .footer a {
        color: white;
        text-decoration: none;
    }
    .footer a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Reddit CRUD App Interface</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">ProdigalAI Internship Project</div>', unsafe_allow_html=True)
st.markdown('<a href="https://github.com/ajju-devs" target="_blank" class="link">For GitHub Repository Click Here</a>', unsafe_allow_html=True)

# Display logged-in username if available
if st.session_state['username']:
    st.markdown(f'<div class="username-display">Logged in as: {st.session_state["username"]}</div>', unsafe_allow_html=True)

# Input for Reddit credentials with "Edit credentials" button
if not st.session_state['credentials_entered'] or st.button("Edit credentials"):
    with st.form("credentials_form", clear_on_submit=True):
        client_id = st.text_input("Client ID", type="password")
        client_secret = st.text_input("Client Secret", type="password")
        user_agent = st.text_input("User Agent")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Submit credentials")

    if submit_button:
        reddit = login_to_reddit(client_id, client_secret, user_agent, username, password)
        if reddit:
            st.session_state['reddit'] = reddit
            st.session_state['credentials_entered'] = True
            st.session_state['username'] = username  # Store the username for display
            st.success("Logged in successfully!")
            time.sleep(2)
            st.experimental_rerun()  # Rerun to hide credentials section

# Main app features load only if credentials are validated
if st.session_state['credentials_entered']:
    reddit = st.session_state['reddit']  # Use stored Reddit instance
    st.write("Use this interface to create, read, update, and delete posts on Reddit.")

    # Editable subreddit name
    subreddit_name_create = st.text_input("Enter Subreddit Name for Post Creation", "test", key="subreddit_create", help="Type the subreddit you want to post in")

    # CRUD actions dropdown
    action = st.selectbox("Choose an Action", ["Create Post", "Read Posts", "Update Post", "Delete Post"], key="action")

    # CRUD operations
    if action == "Create Post":
        title = st.text_input("Post Title", key="title", help="Title of the post")
        content_type = st.selectbox("Content Type", ["text", "image", "video"], key="content_type", help="Choose post content type")

        if content_type == "text":
            body = st.text_area("Post Content", key="body", help="Write the content of the post")
            if st.button("Submit Text Post", key="submit_text", help="Click to submit text post"):
                post_id = post_content(reddit, subreddit_name_create, title, content_type, content_body=body)
                if post_id:
                    st.success(f"Text post created with ID: {post_id}")
                    
        elif content_type == "image":
            image_path = st.file_uploader("Upload an Image", type=['jpg', 'jpeg', 'png'], key="image", label_visibility="collapsed")
            if image_path and st.button("Submit Image Post", key="submit_image"):
                with open("temp_image.jpg", "wb") as f:
                    f.write(image_path.read())
                post_id = post_content(reddit, subreddit_name_create, title, content_type, content_path="temp_image.jpg")
                if post_id:
                    st.success(f"Image post created with ID: {post_id}")
                os.remove("temp_image.jpg")
                
        elif content_type == "video":
            video_path = st.file_uploader("Upload a Video", type=['mp4'], key="video", label_visibility="collapsed")
            if video_path and st.button("Submit Video Post", key="submit_video"):
                with open("temp_video.mp4", "wb") as f:
                    f.write(video_path.read())
                post_id = post_content(reddit, subreddit_name_create, title, content_type, content_path="temp_video.mp4")
                if post_id:
                    st.success(f"Video post created with ID: {post_id}")
                os.remove("temp_video.mp4")

    elif action == "Read Posts":
        # Input for subreddit name
        subreddit_name_read = st.text_input("Enter Subreddit Name to Read Posts", "test", key="subreddit_read", help="Type the subreddit you want to read posts from")

        # Button to read posts from the subreddit
        if st.button("Read All Posts by User"):
            # Fetch all posts by the logged-in user in the given subreddit
            posts = read_recent_posts(reddit, subreddit_name_read, limit=None, username=st.session_state['username'])
            if posts:
                for post in posts:
                    st.write(f"**Post Title:** {post['title']}")
                    st.write(f"**Post ID:** {post['post_id']}")
                    st.write(f"**URL:** {post['url']}")
                    st.write("--------")
            else:
                st.write("No posts found for this user in this subreddit.")

    elif action == "Update Post":
        post_id = st.text_input("Post ID to Update", key="update_id")
        new_title = st.text_input("New Title", key="new_title")
        new_body = st.text_area("New Content", key="new_body")
        if st.button("Update Post", key="update_button"):
            result = update_or_delete_post(reddit, "update", post_id, new_title, new_body)
            st.write(result)

    # Delete Post
    elif action == "Delete Post":
        post_url = st.text_input("Post URL to Delete", key="delete_url", help="Paste the post URL here to delete")
        if post_url:
            post_id = re.search(r"\/comments\/([^\/]+)", post_url)  # Extract post ID from URL
            if post_id:
                post_id = post_id.group(1)
            else:
                st.error("Invalid URL. Please provide a valid Reddit post URL.")
            
        if st.button("Delete Post", key="delete_button"):
            if post_id:
                result = update_or_delete_post(reddit, "delete", post_id)
                if result == "Post deleted successfully":
                    st.success(result, icon="✅")  # Green background for success
                else:
                    st.error(result)  # Error message if something goes wrong
            else:
                st.error("Error: Post ID extraction failed. Ensure URL is valid.")

# Footer section
st.markdown("""
<div class="footer">
    Built by: Ajay Kumar 10219011621 USAR AI-ML 4th year | <a href="https://github.com/ajju-devs" target="_blank">GitHub- @ajju-devs</a>
</div>
""", unsafe_allow_html=True)