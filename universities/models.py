from django.db import models

class University(models.Model):
    UNIVERSITY_TYPES = [
        ('public', 'Public University'),
        ('private', 'Private University'),
        ('church', 'Church-affiliated University'),
    ]
    
    name = models.CharField(max_length=255)
    name_polish = models.CharField(max_length=255, blank=True)
    university_type = models.CharField(max_length=10, choices=UNIVERSITY_TYPES)
    city = models.CharField(max_length=100)
    voivodeship = models.CharField(max_length=100)  # Polish administrative division
    website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    description = models.TextField(blank=True)
    established_year = models.IntegerField(null=True, blank=True)
    student_count = models.IntegerField(null=True, blank=True)
    international_students = models.BooleanField(default=True)
    english_programs = models.BooleanField(default=False)
    
    # SEO and search fields
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Universities"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class StudyProgram(models.Model):
    DEGREE_LEVELS = [
        ('bachelor', 'Bachelor Programme'),
        ('master', 'Master\'s Programme'),
        ('long_master', 'Long cycle Master\'s Programme'),
        ('doctoral', 'Doctoral studies'),
        ('non_degree', 'Non-degree programme'),
    ]
    
    STUDY_AREAS = [
        ('agricultural', 'Agricultural, forestry and veterinary sciences'),
        ('arts', 'Arts'),
        ('biological', 'Biological sciences'),
        ('humanities', 'Humanities'),
        ('medical', 'Medical, health and sport sciences'),
        ('science', 'Science'),
        ('social', 'Social sciences'),
        ('technological', 'Technological sciences'),
    ]
    
    LANGUAGES = [
        ('PL', 'Polish'),
        ('EN', 'English'),
        ('DE', 'German'),
        ('RU', 'Russian'),
    ]
    
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='programs')
    name = models.CharField(max_length=255)
    degree_level = models.CharField(max_length=15, choices=DEGREE_LEVELS)
    study_area = models.CharField(max_length=15, choices=STUDY_AREAS)
    language = models.CharField(max_length=2, choices=LANGUAGES, default='PL')
    duration_years = models.IntegerField(null=True, blank=True)
    ects_credits = models.IntegerField(null=True, blank=True)
    tuition_fee_eur = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    admission_requirements = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['university', 'name', 'degree_level']
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_degree_level_display()}) - {self.university.name}"

