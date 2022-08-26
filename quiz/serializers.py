from quiz.models import Quiz, QuizTaker, Question, Answer, UsersAnswer
from rest_framework import serializers


class QuizListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz    
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['questions_count'] = instance.questions.count()  
        representation['test_completed_users_count'] = instance.completed_tests.count()
        return representation


class AnswerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Answer
		fields = ["id", "question", "label", 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['answers'] = AnswerSerializer(instance.answers.all(), many=True, context=self.context).data
        return representation


class UsersAnswerSerializer(serializers.ModelSerializer):
	class Meta:
		model = UsersAnswer
		fields = "__all__"



class QuizQuestionsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['questions'] =QuestionSerializer(instance.questions.all(), many=True, context=self.context).data
        return representation


class QuizTakerSerializer(serializers.ModelSerializer):
    class Meta:
        model= QuizTaker
        fields = "__all__"