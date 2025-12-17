from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Contact, Course, Category, Resource, ResourceCategory, Learning
from .utils import fetch_youtube_data  # fonction pour récupérer infos YouTube


# ================= ACCUEIL =================
def acceuil(request):
    slides = [1, 2, 3]  # images carousel
    featured_courses = Course.objects.filter(is_featured=True).order_by('-created_at')[:7]
    context = {"slides": slides, "featured_courses": featured_courses}
    return render(request, 'main/acceuil.html', context)


# ================= DÉTAIL COURS =================
def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, 'main/course_detail.html', {'course': course})


# ================= AJOUTER COURS YOUTUBE =================
def add_course_from_youtube(request):
    if request.method == "POST":
        youtube_url = request.POST.get("youtube_url")
        category_id = request.POST.get("category")
        category = get_object_or_404(Category, id=category_id)

        title, description, image_content = fetch_youtube_data(youtube_url)

        course = Course.objects.create(
            title=title,
            description=description,
            category=category,
            youtube_url=youtube_url,
            is_featured=True
        )

        if image_content:
            course.image.save(f"course_{course.id}.jpg", image_content, save=True)

        return redirect("acceuil")

    categories = Category.objects.all()
    return render(request, "main/add_course.html", {"categories": categories})


# ================= FORMATIONS =================
def formations(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    selected_category = None
    courses = Course.objects.all()

    if category_id:
        try:
            selected_category = Category.objects.get(id=category_id)
            courses = courses.filter(category=selected_category)
        except Category.DoesNotExist:
            selected_category = None

    query = request.GET.get('q')
    if query:
        courses = courses.filter(title__icontains=query)

    context = {
        'courses': courses,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'main/formations.html', context)


# ================= RESSOURCES =================
def ressources(request):
    categories = ResourceCategory.objects.all()
    category_id = request.GET.get('category')
    selected_category = None
    resources = Resource.objects.all()

    if category_id:
        try:
            selected_category = ResourceCategory.objects.get(id=category_id)
            resources = resources.filter(category=selected_category)
        except ResourceCategory.DoesNotExist:
            selected_category = None

    context = {
        'resources': resources,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'main/ressources.html', context)


# ================= CONTACT =================
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        Contact.objects.create(name=name, email=email, message=message)

        return redirect("acceuil")

    return render(request, "main/contact.html")


# ================= MON APPRENTISSAGE =================
@login_required
def apprentissage(request):
    courses = [l.course for l in request.user.learning_courses.all()]
    return render(request, 'main/apprentissage.html', {'courses': courses})


@login_required
def add_to_learning(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Learning.objects.get_or_create(user=request.user, course=course)
    return redirect('apprentissage')


@login_required
def remove_from_learning(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    Learning.objects.filter(user=request.user, course=course).delete()
    return redirect('apprentissage')
