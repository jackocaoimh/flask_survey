from flask import Flask, render_template, request, session, redirect
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"
app = Flask(__name__)
app.secret_key = 'my_secret'

@app.route('/')
def show_welcome():
    return render_template('survey_start.html', survey=survey)

@app.route('/begin', methods = ["POST"])
def start_survey():

    session[RESPONSES_KEY] = []
    return redirect('/questions/0')

@app.route('/answer', methods = ['POST'])
def handle_question():
    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/questions/<int:qid>')
def show_question(qid):
    responses = session.get(RESPONSES_KEY)

    if len(responses) == len(survey.questions):
        return redirect('/complete')
    
    question = survey.questions[qid]
    return render_template('questions.html', question= question, question_num=qid )



@app.route('/complete')
def show_thanks():
    return render_template('completion.html')