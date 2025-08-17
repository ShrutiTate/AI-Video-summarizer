import google.generativeai as genai

genai.configure(api_key="AIzaSyBaSmyIZrGjFOzzouktd0ZDzbMNDik7L_o")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Hello Gemini!")
print(response.text)
