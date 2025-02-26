import streamlit as st
import os
from PIL import Image
import json

def load_model():
    return None

def classify_image(image, model):
    return "Action"

model = load_model()

st.set_page_config(page_title="Pictures Hub", layout="wide")
st.image("logo_black.svg")

st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #1e1e2f, #252540);
        color: white;
        font-family: Arial, sans-serif;
    }
    .main-title {
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        color: #ffcc00;
        margin-bottom: 20px;
    }
    .navbar {
        background: linear-gradient(to right, #ff6600, #ff3300);
        overflow: hidden;
        padding: 15px 10px;
        display: flex;
        justify-content: center;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3);
    }
    .navbar a {
        color: white;
        text-align: center;
        padding: 14px 20px;
        text-decoration: none;
        font-size: 20px;
        font-weight: bold;
        border-radius: 8px;
        transition: background 0.3s, transform 0.2s;
        margin: 0 10px;
    }
    .navbar a:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: scale(1.1);
    }
    .section {
        background: rgba(255, 255, 255, 0.1);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0px 4px 8px rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        margin: 20px;
    }
    .gallery-image {
        border-radius: 15px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
    }
    </style>
    <div class="navbar">
        <a href="/?nav=Home">Home</a>
        <a href="/?nav=Upload">Upload</a>
        <a href="/?nav=Gallery">Gallery</a>
        <a href="/?nav=Login">Login</a>
        <a href="/?nav=Signup">Signup</a>
    </div>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>Pictures Hub</div>", unsafe_allow_html=True)

query_params = st.experimental_get_query_params()
page = query_params.get("nav", ["Home"])[0]

def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as file:
            return json.load(file)
    return {}

def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file)

if page == "Home":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.header("Welcome to Pictures Hub!")
    st.write("Upload, browse, and download amazing images!")
    st.image("OIP.jpeg")
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Upload":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.header("Upload Your Image")
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image")
        save_path = os.path.join("gallery", uploaded_file.name)
        os.makedirs("gallery", exist_ok=True)
        img.save(save_path)
        category = classify_image(img, model)
        st.success(f"Image classified as: {category}")
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Gallery":
    st.header("Image Gallery")
    search_query = st.text_input("Search for an image")
    gallery_path = "gallery"
    os.makedirs(gallery_path, exist_ok=True)
    images = [f for f in os.listdir(gallery_path) if f.endswith(("jpg", "png", "jpeg"))]
    
    if search_query:
        images = [img for img in images if search_query.lower() in img.lower()]
    
    if images:
        cols = st.columns(3)
        for idx, img_name in enumerate(images):
            img_path = os.path.join(gallery_path, img_name)
            img = Image.open(img_path)
            with cols[idx % 3]:
                st.image(img, use_column_width=True, caption=img_name)
                with open(img_path, "rb") as file:
                    st.download_button("Download", file, file_name=img_name)
    else:
        st.write("No images found.")

elif page == "Login":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.header("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    users = load_users()
    if st.button("Login"):
        if username in users and users[username] == password:
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "Signup":
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.header("User Signup")
    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")
    users = load_users()
    if st.button("Signup"):
        if new_username in users:
            st.error("Username already exists. Choose another.")
        else:
            users[new_username] = new_password
            save_users(users)
            st.success("Signup successful! Redirecting to login...")
            st.experimental_set_query_params(nav=["Login"])
    st.markdown("</div>", unsafe_allow_html=True)
