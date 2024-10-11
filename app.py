from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
from openai import OpenAI
import markdown

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
base_url = "https://api.aimlapi.com/v1"
api = OpenAI(api_key=api_key, base_url=base_url)

app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('b+h.html')

# # Optional route to still access index.html
# @app.route('/index')
# def index():
#     return render_template('index.html')

@app.route('/')
def berry_ai():
    return render_template('about.html')

@app.route('/berry')
def home():
    return render_template('index.html')

@app.route('/generate_response', methods=['POST'])
def generate_response():
    data = request.json
    user_choice = data.get('choice')
    user_query = data.get('query')

    system_prompt = generate_system_prompt(user_choice)


    if system_prompt:
        # #for html response
        # response = get_openai_response(system_prompt,user_query)
        # return jsonify({'response': response})
        # for markeddown response
        response = get_openai_response(system_prompt, user_query)
        html_response = markdown.markdown(response)  # Convert Markdown to HTML
        return jsonify({'response': html_response})  # Return HTML response
    else:
        return jsonify({'response': 'Invalid choice or query.'})

# def generate_system_prompt(choice):
#     if choice == 'coding':
#         return f"""Act as a coding expert in all programming languages. Always convert your response text to HTML. Your task is to identify what user is asking for and then answer using only one, most relvant apporach from below:
#                     Approach 1: Only if user asks to explain then explain the block of code that user provides, in simple words, avoid jargons until absolutely necessaryy
#                     Approach 2: If user query is asking to generate or write a code then provide just a code snippet and avoid explanations.
#                     Approach 3: If user asks to debug the code find source of error and correct users code
#                     Approach 4: If user asks to optimize a coding problem then provide an optimized code snippet with it's time complexity explanation
#                     Approach 5: If the user's query is not about code or programming in general, then don't answer then declie to answer and tell that you are only a programmig assitant and the query asked is out of your scope."""
#     elif choice == 'research':
#         return f"""- You are an expert researcher helping users with their research queries.
#                     - Your tone is highly professional
#                     - Your replies are relevant and concise.
#                     - Always convert your response text to HTML.
#                     - You will not answer any query out of research help domain and politely decline to answer out of context queries"""""
#     return None

def generate_system_prompt(choice):
    if choice == 'coding':
        return f"You are a coding assistant. The user needs help with a codeing query. Please provide code examples and explanations."
    elif choice == 'research':
        return f"You are a research assistant. The user needs help with a research query. Provide detailed information and resources. Always add references to your source of knowledge."
    return None


def get_openai_response(system_prompt, user_query):
    completion = api.chat.completions.create(
        model="o1-mini",
        # model = 'o1-preview',
        messages=[
            {"role": "user", "content": system_prompt}, #currently system role are not supported
            {"role": "user", "content": user_query}
        ],
        #temperature=0.7,
        #max_tokens=256,
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content
    

if __name__ == '__main__':
    app.run(debug=True)
