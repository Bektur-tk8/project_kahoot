from django.urls import path, re_path
from quiz.views import  QuizListAPI, QuizDetailAPI, SaveUsersAnswer,StartQuiz


urlpatterns = [
	path("quizzes/", QuizListAPI.as_view()),
	path("start_quiz/<int:quiz_id>/", StartQuiz.as_view()),
    path("save_answer/", SaveUsersAnswer.as_view()),
	path("quiz_questions/<int:pk>/", QuizDetailAPI.as_view() ),
    
]   