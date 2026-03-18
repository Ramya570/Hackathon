# ----------------------------------------------------
# 0. Setup and Imports
# ----------------------------------------------------
import os
from fpdf import FPDF
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

# FIX: Tell load_dotenv to look for your specific file named 'story.env'
load_dotenv('story.env') 

# Retrieve the API Key from the loaded environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

# Global variables for state management
generated_story = None
pdf_filename = "Shreya_Storybook_Gemini_Final.pdf"
client = None

# ----------------------------------------------------
# 1. User Input and Prompt Assembly
# ----------------------------------------------------

def get_user_input():
    print("--- AI Children's Story Creator (Free Tier) ---")
    
    # 1. Collect Input
    name = input("1. Enter the child's Name: ")
    age = input("2. Enter the child's Age: ")
    animal = input("3. Enter their favorite Animal: ")
    color = input("4. Enter their favorite Color: ")
    theme = input("5. Enter the Story Theme (e.g., Space Rescue, Friendly Dragon): ")
    
    # 2. Assemble Detailed Prompt
    prompt = f"""
    You are a friendly, imaginative children's book author. Write a short, comforting bedtime story for a {age}-year-old named {name}. 
    The main character is a gentle {color} {animal}. 
    The central theme of the story is "{theme}".
    
    The story must be structured into exactly 4 chapters (around 100 words each). 
    The tone must be gentle and positive.

    Format your output clearly and strictly with the markers: **TITLE:**, **CHAPTER 1:**, **CHAPTER 2:**, **CHAPTER 3:**, **CHAPTER 4:**
    """
    return prompt, name

# ----------------------------------------------------
# 2. Gemini Text Generation
# ----------------------------------------------------

def initialize_gemini_client():
    """Initializes client and provides a clear error if the key is missing."""
    global client
    if not GEMINI_API_KEY:
        print("\n--- FATAL ERROR: GEMINI_API_KEY is not found. ---")
        print("Please check your key is set inside the 'story.env' file.")
        return False
    try:
        # Client initialized using key from environment variable
        client = genai.Client()
        return True
    except Exception as e:
        print(f"\n--- ERROR: Failed to initialize Gemini Client: {e} ---")
        return False

def generate_text_story(story_prompt):
    global generated_story
    if not client:
        return False
        
    try:
        print("\n--- Sending prompt to Gemini 2.5 Flash... Please wait. ---")
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                {"role": "user", "parts": [{"text": story_prompt}]}
            ],
            config=genai.types.GenerateContentConfig(
                temperature=0.8
            )
        )
        
        story_text = response.text.strip()
        
        if not story_text:
            print("\n--- DEBUG: API returned an empty story. ---")
            return False
            
        generated_story = story_text
        print("\n--- Story Text Generated Successfully! ---")
        print("\n--- PREVIEW OF GENERATED STORY ---\n" + generated_story) 
        print("---------------------------------------")
        return True
        
    except APIError as e:
        print(f"\n--- DEBUG: A Gemini API Error occurred (Check your key/quota): {e} ---")
        return False
    except Exception as e:
        print(f"\n--- DEBUG: An unexpected Python error occurred during API call: {e} ---")
        return False

# ----------------------------------------------------
# 3. PDF Creation (Final Assembly with Encoding Fix)
# ----------------------------------------------------

def create_storybook_pdf(text, filename, child_name):
    if not text:
        print("Cannot create PDF: Story text is missing.")
        return

    print("\n--- Creating PDF Storybook... ---")
    
    # 1. Initialize PDF object 
    pdf = FPDF(unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # FIX 1: Comprehensive character replacement to avoid ALL encoding errors
    safe_text = text.replace('–', '-')        # Replace long dash
    safe_text = safe_text.replace('—', '-')      # Replace em dash
    safe_text = safe_text.replace('“', '"')     # Replace opening double quote
    safe_text = safe_text.replace('”', '"')     # Replace closing double quote
    safe_text = safe_text.replace('‘', "'")     # Replace opening single quote
    safe_text = safe_text.replace('’', "'")     # Replace curly apostrophe (YOUR FIX)
    safe_text = safe_text.replace('**', '')    # Clean up AI markers
    
    parts = safe_text.split('\n')
    
    # Set default font (safe for ASCII characters after replacement)
    pdf.set_font("Arial", size=12) 
    
    for line in parts:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith("TITLE:"):
            # Cover Page
            pdf.add_page()
            title = line.replace("TITLE:", "").strip()
            pdf.set_font("Arial", "B", 24)
            pdf.cell(0, 30, title, 0, 1, 'C')
            pdf.set_font("Arial", "", 14)
            pdf.cell(0, 10, f"A Story for {child_name}", 0, 1, 'C')
            pdf.ln(10)
        
        elif line.startswith("CHAPTER"):
            # Image Placeholder and Chapter Title
            pdf.add_page()
            
            # --- IMAGE PLACEHOLDER DRAWING ---
            pdf.set_fill_color(220, 220, 220) 
            pdf.rect(10, 20, 180, 100, 'F') 
            pdf.set_font("Arial", "I", 12)
            pdf.set_text_color(100, 100, 100) 
            pdf.set_xy(10, 65)
            pdf.cell(180, 10, f"[Illustration Placeholder for {line}]", 0, 0, 'C')
            pdf.set_text_color(0, 0, 0) # Reset text color
            pdf.ln(100) # Move cursor down past the image box
            # --------------------------------
            
            # Chapter Title and Content (starts on the next line)
            pdf.set_font("Arial", "B", 16)
            pdf.multi_cell(0, 10, line, 0, 'L')
            pdf.ln(2)
        else:
            # Chapter Content
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 6, line)
            pdf.ln(1)
            
    try:
        # FINAL FIX: Output call without the 'encoding' argument
        pdf.output(filename, 'F') 
        print(f"\n✅ SUCCESS! Storybook saved as: {filename} in your project folder.")
    except Exception as e:
        print(f"❌ Error saving PDF: {e}")

# ----------------------------------------------------
# 4. Main Execution Block
# ----------------------------------------------------

if __name__ == "__main__":
    
    # 1. Initialize API Client
    if initialize_gemini_client():
        # 2. Get user inputs
        prompt_text, child_name = get_user_input()
        
        # 3. Generate Story Text 
        if generate_text_story(prompt_text):
            
            # 4. Create Final PDF
            create_storybook_pdf(generated_story, pdf_filename, child_name)
            
    print("\nProject finished.")