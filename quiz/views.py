from datetime import datetime
from os import stat
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from quiz.models import Answer, Question, Quiz, TestParticipant, UsersAnswer
from accounts.models import User
from quiz.utils import check_test_over, calculate_score
from quiz.serializers import  (
    QuizQuestionsDetailSerializer, 
    QuizListSerializer, 
    UsersAnswerSerializer,
    TestParticipantSerializer
    )


class QuizListAPI(generics.ListAPIView):
    serializer_class = QuizListSerializer
    permission_classes = [
    #    permissions.IsAuthenticated
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
    # permission_classes = [
	# 	# permissions.IsAuthenticated
	# ]
    queryset = Quiz.objects.all()

class StartQuiz(APIView):
    def get(self, request,quiz_id ,*args, **kwargs):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        user = get_object_or_404(User, email="tbektur7@gmail.com")
        quiz_user = TestParticipant.objects.create(
            quiz =quiz,
            user=user
        )      
        serializer=TestParticipantSerializer(instance=quiz_user)
        return Response(data={"message":"Test started", "test_participant":serializer.data}, status=status.HTTP_200_OK)


class SaveUsersAnswer(APIView):
    serializer_class = UsersAnswerSerializer
    permission_classes = [
		# permissions.IsAuthenticated
    ]



    def post(self, request, *args, **kwargs):
        testparticipant_id = request.data['testparticipant']
        question_id = request.data['question']
        answer_id = request.data['answer']
        answer_time = request.data['answer_time']
        testparticipant = get_object_or_404(TestParticipant, id=testparticipant_id)
        question = get_object_or_404(Question, id=question_id)
        answer = get_object_or_404(Answer, id=answer_id)

        if testparticipant.completed:
            return Response({
				"message": "This quiz is already complete. you can't answer any more questions"},
              status=status.HTTP_412_PRECONDITION_FAILED
           )
        
        obj = UsersAnswer.objects.get_or_create(test_participant=testparticipant, question=question, answer=answer)
        score = calculate_score(question_id, answer_time)
        testparticipant.score += score
        
        if check_test_over(testparticipant):
            testparticipant.completed = True
            testparticipant.date_finished = datetime.now()
            testparticipant.save()
            return Response(
                {
                    "message":"You have finished the test!"
                },
                status = status.HTTP_200_OK
            )
        testparticipant.save()
        return Response({"message":"Answer Received!"}, status=status.HTTP_200_OK)





# class SubmitQuizAPI(generics.GenericAPIView):
# 	serializer_class = QuizResultSerializer
# 	permission_classes = [
# 		permissions.IsAuthenticated
# 	]

# 	def post(self, request, *args, **kwargs):
# 		quiztaker_id = request.data['quiztaker']
# 		question_id = request.data['question']
# 		answer_id = request.data['answer']

# 		quiztaker = get_object_or_404(QuizTaker, id=quiztaker_id)
# 		question = get_object_or_404(Question, id=question_id)

# 		quiz = Quiz.objects.get(slug=self.kwargs['slug'])

# 		if quiztaker.completed:
# 			return Response({
# 				"message": "This quiz is already complete. You can't submit again"},
# 				status=status.HTTP_412_PRECONDITION_FAILED
# 			)

# 		if answer_id is not None:
# 			answer = get_object_or_404(Answer, id=answer_id)
# 			obj = get_object_or_404(UsersAnswer, quiz_taker=quiztaker, question=question)
# 			obj.answer = answer
# 			obj.save()

# 		quiztaker.completed = True
# 		correct_answers = 0

# 		for users_answer in UsersAnswer.objects.filter(quiz_taker=quiztaker):
# 			answer = Answer.objects.get(question=users_answer.question, is_correct=True)
# 			print(answer)
# 			print(users_answer.answer)
# 			if users_answer.answer == answer:
# 				correct_answers += 1

# 		quiztaker.score = int(correct_answers / quiztaker.quiz.question_set.count() * 100)
# 		print(quiztaker.score)
# 		quiztaker.save()

# 		return Response(self.get_serializer(quiz).data)


