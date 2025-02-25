import streamlit as st
import os
from PIL import Image
import shutil
import json

# Dummy function to load a pretrained model for classification (replace with actual model)
def load_model():
    return None

# Dummy function for classification (replace with real inference code)
def classify_image(image, model):
    return "Action"

# Load model
model = load_model()

# Streamlit UI
st.set_page_config(page_title="Pictures Hub", layout="wide")
st.image("logo_black.svg")

# Custom CSS for Navigation Bar
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 50px;
        font-weight: bold;
        color: #ff6600;
    }
    .sidebar-text {
        font-size: 18px;
        color: #ffffff;
    }
    .gallery-image {
        border-radius: 15px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
    }
    .navbar {
        background-color: #333;
        overflow: hidden;
        padding: 10px 20px;
        display: flex;
        justify-content: space-around;
    }
    .navbar a {
        float: left;
        display: block;
        color: white;
        text-align: center;
        padding: 14px 16px;
        text-decoration: none;
        font-size: 20px;
        border-radius: 5px;
    }
    .navbar a:hover {
        background-color: #ff6600;
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

# Get Navigation Selection from URL
query_params =st.experimental_get_query_params()
page = query_params.get("nav", ["Home"])[0]

# Load user data
def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as file:
            return json.load(file)
    return {}

# Save user data
def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file)

# Home Page
if page == "Home":
    st.header("Welcome to Pictures Hub!")
    st.write("Upload, browse, and download amazing images!")
    st.image("OIP.jpeg","nature.jpeg")
   # st.image("nature.jpeg")

# Upload Page
elif page == "Upload":
    st.header("Upload Your Image")
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Image", use_column_width=True)
        
        # Save Image
        save_path = os.path.join("gallery", uploaded_file.name)
        os.makedirs("gallery", exist_ok=True)
        img.save(save_path)
        
        # Classify Image
        category = classify_image(img, model)
        st.success(f"Image classified as: {category}")
        st.write("Image saved successfully!")

# Gallery Page
elif page == "Gallery":
    st.header("Image Gallery")
    gallery_path = "gallery"
    os.makedirs(gallery_path, exist_ok=True)
    
    images = [f for f in os.listdir(gallery_path) if f.endswith(("jpg", "png", "jpeg"))]
    
    if images:
        cols = st.columns(3)
        for idx, img_name in enumerate(images):
            img_path = os.path.join(gallery_path, img_name)
            img = Image.open(img_path)
            with cols[idx % 3]:
                st.image(img, output_format="auto")
                with open(img_path, "rb") as file:
                    st.download_button("Download", file, file_name=img_name)
    else:
        st.write("No images in the gallery yet.")

# Login Page
elif page == "Login":
    st.header("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    users = load_users()
    
    if st.button("Login"):
        if username in users and users[username] == password:
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

# Signup Page
elif page == "Signup":
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

