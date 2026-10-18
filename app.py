import streamlit as st
import qrcode
from io import BytesIO
from datetime import datetime

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="QR Code Generator",
    page_icon="🔳",
    layout="centered"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #777;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .qr-box {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #ddd;
        margin-top: 20px;
    }

    .info-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #f5f5f5;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="title">QR Code Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Generate QR codes instantly using Python</div>',
    unsafe_allow_html=True
)

# -----------------------------
# Session State
# -----------------------------
if "qr_image" not in st.session_state:
    st.session_state.qr_image = None

if "qr_data" not in st.session_state:
    st.session_state.qr_data = ""

# -----------------------------
# Input Section
# -----------------------------
st.subheader("Enter Your Information")

input_type = st.selectbox(
    "Select QR Code Type",
    [
        "Text",
        "Website URL",
        "Email",
        "Phone Number",
        "Wi-Fi"
    ]
)

# -----------------------------
# Dynamic Input
# -----------------------------
if input_type == "Text":

    user_input = st.text_area(
        "Enter text",
        placeholder="Enter your text here..."
    )

elif input_type == "Website URL":

    user_input = st.text_input(
        "Enter website URL",
        placeholder="https://example.com"
    )

elif input_type == "Email":

    email = st.text_input(
        "Email Address",
        placeholder="example@gmail.com"
    )

    subject = st.text_input(
        "Email Subject"
    )

    message = st.text_area(
        "Email Message"
    )

    if email:
        user_input = (
            f"mailto:{email}"
            f"?subject={subject}"
            f"&body={message}"
        )
    else:
        user_input = ""

elif input_type == "Phone Number":

    phone = st.text_input(
        "Enter phone number",
        placeholder="+91XXXXXXXXXX"
    )

    user_input = f"tel:{phone}" if phone else ""

elif input_type == "Wi-Fi":

    wifi_name = st.text_input(
        "Wi-Fi Name (SSID)"
    )

    wifi_password = st.text_input(
        "Wi-Fi Password",
        type="password"
    )

    security = st.selectbox(
        "Security",
        ["WPA", "WEP", "nopass"]
    )

    if wifi_name:
        user_input = (
            f"WIFI:T:{security};"
            f"S:{wifi_name};"
            f"P:{wifi_password};;"
        )
    else:
        user_input = ""

# -----------------------------
# Buttons
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    generate = st.button(
        "Generate QR Code",
        use_container_width=True
    )

with col2:
    clear = st.button(
        "Clear",
        use_container_width=True
    )

# -----------------------------
# Clear Button
# -----------------------------
if clear:
    st.session_state.qr_image = None
    st.session_state.qr_data = ""
    st.rerun()

# -----------------------------
# Generate QR Code
# -----------------------------
if generate:

    if not user_input.strip():

        st.warning(
            "Please enter some information first."
        )

    else:

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )

        qr.add_data(user_input)
        qr.make(fit=True)

        img = qr.make_image(
            fill_color="black",
            back_color="white"
        )

        # Convert image to bytes
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        st.session_state.qr_image = buffer.getvalue()
        st.session_state.qr_data = user_input

# -----------------------------
# Display QR Code
# -----------------------------
if st.session_state.qr_image:

    st.markdown(
        '<div class="qr-box">',
        unsafe_allow_html=True
    )

    st.subheader("Your QR Code")

    st.image(
        st.session_state.qr_image,
        width=300
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    # -----------------------------
    # Download
    # -----------------------------
    filename = (
        "qr_code_"
        + datetime.now().strftime("%Y%m%d_%H%M%S")
        + ".png"
    )

    st.download_button(
        label="Download QR Code",
        data=st.session_state.qr_image,
        file_name=filename,
        mime="image/png",
        use_container_width=True
    )

    # -----------------------------
    # Information
    # -----------------------------
    st.markdown(
        '<div class="info-box">',
        unsafe_allow_html=True
    )

    st.write("QR Code successfully generated!")

    st.write(
        f"Type: **{input_type}**"
    )

    st.write(
        f"Generated: **{datetime.now().strftime('%d-%m-%Y %I:%M %p')}**"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "Built with Python, Streamlit and QRCode"
)