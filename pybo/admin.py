from django.contrib import admin
from .models import Category, Question, Answer, Comment  # ← 추가: Category, Answer, Comment

# Category 관리
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug","order")
    list_editable = ("order",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}  # name 입력 시 slug 자동 채움

# Question 관리 (기존 기능 + 카테고리 컬럼/필터 추가)
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ("subject",)                 # 기존 유지
    list_display = ("id", "subject", "author", "category", "create_date", "modify_date")
    list_filter = ("category", "create_date")   # 카테고리/날짜 필터

# (선택) Answer/Comment도 관리자에서 보이게
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "question", "create_date", "modify_date")
    search_fields = ("content",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "question", "answer", "create_date", "modify_date")
    search_fields = ("content",)
