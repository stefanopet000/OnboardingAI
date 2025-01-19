from flask import Flask, request, render_template, jsonify
from main import FAQAssistant

app = Flask(__name__)

# Initialize the FAQAssistant with the data file
faq_assistant = FAQAssistant(file_path="data/faqs.json")

@app.route("/")
def home():
    answer= None
    if request.method == "POST":
        question = request.form.get("question")
    return render_template("index.html")

@app.route("/get-answer", methods=["POST"])
def get_answer():
    data = request.get_json()
    question = data.get("question", "")
    answer = faq_assistant.get_answer(question) if question else "No question provided."
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)








"""

from flask import Flask, request, render_template
from main import FAQAssistant

app=Flask(__name__)
faq_assistant = FAQAssistant(file_path="data/faqs.json") #load FAQs when app starts

@app.route('/', methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        user_question = request.form.get("question", "").strip()
        if user_question:
            # Use FAQs to find the best match
            best_match, highest_score = faq_assistant.find_best_match(user_question)


            if highest_score > 80:
                return render_template("index.html", answer=best_match["answer"], question=user_question)
            else:
                return render_template("index.html", answer="Sorry, I don't understand the question. Can you try again?", question=user_question,)
        else:
            return render_template("index.html", answer="Please enter a question")
        
    return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)


"""