from flask import Flask,request , render_template ,jsonify
import openai
import os
from dotenv import load_dotenv
import wikipedia
load_dotenv()
openai.api_key=os.getenv("open_ai_apikey")

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
    try:
        responce=openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{'role':'user','content': question}]
        )
        reply=responce["choices"][0]["message"]["content"]
        print("answer",reply)
        return jsonify({"answer": reply})
    
    except Exception as e:
        
        try:
           answer = wikipedia.summary(question, sentences=2)
           return jsonify({"answer": answer})
        except Exception as wiki_error:
            return jsonify({"answer": "Sorry, I could not find an answer."})


       
    
if __name__=="__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)