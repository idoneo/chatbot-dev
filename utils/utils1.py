from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client correctly
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))  # Changed this line

def get_initial_message():
    """
    Returns the initial messages to start the conversation.
    """
    messages = [
        {"role": "system", "content": "You are a Baseball History and Sports Specialist"},
        {"role": "user", "content": "I want to know about baseball teams performance"},
        {"role": "assistant", "content": "That's awesome, what do you want to know about Baseball"}
    ]
    return messages

def get_chatgpt_response(messages, model="gpt-4"):
    """
    Fetch a response from OpenAI's chat completion API with error handling.

    Args:
        messages (list): A list of message dictionaries with 'role' and 'content'.
        model (str): The model name to use (e.g., 'gpt-4' or 'gpt-3.5-turbo').

    Returns:
        str: The response content from the assistant, or None if an error occurs.
    """
    try:
        print(f"Sending request to OpenAI API with model: {model}")
        print(f"Messages being sent: {messages}")
        
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        
        print(f"Full API response: {response}")
        print(f"Response ID: {response.id}")
        print(f"Model used: {response.model}")
        print(f"Total tokens used: {response.usage.total_tokens}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Completion tokens: {response.usage.completion_tokens}")
        print(f"Response content: {response.choices[0].message.content}")
        
        return response.choices[0].message.content

    except Exception as e:
        print(f"Error during API call: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # Additional error context for common issues
        if "Incorrect API key" in str(e):
            print("API key validation failed. Please check your OpenAI API key.")
        elif "Rate limit" in str(e):
            print("Rate limit exceeded. Please wait before making more requests.")
        elif "Maximum context length" in str(e):
            print(f"Token limit exceeded for model {model}. Try reducing input size or using a different model.")
        elif "Invalid request" in str(e):
            print("Request validation failed. Check message format and content.")
            
        return None

def update_chat(messages, role, content):
    """
    Adds a new message to the conversation history.

    Args:
        messages (list): The current conversation history
        role (str): The role of the message sender ('user' or 'assistant')
        content (str): The message content

    Returns:
        list: Updated messages list
    """
    messages.append({"role": role, "content": content})
    return messages