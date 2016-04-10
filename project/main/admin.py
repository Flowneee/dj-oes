from django.contrib import admin

from .models import Subject, Question, Answer

class AnswerInLine(admin.TabularInline):
    model = Answer
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    fields = ['text','subject',]
    inlines = [AnswerInLine]

admin.site.register(Subject)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer)