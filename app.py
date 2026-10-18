import streamlit as st
import qrcode
from io import BytesIO
from datetime import datetime
from urllib.parse import quote


def escape_wifi_value(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace(":", "\\:")
        .replace('"', '\\"')
    )

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

if "generated_at" not in st.session_state:
    st.session_state.generated_at = None

if "generated_type" not in st.session_state:
    st.session_state.generated_type = ""

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
        user_input = f"mailto:{quote(email, safe='@.+-_')}"
        query = []
        if subject:
            query.append(f"subject={quote(subject, safe='')}")
        if message:
            query.append(f"body={quote(message, safe='')}")
        if query:
            user_input += "?" + "&".join(query)
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
            f"S:{escape_wifi_value(wifi_name)};"
            f"P:{escape_wifi_value(wifi_password)};;"
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
    st.session_state.generated_at = None
    st.session_state.generated_type = ""
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
        st.session_state.generated_at = datetime.now()
        st.session_state.generated_type = input_type

# -----------------------------
# Display QR Code
# -----------------------------
if st.session_state.qr_image:
    with st.container(border=True):
        st.subheader("Your QR Code")
        st.image(st.session_state.qr_image, width=300)

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
    with st.container(border=True):
        st.write("QR Code successfully generated!")
        st.write(f"Type: **{st.session_state.generated_type}**")
        st.write(
            "Generated: **"
            f"{st.session_state.generated_at.strftime('%d-%m-%Y %I:%M %p')}**"
        )

# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "Built with Python, Streamlit and QRCode"
)