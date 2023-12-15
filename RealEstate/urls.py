from . import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from .views import OmahaEventListView, add_listing, about, listing_detail, edit_listing, delete_listing, generate_pdf_report, generate_pdf_report_prompt, search, send_email

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', about.as_view(), name='about'),
    path('explore/', OmahaEventListView.as_view(), name='omaha_event_list'),
    path('listing/search/', search, name="search"),
    path('listings/add_listing/', add_listing, name='add_listing'),
    path('listing/<int:pk>/edit/', edit_listing, name='edit_listing'),
    path('listing/<int:pk>/', listing_detail, name='listing_detail'),
    path('listing/<int:pk>/delete/', delete_listing, name='delete_listing'),
    path('generate-pdf-report/', generate_pdf_report, name='generate_pdf_report'),
    path('listing/<int:pk>/send_email/', views.send_email, name='send_email'),
    path('about/send_email_no_pk/', views.send_email, name='send_email_no_pk'),
    path('generate-pdf-report/', generate_pdf_report, name='generate_pdf_report'),
    path('generate-pdf-report/<int:year>/<int:month>/', generate_pdf_report, name='generate_pdf_report'),
    path('generate-pdf-report-prompt/', generate_pdf_report_prompt, name='generate_pdf_report_prompt'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
