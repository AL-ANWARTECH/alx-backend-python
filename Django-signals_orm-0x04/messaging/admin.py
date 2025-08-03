# messaging/admin.py
from django.contrib import admin
from .models import Message, Notification, MessageHistory


class MessageHistoryInline(admin.TabularInline):
    model = MessageHistory
    extra = 0
    readonly_fields = ('old_content', 'edited_at', 'edited_by')  
    can_delete = False


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content_preview', 'timestamp', 'edited')
    list_filter = ('edited', 'timestamp', 'sender', 'receiver')
    search_fields = ('content', 'sender__username', 'receiver__username')
    inlines = [MessageHistoryInline]  # Shows history in message edit page

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Content"


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('message', 'edited_by', 'edited_at')    
    list_filter = ('edited_at', 'edited_by')                    


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message_preview', 'is_read', 'created_at')

    def message_preview(self, obj):
        return obj.message.content[:50] + "..."
    message_preview.short_description = "Message"