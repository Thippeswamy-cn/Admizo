from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ContactInquiryForm
from .models import Business, CompanyMetric, Insight, Project


FALLBACK_BUSINESSES = [
    {"title": "Technology", "summary": "Software, digital platforms, applications, automation and emerging technologies.", "icon": "grid", "accent": "blue"},
    {"title": "Real Estate", "summary": "Development, property management, investment and connected services.", "icon": "building", "accent": "green"},
    {"title": "Promotions", "summary": "Brand promotions, marketing solutions and strategic promotional services.", "icon": "signal", "accent": "orange"},
    {"title": "Business Development", "summary": "Business strategy, market expansion, partnerships and growth opportunities.", "icon": "chart", "accent": "green"},
    {"title": "Other Ventures", "summary": "Emerging initiatives and carefully selected business opportunities.", "icon": "compass", "accent": "blue"},
]


def home(request):
    if request.method == "POST":
        form = ContactInquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you. Your message is with our team.")
            return redirect(f"{reverse('home')}?sent=1#contact")
    else:
        form = ContactInquiryForm()

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
