from django.contrib import admin
from fugato.models import Question, Answer
from fugato.models import QuestionVote, AnswerVote

# Register your models here.
admin.site.register(Question)
admin.site.register(QuestionVote)
admin.site.register(Answer)
admin.site.register(AnswerVote)
