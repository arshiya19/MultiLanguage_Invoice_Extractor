from dotenv import load_dotenv
load_dotenv()  # Load all the environment variables from .env file

import os
import streamlit as st
from PIL import Image
import google.generativeai as genai

# Configure the Google Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##the input here is what we want the llm model to behave 
def get_gemini_response(input_prompt, image, user_prompt):
    response = model.generate_content([input_prompt, image, user_prompt])
    return response.text

# Load the Gemini Pro Vision model
model = genai.GenerativeModel('gemini-pro-vision')

# Creating the Streamlit app
st.set_page_config(page_title="MultiLanguage Invoice Extractor")

st.header("MultiLanguage Invoice Extractor")

# Box for user input
user_input = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose the image of the invoice..", type=["jpeg", "jpg", "png"])

# Uploaded file should be seen on the app
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

submit = st.button("Tell me about the invoice")

input_prompt = """
You are an expert in understanding invoices. We will upload an image as an Invoice and you have to answer any questions based on the uploaded invoice image.
"""

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_part = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_part
    else:
        raise FileNotFoundError("No file uploaded")

# If submit button is clicked
if submit:
    if uploaded_file is not None:
        image_data = input_image_details(uploaded_file)
        response = get_gemini_response(input_prompt, image_data, user_input)
        st.subheader("The response is")
        st.write(response)
    else:
        st.error("Please upload an invoice image.")




