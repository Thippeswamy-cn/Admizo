from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.text import slugify

from .forms import ContactInquiryForm
from .models import Business, CompanyMetric, Insight, Project


FALLBACK_BUSINESSES = [
    {"title": "Technology", "summary": "Software, digital platforms, applications, automation and emerging technologies.", "icon": "grid", "accent": "blue"},
    {"title": "Real Estate", "summary": "Development, property management, investment and connected services.", "icon": "building", "accent": "green"},
    {"title": "Promotions", "summary": "Brand promotions, marketing solutions and strategic promotional services.", "icon": "signal", "accent": "orange"},
    {"title": "Business Development", "summary": "Business strategy, market expansion, partnerships and growth opportunities.", "icon": "chart", "accent": "green"},
    {"title": "Other Ventures", "summary": "Emerging initiatives and carefully selected business opportunities.", "icon": "compass", "accent": "blue"},
]

for business in FALLBACK_BUSINESSES:
    business["slug"] = slugify(business["title"])


def business_list(request):
    return render(request, "businesses/index.html", {
        "businesses": list(Business.objects.filter(is_published=True)) or FALLBACK_BUSINESSES,
    })


def business_detail(request, slug):
    business = Business.objects.filter(slug=slug, is_published=True).first()
    if business is None:
        if Business.objects.filter(is_published=True).exists() or Business.objects.filter(slug=slug).exists():
            raise Http404("Business not found")
        business = next((item for item in FALLBACK_BUSINESSES if item["slug"] == slug), None)
    if business is None:
        raise Http404("Business not found")
    known_slugs = {item["slug"] for item in FALLBACK_BUSINESSES}
    template = f"businesses/{slug}/index.html" if slug in known_slugs else "businesses/detail.html"
    icon = business["icon"] if isinstance(business, dict) else business.icon
    image = {
        "building": "work-real-estate.jpg", "signal": "work-promotions.jpg",
        "chart": "work-business.jpg", "compass": "work-ventures.jpg",
    }.get(icon, "work-technology.jpg")
    return render(request, template, {
        "business": business, "business_image": f"images/{image}",
        "enquiry_service": slug if slug in known_slugs and slug != "other-ventures" else "other",
    })


def home(request):
    if request.method == "POST":
        form = ContactInquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you. Your message is with our team.")
            return redirect(f"{reverse('home')}?sent=1#contact")
    else:
        service = request.GET.get("service", "")
        valid_services = {value for value, label in ContactInquiryForm.base_fields["service"].choices}
        form = ContactInquiryForm(initial={"service": service} if service in valid_services else None)

    businesses = list(Business.objects.filter(is_published=True))
    metrics = CompanyMetric.objects.filter(is_published=True)
    projects = Project.objects.filter(is_published=True)
    insights = Insight.objects.filter(is_published=True)[:3]

    return render(
        request,
        "home.html",
        {
            "businesses": businesses or FALLBACK_BUSINESSES,
            "metrics": metrics,
            "projects": projects,
            "insights": insights,
            "form": form,
        },
    )
