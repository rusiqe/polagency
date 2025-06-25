from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import University, StudyProgram

def university_list(request):
    """Display list of universities with search and filter functionality"""
    universities = University.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        universities = universities.filter(
            Q(name__icontains=search_query) |
            Q(name_polish__icontains=search_query) |
            Q(city__icontains=search_query)
        )
    
    # Filter by type
    university_type = request.GET.get('type', '')
    if university_type:
        universities = universities.filter(university_type=university_type)
    
    # Filter by city
    city = request.GET.get('city', '')
    if city:
        universities = universities.filter(city=city)
    
    # Filter by English programs
    english_programs = request.GET.get('english_programs', '')
    if english_programs == 'true':
        universities = universities.filter(english_programs=True)
    
    # Get unique cities for filter dropdown
    cities = University.objects.values_list('city', flat=True).distinct().order_by('city')
    
    # Pagination
    paginator = Paginator(universities, 12)  # Show 12 universities per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'selected_type': university_type,
        'selected_city': city,
        'english_programs': english_programs,
        'cities': cities,
        'university_types': University.UNIVERSITY_TYPES,
    }
    
    return render(request, 'universities/university_list.html', context)

def university_detail(request, slug):
    """Display detailed information about a specific university"""
    university = get_object_or_404(University, slug=slug)
    programs = university.programs.all().order_by('degree_level', 'name')
    
    # Group programs by degree level
    programs_by_level = {}
    for program in programs:
        level = program.get_degree_level_display()
        if level not in programs_by_level:
            programs_by_level[level] = []
        programs_by_level[level].append(program)
    
    context = {
        'university': university,
        'programs_by_level': programs_by_level,
    }
    
    return render(request, 'universities/university_detail.html', context)

def program_search(request):
    """Search for study programs with advanced filters"""
    programs = StudyProgram.objects.select_related('university').all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        programs = programs.filter(
            Q(name__icontains=search_query) |
            Q(university__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by degree level
    degree_level = request.GET.get('degree_level', '')
    if degree_level:
        programs = programs.filter(degree_level=degree_level)
    
    # Filter by study area
    study_area = request.GET.get('study_area', '')
    if study_area:
        programs = programs.filter(study_area=study_area)
    
    # Filter by language
    language = request.GET.get('language', '')
    if language:
        programs = programs.filter(language=language)
    
    # Filter by university type
    university_type = request.GET.get('university_type', '')
    if university_type:
        programs = programs.filter(university__university_type=university_type)
    
    # Pagination
    paginator = Paginator(programs, 15)  # Show 15 programs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'selected_degree_level': degree_level,
        'selected_study_area': study_area,
        'selected_language': language,
        'selected_university_type': university_type,
        'degree_levels': StudyProgram.DEGREE_LEVELS,
        'study_areas': StudyProgram.STUDY_AREAS,
        'languages': StudyProgram.LANGUAGES,
        'university_types': University.UNIVERSITY_TYPES,
    }
    
    return render(request, 'universities/program_search.html', context)

