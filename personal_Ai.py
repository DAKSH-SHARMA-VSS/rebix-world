from flask import Flask,request , render_template ,jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY=os.getenv("API")
genai.configure(api_key=API_KEY)
app=Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["GET","POST"])
def ask_my_AI():
    data=request.get_json(force=True)
    print("question:",data)
    question=data.get("question","")

    if not question.strip():
        return jsonify("first enter something...")
    if "who makes you" in question or "tumhe kisne bnaya" in question:
        return jsonify({"answer":"mujhe DAKSH SHARMA ne banaya hai mai unka pehla AI hu"})
    if "who made you" in question:
        return jsonify({"answer":"Mr. DAKSH SHARMA created me ,i am the first AI made by DAKSH.."})
    try:
        model=genai.GenerativeModel("gemini-2.0-flash")
        chat=model.start_chat()
        response=chat.send_message(question)
        return jsonify({"answer": response.text})
    
    except Exception as e:
        return jsonify({'answer':"sorry i could not find answer"})
        
  
    
if __name__=="__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)