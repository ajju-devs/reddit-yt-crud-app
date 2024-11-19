import streamlit as st
import praw
import os
import logging
import time
import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import tempfile

st.set_page_config(
    page_title="Reddit-YT CRUD Application",  
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# for credentials and reddit instance
if 'credentials_entered' not in st.session_state:
    st.session_state['credentials_entered'] = False
if 'youtube_credentials_entered' not in st.session_state:
    st.session_state['youtube_credentials_entered'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None

selected_section = st.sidebar.radio(
    "Choose a CRUD Option",
    ("Reddit CRUD", "YouTube CRUD")
)

# Reddit CRUD
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

    if limit is None:
        limit = float('inf')
    
    for post in subreddit.new(limit=limit):
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

def login_to_reddit(client_id, client_secret, user_agent, username, password):
    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password
        )
        reddit.user.me()  
        return reddit
    except Exception as e:
        st.error(f"Login failed: {e}")
        return None

# YouTube CRUD
def initialize_youtube(api_key):
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube
    except Exception as e:
        st.error(f"YouTube initialization failed: {e}")
        return None

def upload_video(youtube, title, description, tags, category, video_file_path):
    try:
        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags.split(","),
                    "categoryId": category
                },
                "status": {
                    "privacyStatus": "public"
                }
            },
            media_body=video_file_path
        )
        response = request.execute()
        return response.get('id')
    except HttpError as e:
        st.error(f"An error occurred: {e}")
        return None

def delete_video(youtube, video_id):
    try:
        request = youtube.videos().delete(id=video_id)
        request.execute()
        return "Video deleted successfully"
    except HttpError as e:
        st.error(f"An error occurred: {e}")
        return None

def list_videos(youtube, limit=5):
    try:
        request = youtube.videos().list(
            part="snippet",
            chart="mostPopular",
            maxResults=limit
        )
        response = request.execute()
        return response.get("items", [])
    except HttpError as e:
        st.error(f"An error occurred: {e}")
        return []

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

if selected_section == "Reddit CRUD":
    st.markdown('<div class="title">Reddit CRUD App Interface 🚀</div>', unsafe_allow_html=True)
elif selected_section == "YouTube CRUD":
    st.markdown('<div class="title" style="color: #FF0000;">YouTube CRUD App Interface 🚀</div>', unsafe_allow_html=True)

st.markdown('<div class="subtitle">ProdigalAI Internship Project</div>', unsafe_allow_html=True)
st.markdown('<a href="https://github.com/ajju-devs/reddit-crud-app" target="_blank" class="link">For GitHub Repository Click Here</a>', unsafe_allow_html=True)

if selected_section == "Reddit CRUD":
    if st.session_state['username']:
        st.markdown(f'<div class="username-display">Logged in as: {st.session_state["username"]}</div>', unsafe_allow_html=True)

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
                st.session_state['username'] = username 
                st.success("Logged in successfully!")
                time.sleep(2)
                st.experimental_rerun() 

    if st.session_state['credentials_entered']:
        reddit = st.session_state['reddit']
        st.write("Use this interface to create, read, update, and delete posts on Reddit.")
        subreddit_name_create = st.text_input("Enter Subreddit Name for Post Creation", "test", key="subreddit_create", help="Type the subreddit you want to post in")

        action = st.selectbox("Choose an Action", ["Create Post", "Read Posts", "Update Post", "Delete Post"], key="action")

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
            subreddit_name_read = st.text_input("Enter Subreddit Name to Read Posts", "test", key="subreddit_read", help="Type the subreddit you want to read posts from")

            if st.button("Read All Posts by User"):
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

        elif action == "Delete Post":
            post_url = st.text_input("Post URL to Delete", key="delete_url", help="Paste the post URL here to delete")
            if post_url:
                post_id = re.search(r"\/comments\/([^\/]+)", post_url)  
                if post_id:
                    post_id = post_id.group(1)
                else:
                    st.error("Invalid URL. Please provide a valid Reddit post URL.")
                
            if st.button("Delete Post", key="delete_button"):
                if post_id:
                    result = update_or_delete_post(reddit, "delete", post_id)
                    if result == "Post deleted successfully":
                        st.success(result, icon="✅")  
                    else:
                        st.error(result)
                else:
                    st.error("Error: Post ID extraction failed. Ensure URL is valid.")

elif selected_section == "YouTube CRUD":
    if not st.session_state['youtube_credentials_entered']:
        with st.form("youtube_credentials_form", clear_on_submit=True):
            api_key = st.text_input("YouTube API Key", type="password")
            submit_button = st.form_submit_button("Submit")
        
        if submit_button:
            youtube = initialize_youtube(api_key)
            if youtube:
                st.session_state['youtube_credentials_entered'] = True
                st.session_state['youtube'] = youtube
                st.success("YouTube API initialized successfully!")
                time.sleep(2)
                st.experimental_rerun()
    else:
        youtube = st.session_state['youtube']
        action = st.selectbox("Choose a YouTube Action", ["Upload Video", "Delete Video", "List Videos"])
        if action == "Upload Video":
            with st.form("youtube_upload_form", clear_on_submit=True):
                video_title = st.text_input("Video Title")
                video_description = st.text_area("Video Description")
                video_tags = st.text_input("Tags (comma-separated)")
                video_category = st.text_input("Category ID (e.g., 22 for People & Blogs)")
                video_file = st.file_uploader("Upload Video File", type=["mp4", "mov", "avi"])
                submit_button = st.form_submit_button("Upload Video")
        
            if submit_button:
                if video_title and video_file:
                    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
                        temp_file_path = temp_file.name
                        f = temp_file
                        f.write(video_file.read())

                    video_id = upload_video(youtube, video_title, video_description, video_tags, video_category, temp_file_path)
                    if video_id:
                        st.success(f"Video uploaded successfully! Video ID: {video_id}")
                    os.remove(temp_file_path)  
                else:
                    st.error("Please provide a title and a valid video file.")
                    
        elif action == "Delete Video":
            video_id = st.text_input("Enter Video ID to Delete")
            delete_button = st.button("Delete Video")
            
            if delete_button:
                if video_id:
                    result = delete_video(youtube, video_id)
                    st.success(result)
                else:
                    st.error("Please enter a valid Video ID.")

        elif action == "List Videos":
            limit = st.number_input("Number of Videos to List", min_value=1, max_value=50, value=5)
            list_button = st.button("List Videos")
            
            if list_button:
                videos = list_videos(youtube, limit)
                if videos:
                    for video in videos:
                        video_title = video["snippet"]["title"]
                        video_url = f"https://www.youtube.com/watch?v={video['id']}"
                        st.markdown(f"- **{video_title}**: [Watch Video]({video_url})")
                else:
                    st.error("No videos found or an error occurred.")


# Footer
st.markdown("""
<div class="footer">
    Built by: Ajay Kumar 10219011621 USAR AI-ML 4th year | 
    <a href="https://github.com/ajju-devs" target="_blank" style="
        display: inline-block;
        background-color: #4d00fe;
        color: white;
        padding: 5px 10px;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
    ">Ajay's Github</a>
</div>
""", unsafe_allow_html=True)
