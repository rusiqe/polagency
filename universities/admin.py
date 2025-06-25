from django.contrib import admin
from django.utils.text import slugify
from .models import University, StudyProgram

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'university_type', 'english_programs', 'created_at']
    list_filter = ['university_type', 'city', 'voivodeship', 'english_programs', 'international_students']
    search_fields = ['name', 'name_polish', 'city']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'name_polish', 'slug', 'university_type', 'established_year')
        }),
        ('Location', {
            'fields': ('city', 'voivodeship', 'address')
        }),
        ('Contact Information', {
            'fields': ('website', 'email', 'phone')
        }),
        ('Details', {
            'fields': ('description', 'student_count', 'international_students', 'english_programs')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.name)
        super().save_model(request, obj, form, change)

@admin.register(StudyProgram)
class StudyProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'university', 'degree_level', 'study_area', 'language', 'tuition_fee_eur']
    list_filter = ['degree_level', 'study_area', 'language', 'university__university_type']
    search_fields = ['name', 'university__name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('university', 'name', 'degree_level', 'study_area', 'language')
        }),
        ('Program Details', {
            'fields': ('duration_years', 'ects_credits', 'tuition_fee_eur')
        }),
        ('Descriptions', {
            'fields': ('description', 'admission_requirements')
        }),
    )

