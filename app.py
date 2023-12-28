from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import fitz # PyMuPDF which uses PDF files

load_dotenv() # Which loads all the env varibales from .env

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
        # Check if the uploaded file is a PDF
        if uploaded_file.type == 'application/pdf':
            # Convert PDF to image
            images = pdf_to_images(uploaded_file)
            return images
        else:
            # For other image types, read the file into bytes
            bytes_data = uploaded_file.getvalue()
            image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
            return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")



def pdf_to_images(uploaded_file):
    pdf_images = []
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img_byte_array = BytesIO()
        img.save(img_byte_array, format="PNG")
        pdf_images.append({"image": img_byte_array.getvalue(), "page_num": page_num + 1})

    pdf_document.close()
    return pdf_images


# Streamlit app code working
st.set_page_config(page_title = " Multi-Lang Invoice Extractor ")
st.header("Gemini GenAI Application : Multi-Lang Invoice Extractor ")
input = st.text_input("Input Prompt: ",key = "input")
uploaded_file = st.file_uploader("Choose an image of the invoice .....", type=["jpg","jpeg","png","pdf"])
images = []

if uploaded_file is not None:
    if uploaded_file.type == 'application/pdf':
        images = pdf_to_images(uploaded_file)
    else:
        images = [{"image": Image.open(uploaded_file).convert("RGB").save(None, "PNG"), "page_num": 1}]
   
for image_data in images:
    st.image(Image.open(BytesIO(image_data["image"])), caption=f"Page {image_data['page_num']}", use_column_width=True)

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
