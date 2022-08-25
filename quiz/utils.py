from quiz.models import Quiz, TestParticipant, Question

def check_test_over(participant: TestParticipant):
    if participant.quiz.questions.count() == participant.user_answers.count():
        return True
    else:
        return False


def calculate_score(question_id, answer_time):
    question = Question.objects.get(id=question_id)
    answer_time = int(answer_time)
    if answer_time == 1:
        score = (question.score - (question.score/question.timer*answer_time)+(question.score/question.timer))
    elif answer_time > 1:
        score = (question.score - (question.score/question.timer*answer_time))
    else:
        score = 0
    return score