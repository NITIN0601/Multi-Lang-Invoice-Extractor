from dotenv import load_dotenv
import os 

load_dotenv() # Which loads all the env varibales from .env
#GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

import streamlit as st
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini Pro Vision
model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input, image, prompt):
    """
    Gemini Model : 
    Parameters are taken in List format
    input: "AI Assistant - Expertize" : 
    image: "input Image" 
    prompt: "what message is resulted"
    """
    response = model.generate_content([input, image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    """
    Function : to convert the image into bytes 
    uploaded_file: Image input 
    return: image bytes 
    """
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")


# Streamlit app code working

st.set_page_config(page_title = " Multi-Lang Invoice Extractor ")
st.header("Gemini GenAI Application : Multi-Lang Invoice Extractor ")
input = st.text_input("Input Prompt: ",key = "input")
uploaded_file = st.file_uploader("Choose an image of the invoice .....", type=["jpg","jpeg","png"])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button(" Tell me about the invoice ")

input_prompt = """
You are an expert in understanding invoices. We will upload an image as inovice and you will have to anser any questions based on the uploaded invoice image.
"""

# If the Submit button is selected
if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is : ")
    st.write(response)
