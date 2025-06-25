from django.contrib import admin
from .models import ChatSession, ChatMessage, FAQ, ContactRequest

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user_ip', 'started_at', 'is_active', 'connected_to_admin', 'admin_user']
    list_filter = ['is_active', 'connected_to_admin', 'started_at']
    search_fields = ['session_id', 'user_ip']
    readonly_fields = ['session_id', 'user_ip', 'user_agent', 'started_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('admin_user')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'message_type', 'content_preview', 'timestamp', 'sender_name']
    list_filter = ['message_type', 'timestamp']
    search_fields = ['content', 'session__session_id']
    readonly_fields = ['session', 'message_type', 'content', 'timestamp', 'sender_name']
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('session')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'is_active', 'order', 'updated_at']
    list_filter = ['category', 'is_active']
    search_fields = ['question', 'answer', 'keywords']
    list_editable = ['is_active', 'order']
    
    fieldsets = (
        ('Question & Answer', {
            'fields': ('category', 'question', 'answer')
        }),
        ('Settings', {
            'fields': ('keywords', 'is_active', 'order')
        }),
    )

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'email', 'priority', 'status', 'assigned_to', 'created_at']
    list_filter = ['priority', 'status', 'created_at', 'assigned_to']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['priority', 'status', 'assigned_to']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Request Details', {
            'fields': ('subject', 'message', 'chat_session')
        }),
        ('Management', {
            'fields': ('priority', 'status', 'assigned_to')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('assigned_to', 'chat_session')

