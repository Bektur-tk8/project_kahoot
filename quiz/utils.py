from quiz.models import Quiz, QuizTaker, Question
from accounts.models import User
def check_test_over(quiztaker: QuizTaker):
    if quiztaker.quiz.questions.count() == quiztaker.user_answers.count():
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


def calculate_rating(request):
    users = User.objects.all().order_by("-score")
    r=1
    for user in users:
        user.rating_place = r
        r += 1 
        user.save()
    group_users = users.filter(group=request.user.group).order_by("-score")
    r=1
    for user in group_users:
        user.group_rating = r
        r += 1 
        user.save()