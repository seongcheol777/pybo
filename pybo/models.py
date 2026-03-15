from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='questions',
    )
    view_count = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    accepted_answer = models.OneToOneField(
        'Answer',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='accepted_for',
    )
    attachment = models.FileField(upload_to='question_attachments/', null=True, blank=True)

    def __str__(self):
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')
    attachment = models.FileField(upload_to='answer_attachments/', null=True, blank=True)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)


class Notification(models.Model):
    TYPE_CHOICES = [
        ('answer', '답변'),
        ('comment', '댓글'),
        ('vote', '추천'),
        ('accept', '채택'),
    ]
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    notification_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-create_date']

    def get_message(self):
        type_map = {
            'answer': f'{self.sender.username}님이 회원님의 질문에 답변을 달았습니다.',
            'comment': f'{self.sender.username}님이 댓글을 달았습니다.',
            'vote': f'{self.sender.username}님이 추천했습니다.',
            'accept': f'회원님의 답변이 채택되었습니다.',
        }
        return type_map.get(self.notification_type, '새 알림이 있습니다.')

    def get_url(self):
        if self.question:
            url = f'/pybo/{self.question.id}/'
            if self.answer:
                url += f'#answer_{self.answer.id}'
            return url
        return '/'


class Banner(models.Model):
    slot = models.PositiveSmallIntegerField(unique=True, help_text='1~20 (가로4×세로5)')
    image_url = models.URLField(blank=True, default='', help_text='이미지 URL (GIF/PNG/JPG, 400×50px 권장)')
    link_url = models.URLField(blank=True, help_text='클릭 시 이동할 URL (선택)')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['slot']

    def __str__(self):
        return f'배너 슬롯 {self.slot}'
