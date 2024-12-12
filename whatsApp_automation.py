import streamlit as st
import pywhatkit as kit
import pyautogui
import time
import os

# Configure Streamlit app
st.set_page_config(page_title="WhatsApp Automation",
                   layout="wide", page_icon="🪀")

# Add background image via CSS and set text color to black
st.markdown("""
    <style>
        .stApp {
            background-image: url("https://overbr.com.br/wp-content/uploads/2018/05/WhatsApp-Business.jpg");
            background-size: cover;
            background-position: center center;
            background-attachment: fixed;
        }
        .main-heading {
            font-size: 2.5rem;
            color: #ffffff;  /* Set the text color to black */
            text-shadow: 2px 2px 5px #000000;
            text-align: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .stTextInput, .stTextArea {
            font-size: 16px;
            border-radius: 10px;
            color: #ffffff;  /* Set text color in inputs and text areas to black */
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            border-radius: 10px;
            padding: 10px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stSelectbox>div {
            font-size: 18px;
            color: #ffffff;  /* Set text color in dropdown to black */
        }
        .stMarkdown {
            color: #ffffff;  /* Set the color of markdown text to black */
        }
    </style>
""", unsafe_allow_html=True)

# Main heading
st.markdown('<h1 class="main-heading">📱💬 WhatsApp Automation Web App 🚀</h1>',
            unsafe_allow_html=True)

# Function to send a message and logout
def send_message(phone, message, hour, minute):
    kit.sendwhatmsg(phone, message, hour, minute)
    st.success("✅ Message sent successfully!")
    logout()

# Function to send an image and optional additional text, then logout
def send_image(recipient, image_file, caption, additional_text):
    # Save uploaded image temporarily
    if image_file is not None:
        temp_image_path = os.path.join("temp", image_file.name)
        os.makedirs("temp", exist_ok=True)
        with open(temp_image_path, "wb") as f:
            f.write(image_file.getbuffer())
        
        # Send the image with caption
        kit.sendwhats_image(recipient, temp_image_path, caption)
        st.success("✅ Image sent successfully!")
        
        # Adding a small delay before sending additional text
        if additional_text:
            time.sleep(3)  # Wait for WhatsApp to process the image
            # Using pyautogui to send the additional text
            pyautogui.write(additional_text)  # Type the additional text
            pyautogui.press('enter')  # Send the text message
            st.success("📜 Additional text sent successfully!")
        
        # Remove the temporary image file
        os.remove(temp_image_path)
        st.info("🗑 Temporary file deleted.")
        
        # Logout
        logout()
    else:
        st.error("❌ No image file uploaded!")

# Function to send a group message and logout
def send_group_message(group_id, message, hour, minute):
    kit.sendwhatmsg_to_group(group_id, message, hour, minute)
    st.success("✅ Group message sent successfully!")
    logout()

# Function to send an instant group message and logout
def send_instant_group_message(group_id, message):
    kit.sendwhatmsg_to_group_instantly(group_id, message)
    st.success("⚡ Instant group message sent successfully!")
    logout()

# Function to logout from WhatsApp Web
def logout():
    time.sleep(2)  # Wait 2-3 seconds before logging out
    pyautogui.hotkey("ctrl", "w")  # Close the WhatsApp Web tab
    st.success("🚪 Logged out from WhatsApp Web!")

# Streamlit App
st.title("WhatsApp Automation App 📲")
st.write("Automate sending messages, images, and group communications via WhatsApp Web! 🔥")

# Menu for operations
option = st.selectbox("Choose an action 🔧", ["Send Message ✉️", "Send Image 🖼️", "Send Group Message 🗨️", "Send Instant Group Message ⚡"])

if option == "Send Message ✉️":
    phone = st.text_input("Phone Number (with country code, e.g., +91XXXXXXXXXX): 📞")
    message = st.text_area("Message 📝:")
    hour = st.number_input("Hour (24-hour format): ⏰", min_value=0, max_value=23, step=1)
    minute = st.number_input("Minute: ⏱️", min_value=0, max_value=59, step=1)
    if st.button("Send Message 💌"):
        send_message(phone, message, hour, minute)

elif option == "Send Image 🖼️":
    recipient = st.text_input("Recipient (Phone Number or Group ID): 👤")
    image_file = st.file_uploader("Upload an Image: 📸", type=["jpg", "jpeg", "png"])
    caption = st.text_input("Caption (optional): 🏷️")
    additional_text = st.text_area("Additional Text (optional): ✍️")
    if st.button("Send Image 🖼️"):
        send_image(recipient, image_file, caption, additional_text)

elif option == "Send Group Message 🗨️":
    group_id = st.text_input("Group ID: 👥")
    message = st.text_area("Message 📝:")
    hour = st.number_input("Hour (24-hour format): ⏰", min_value=0, max_value=23, step=1)
    minute = st.number_input("Minute: ⏱️", min_value=0, max_value=59, step=1)
    if st.button("Send Group Message 🗣️"):
        send_group_message(group_id, message, hour, minute)

elif option == "Send Instant Group Message ⚡":
    group_id = st.text_input("Group ID: 👥")
    message = st.text_area("Message 📝:")
    if st.button("Send Instant Group Message ⚡"):
        send_instant_group_message(group_id, message)

# Logout Button
if st.button("Logout from WhatsApp Web 🚪"):
    logout()
