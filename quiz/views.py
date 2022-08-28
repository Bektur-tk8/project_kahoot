from datetime import datetime
from os import stat
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.authentication import  SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from quiz.models import Answer, Question, Quiz, QuizTaker, UsersAnswer
from accounts.models import User
from quiz.utils import check_test_over, calculate_score, calculate_rating
from quiz.serializers import  (
    QuizQuestionsDetailSerializer, 
    QuizListSerializer, 
    UsersAnswerSerializer,
    QuizTakerSerializer
    )


class QuizListAPI(generics.ListAPIView):
    serializer_class = QuizListSerializer
    permission_classes = [
       permissions.IsAuthenticated
    ]

    def get_queryset(self, *args, **kwargs):
        queryset = Quiz.objects.filter(is_active=True)
        # query = self.request.GET.get("q")
        return queryset
		# if query:
		# 	queryset = queryset.filter(
		# 		Q(name__icontains=query) |
		# 		Q(description__icontains=query)
		# 	).distinct()

		# return queryset


class QuizDetailAPI(generics.RetrieveAPIView):
    serializer_class = QuizQuestionsDetailSerializer
    # authentication_classes = (SessionAuthentication,)
    permission_classes = [
		permissions.IsAuthenticated
	]
    queryset = Quiz.objects.all()

class StartQuiz(APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    def get(self, request,quiz_id ,*args, **kwargs):
        if not QuizTaker.objects.filter(quiz__id=quiz_id, user=request.user).exists():
            quiz = get_object_or_404(Quiz, id=quiz_id)
            user = request.user 
            quiz_user = QuizTaker.objects.create(
                quiz =quiz,
                user=user
            )      
            serializer=QuizTakerSerializer(instance=quiz_user)
            return Response(data={"message":"Test started", "quiz_taker":serializer.data}, status=status.HTTP_200_OK)
        return Response({"message":"You already passed test!"}, status=status.HTTP_403_FORBIDDEN)


class SaveUsersAnswer(APIView):
    serializer_class = UsersAnswerSerializer
    permission_classes = [
		permissions.IsAuthenticated
    ]
    @swagger_auto_schema(request_body=UsersAnswerSerializer)
    def post(self, request, *args, **kwargs):
        quiztaker_id = request.data['quiz_taker']
        question_id = request.data['question']
        answer_id = request.data['answer']
        answer_time = request.data['answer_time']
        quiztaker = get_object_or_404(QuizTaker, id=quiztaker_id)
        question = get_object_or_404(Question, id=question_id)
        answer = get_object_or_404(Answer, id=answer_id)

        if quiztaker.completed:
            return Response({
				"message": "This quiz is already complete. you can't answer any more questions"},
              status=status.HTTP_412_PRECONDITION_FAILED
           )
        
        obj = UsersAnswer.objects.get_or_create( quiz_taker=quiztaker, question=question, answer=answer)
        if  answer.is_correct:
            score = calculate_score(question_id, answer_time)
            quiztaker.score += score
            quiztaker.save()
        
        if check_test_over(quiztaker):
            quiztaker.completed = True
            quiztaker.date_finished = datetime.now()
            quiztaker.save()
            user = quiztaker.user
            user.score += quiztaker.score
            user.save()
            calculate_rating(request)
            return Response(
                {
                    "message":"You are finished test!"
                },
                status = status.HTTP_200_OK
            )
        return Response({"message":"Answer Received!"}, status=status.HTTP_200_OK)