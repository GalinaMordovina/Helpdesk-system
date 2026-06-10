from django.contrib import admin

from comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "ticket",
        "author",
        "created_at",
    )
    list_filter = (
        "created_at",
    )
    search_fields = (
        "text",
        "author__username",
        "ticket__title",
    )
