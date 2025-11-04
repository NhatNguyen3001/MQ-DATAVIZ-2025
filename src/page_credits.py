import streamlit as st
from PIL import Image, ImageOps, ImageDraw
from io import BytesIO
import requests
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
IMG_PATH = PROJECT_ROOT / "img"

st.title("👥 Credits")


people = [
    {
        "name": "Dang Nhat Nguyen (Davis)",
        "degree": "Master of Information Technology (Artificial Intelligence)",
        "email": "davisnguyen3001@gmail.com",
        "image": IMG_PATH / "Nhat_img.png",
        "LinkedIn": "https://www.linkedin.com/in/dangnhatnguyen/"
    },
    {
        "name": "Dang Khanh Nguyen (Tobi)",
        "degree": "Bachelor of Information Technology (Data Science)",
        "email": "khanhdnguyen007@gmail.com",
        "image": IMG_PATH / "Khanh_img.jpg",
        "LinkedIn": "https://www.linkedin.com/in/khanhnguyendang007/"
    },
    {
        "name": "Kim To Thanh Vuong (Kayne)",
        "degree": "Bachelor of Information Technology (Data Science)",
        "email": "vuongkimtothanh@gmail.com",
        "image": IMG_PATH / "Thanh_img.jpg",
        "LinkedIn": "https://www.linkedin.com/in/kim-to-thanh-vuong-4a0b522a3/"
    },
    {
        "name": "Ha Bao Ngoc Dang (Elsa)",
        "degree": "Bachelor of Information Technology (Information system, business analyst and data science)",
        "email": "elsa.eira05@gmail.com",
        "image": IMG_PATH / "Ngoc_img.png",
        "LinkedIn": "https://www.linkedin.com/in/ha-bao-ngoc-dang-606173315/"
    },
    {
        "name": "Ha Linh Tran",
        "degree": "Bachelor of Commerce (Business Analytics)",
        "email": "tranlinh22052004@gmail.com",
        "image": IMG_PATH / "Linh_img.jpg",
        "LinkedIn": "https://www.linkedin.com/in/ha-linh-tran-96b546255/"
    }
]

AVATAR_SIZE = (260, 260)

def render_person(col, person):
    with col:

        src = person["image"]
        img = Image.open(src)
        img = ImageOps.exif_transpose(img)
        

        if img is not None:
            img = img.convert("RGBA")
            avatar_size = (260, 260)           # same as your global
            img = ImageOps.fit(img, avatar_size, method=Image.LANCZOS, centering=(0.5, 0.5))
            mask = Image.new("L", avatar_size, 0)
            ImageDraw.Draw(mask).ellipse((0, 0, *avatar_size), fill=255)
            img.putalpha(mask)

            # --- center the image ---
            l, mid, r = st.columns([1, 3, 1])  # adjust middle weight if needed
            with mid:
                st.image(img, width=avatar_size[0])


        # --- centered text ---
        name = person.get("name",""); degree = person.get("degree","")
        email = person.get("email",""); linkedin = person.get("LinkedIn","")
        st.markdown(
            f"""
                <div style="width:{AVATAR_SIZE[0]}px; margin:8px auto 0 auto; text-align:center">
                    <h4 style="margin:8px 0 4px 0">{name}</h4>
                    <div style="color:#666; margin-bottom:6px">{degree}</div>
                    <div style="margin-bottom:4px"><a href="mailto:{email}">{email}</a></div>
                    <div><a href="{linkedin}" target="_blank">LinkedIn</a></div>
                </div>
                """,
                unsafe_allow_html=True
            )


# ---- Row 1: exactly 3 cards ----
row1 = st.columns(3, gap="large")
for i, c in enumerate(row1):
    render_person(c, people[i])

# ---- Row 2: exactly 2 cards, centered ----
# spacers make the two cards centered: [spacer, card, card, spacer]
sp_left, c1, c2, sp_right = st.columns([1, 3, 3, 1], gap="large")
render_person(c1, people[3])
render_person(c2, people[4])
