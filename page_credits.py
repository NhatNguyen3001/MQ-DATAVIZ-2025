import streamlit as st
from PIL import Image, ImageOps, ImageDraw
from io import BytesIO
import requests


st.title("👥 Credit")


people = [
    {
        "name": "Dang Nhat Nguyen (Davis)",
        "degree": "Master of Information Technology (Artificial Intelligent)",
        "email": "dangnhat.nguyen@students.mq.edu.au",
        "image": "img/Nhat_img.png",
        "LinkedIn": "https://www.linkedin.com/in/dangnhatnguyen/"
    },
    {
        "name": "Dang Khanh Nguyen (Tobi)",
        "degree": "Bachelor of Information Technology (Data Science)",
        "email": "khanhdnguyen007@gmail.com",
        "image": "img/Khanh_img.jpg",
        "LinkedIn": "https://www.linkedin.com/in/khanhnguyendang007/"
    },
    {
        "name": "Kim To Thanh Vuong (Kayne)",
        "degree": "Bachelor of Information Technology (Data Science)",
        "email": "vuongkimtothanh@gmail.com",
        "image": "img/Thanh_img.jpg",
        "LinkedIn": "https://www.linkedin.com/in/kim-to-thanh-vuong-4a0b522a3/"
    },
    {
        "name": "Ha Bao Ngoc Dang",
        "degree": "Bachelor of Information Technology & Business Analyst (Data Science)",
        "email": "elsa.eira05@gmail.com",
        "image": "img/Ngoc_img.png",
        "LinkedIn": "https://www.linkedin.com/in/ha-bao-ngoc-dang-606173315/"
    },
    {
        "name": "Ha Linh Tran",
        "degree": "Bachelor of Commerce (Business Analytics)",
        "email": "tranlinh22052004@gmail.com",
        "image": "img/Linh_img.jpg",
        "LinkedIn": "https://www.linkedin.com/in/ha-linh-tran-96b546255/"
    }
]

AVATAR_SIZE = (260, 260)

def render_person(col, person):
    with col:
        # open + fix orientation (no loader fn)
        src = person["image"]
        try:
            if isinstance(src, str) and src.startswith("http"):
                r = requests.get(src, timeout=10)
                r.raise_for_status()
                img = Image.open(BytesIO(r.content))
            else:
                img = Image.open(src)
            img = ImageOps.exif_transpose(img)
        except Exception:
            img = None

        # resize + circular crop
        if img is not None:
            img = img.convert("RGBA")
            img = ImageOps.fit(img, AVATAR_SIZE, method=Image.LANCZOS, centering=(0.5, 0.5))
            mask = Image.new("L", AVATAR_SIZE, 0)
            ImageDraw.Draw(mask).ellipse((0, 0, *AVATAR_SIZE), fill=255)
            img.putalpha(mask)
            st.image(img)
        else:
            st.write("🖼️ Image not available")

        # name, degree, email, LinkedIn (centered)
        st.markdown(
            f"""
            <div style="text-align:center">
                <h4 style="margin:8px 0 4px 0">{person['name']}</h4>
                <div style="color:#666;margin-bottom:6px">{person['degree']}</div>
                <div style="margin-bottom:4px"><a href="mailto:{person['email']}">{person['email']}</a></div>
                <div><a href="{person['LinkedIn']}" target="_blank">LinkedIn</a></div>
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
