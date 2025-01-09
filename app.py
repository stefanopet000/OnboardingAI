from flask import Flask, request, render_template
from main import FAQAssistant

app=Flask(__name__)
faq_assistant = FAQAssistant() #load FAQs when app starts

@app.route('/', method = ["GET", "POST"])
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
__name__ == "__main__":
app.run(debug=True)

