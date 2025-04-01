from fastapi import FastAPI
from transformers import pipeline

app = FastAPI()

pipe = pipeline("text2text-generation", model="google/flan-t5-small")

@app.get("/")
def home():
    return {"message": "Welcome to the Text Generation API!"}

@app.get('/generate')
def generate(text:str):
    output = pipe(text)
    return {"output":output[0]['generated_text']}# Import the FastAPI framework
# FastAPI is a modern, high-performance web framework for building APIs with Python
from fastapi import FastAPI

# Import the pipeline module from transformers
# Hugging Face's transformers library provides easy-to-use interfaces for working with
# state-of-the-art NLP models
from transformers import pipeline

# Initialize the FastAPI application
# This creates the main entry point for our API
app = FastAPI()

# Set up the text generation pipeline
# Parameters:
# - "text2text-generation": Task type - converts input text to output text
# - model: "google/flan-t5-small" - A 80M parameter instruction-tuned T5 model
#   FLAN-T5 models are fine-tuned on a variety of instruction-based tasks
#   and can follow natural language instructions
# 
# This pipeline handles:
# 1. Loading the model from Hugging Face Hub (first run will download it)
# 2. Setting up the tokenizer appropriate for this model
# 3. Managing the device placement (CPU/GPU)
# 4. Pre/post-processing for inputs/outputs
pipe = pipeline("text2text-generation", model="google/flan-t5-small")

# Define the root endpoint
# The @app.get("/") decorator routes HTTP GET requests for the URL "/" to this function
# This provides a simple health check and welcome message for the API
@app.get("/")
def home():
    """
    Root endpoint that returns a welcome message.
    Used for checking if the API is running.
    
    Returns:
        dict: A simple JSON response with a welcome message
    """
    return {"message": "Welcome to the Text Generation API!"}

# Define the text generation endpoint
# The @app.get("/generate") decorator routes GET requests for "/generate" to this function
# The text parameter will be passed as a query parameter, e.g., /generate?text=Hello
@app.get('/generate')
def generate(text: str):
    """
    Generate text based on the input using the FLAN-T5 Small model.
    
    Args:
        text (str): The input text/prompt for text generation
              
    Returns:
        dict: A JSON response containing the generated text in the 'output' field
        
    Examples:
        Request: GET /generate?text=Translate%20to%20French:%20Hello%20world
        Response: {"output": "Bonjour le monde"}
    """
    # Process the input text through the pipeline
    # The pipeline handles tokenization, model inference, and decoding
    # Returns a list of dictionaries, we take the first (and only) result
    output = pipe(text)
    
    # Return the generated text as a JSON response
    # Extracting the 'generated_text' field from the first (and only) result
    return {"output": output[0]['generated_text']}