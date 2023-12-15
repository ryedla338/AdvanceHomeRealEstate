from django.shortcuts import render, redirect, get_object_or_404
from .forms import PropertyListingForm, TypeSearchForm, NeighborhoodSearchForm, PriceSearchForm
from django.views.generic import ListView
from .models import OmahaEvent, Owner, Search
from .forms import PropertyListingEditForm
from .models import PropertyListing, PropertyType, PropertyPriceRange, PropertyNeighborhood
from django.http import HttpResponse
from io import BytesIO
from django.utils import timezone
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from collections import Counter
from django.conf import settings
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from calendar import month_name
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template

from .models import Search


def index(request):
    property_listings = PropertyListing.objects.all()
    context = {'property_listings': property_listings}
    return render(request, 'index.html', context)


class about(ListView):
    model = Owner
    template_name = 'about.html'
    context_object_name = 'owners'

    def get_queryset(self):
        return Owner.objects.all()


class OmahaEventListView(ListView):
    model = OmahaEvent
    template_name = 'omaha_events.html'
    context_object_name = 'events'

    def get_queryset(self):
        return OmahaEvent.objects.all()



def listing_detail(request, pk):
    property_listing = get_object_or_404(PropertyListing, pk=pk)
    success_popup = request.GET.get('success_popup', False) == 'True'
    if request.method == 'POST' and 'toggle_featured' in request.POST:
        # Toggle the featured status
        property_listing.toggle_featured()

        # Redirect to the same listing detail page after the toggle
        return redirect('listing_detail', pk=pk)

    context = {'property_listing': property_listing}

    return render(request, 'listing_detail.html', context)


def add_listing(request):
    if request.method == 'POST':
        form = PropertyListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save()
            return redirect('listing_detail', pk=listing.pk)
    else:
        form = PropertyListingForm()

    return render(request, 'add_listing.html', {'form': form})


def edit_listing(request, pk):
    listing = get_object_or_404(PropertyListing, pk=pk)

    if request.method == 'POST':
        form = PropertyListingEditForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listing_detail', pk=pk)
    else:
        form = PropertyListingEditForm(instance=listing)

    return render(request, 'edit_listing.html', {'form': form, 'listing': listing})


# views.py

def delete_listing(request, pk):
    listing = get_object_or_404(PropertyListing, pk=pk)
    listing.delete()
    return redirect('search')


from django.shortcuts import render, HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from django.utils import timezone
from collections import Counter
from .models import Search
from calendar import month_name

# ... (previous imports)


def generate_pdf_report(request, year, month):
    try:
        # Retrieve all searches from the database for the selected month and year
        all_searches = Search.objects.filter(created_at__year=year, created_at__month=month)

        # Group searches by month and year
        searches_by_month = {}
        for search in all_searches:
            key = (search.created_at.year, search.created_at.month)
            if key not in searches_by_month:
                searches_by_month[key] = []
            searches_by_month[key].append(search)

        # Create a BytesIO buffer to store the PDF file
        buffer = BytesIO()

        # Create the PDF object using the buffer as its "file"
        p = SimpleDocTemplate(buffer, pagesize=letter)

        # Add content to the PDF
        elements = []
        centered_style = ParagraphStyle(
            'centered',
            parent=getSampleStyleSheet()['Heading1'],
            alignment=1,  # 0=Left, 1=Center, 2=Right
        )

        # Add heading "Advance Home Real Estate"
        elements.append(Paragraph("Advance Home Real Estate", centered_style))

        # Add heading "Monthly search report" with month name and year
        month_heading = month_name[int(month)]  # Convert month number to month name
        heading_text = f"Monthly Search Report - {month_heading} {year}"
        elements.append(Paragraph(heading_text, centered_style))

        if not all_searches:
            elements.append(Paragraph("No searches in this month.", getSampleStyleSheet()['Heading2']))
        else:

            property_type_counts = Counter(search.property_type for search in all_searches if search.property_type)
            property_type_summary = [
                Paragraph(f"{property_type} was searched for {count} times", getSampleStyleSheet()['BodyText'])
                for property_type, count in property_type_counts.items()
            ]
            elements.extend([Spacer(1, 12), Paragraph("Summary for Property Types:",
                                                      getSampleStyleSheet()["Heading2"])] + property_type_summary)


            # Add summary details for property price ranges
            price_range_counts = Counter(search.property_price_range for search in all_searches if search.property_price_range)
            price_range_summary = [
                Paragraph(f"Property in {price_range} price range was searched for {count} times",
                          getSampleStyleSheet()['BodyText'])
                for price_range, count in price_range_counts.items()
            ]
            elements.extend([Spacer(1, 12), Paragraph("Summary for Property Price Ranges:",
                                                      getSampleStyleSheet()["Heading2"])] + price_range_summary)

            # Add summary details for neighborhoods
            neighborhood_counts = Counter(search.neighborhood for search in all_searches if search.neighborhood)
            neighborhood_summary = [
                Paragraph(f"Property in {neighborhood} neighborhood was searched for {count} times",
                          getSampleStyleSheet()['BodyText'])
                for neighborhood, count in neighborhood_counts.items()
            ]
            elements.extend([Spacer(1, 12),
                             Paragraph("Summary for Neighborhoods:", getSampleStyleSheet()["Heading2"])] + neighborhood_summary)

            # Table Header
            table_header = ["Neighborhood", "Property Type", "Property Price Range", "Search Time (UTC)"]

            # Populate the table with data for the selected month and year
            data = [[f"{timezone.datetime(year, month, 1).strftime('%B %Y')}"]]
            data.append(table_header)

            # Populate the table with data for the current month and year
            for search in all_searches:
                data.append([
                    str(search.neighborhood),
                    str(search.property_type),
                    str(search.property_price_range),
                    str(search.created_at.strftime("%Y-%m-%d %H:%M:%S"))
                ])

            # Create a table with the data
            table = Table(data)

            # Style the table
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ])
            table.setStyle(style)

            # Add the table to the elements list
            elements.extend([Spacer(1, 12), Paragraph(f"Monthly Report - {timezone.datetime(year, month, 1).strftime('%B %Y')}",
                                                      getSampleStyleSheet()["Heading2"]), table])

            # Build the PDF
        p.build(elements)

        # Set the buffer's position to the beginning
        buffer.seek(0)

        # Create a response object with the PDF content
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="search_frequency_report_{year}_{month}.pdf"'
        response.write(buffer.read())

        return response
    except Exception as e:
        # Handle exceptions, log the error, and provide a user-friendly message
        return HttpResponse(f"Error generating PDF: {str(e)}", status=500)


def search(request):
    listings = PropertyListing.objects.all()
    type_form = TypeSearchForm()
    neighborhood_form = NeighborhoodSearchForm()
    price_form = PriceSearchForm()

    if request.method == "POST":
        type_form = TypeSearchForm(request.POST)
        neighborhood_form = NeighborhoodSearchForm(request.POST)
        price_form = PriceSearchForm(request.POST)

        if all([type_form.is_valid(), neighborhood_form.is_valid(), price_form.is_valid()]):
            # Save the Search instance
            search_instance = Search(
                neighborhood=neighborhood_form.cleaned_data['neighborhood'],
                property_type=type_form.cleaned_data['property_type'],
                property_price_range=price_form.cleaned_data['property_price_range']
            )
            search_instance.save()

            # Filter the listings based on the search criteria
            if search_instance.neighborhood:
                listings = listings.filter(neighborhood=search_instance.neighborhood)
            if search_instance.property_type:
                listings = listings.filter(property_type=search_instance.property_type)
            if search_instance.property_price_range:
                listings = listings.filter(property_price_range=search_instance.property_price_range)

    return render(request, 'search.html', {
        'listing': listings,
        'type_form': type_form,
        'neighborhood_form': neighborhood_form,
        'price_form': price_form
    })



from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def send_email(request, pk=None):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        message = request.POST.get('message')

        if pk:
            
            property = get_object_or_404(PropertyListing, pk=pk)
            owner = get_object_or_404(Owner, name=property.owner)
            property_details = f"Property Title: {property.name}\nProperty Address: {property.street},  {property.city},  {property.state},  {property.zipcode}.\n"
            mail_subject = 'New Contact Request'
            mail_message = f"Hello {owner.name}, a client wants to know about a property and here are the details:\n\n\nName: {name}\nPhone: {phone}\nEmail: {email}\nAddress: {address}\nMessage: {message}\nProperty Details:\n{property_details}"
            to_email = [owner.email_id]
        else:
            owner = get_object_or_404(Owner, name="Madison Vance")
            mail_subject = 'New Contact Request'
            mail_message = f"Hello Madison,\n\n Here are the details of the person who wants to contact you: \nName: {name}\nPhone: {phone}\nEmail: {email}\nAddress: {address}\nMessage: {message}"
            to_email = [owner.email_id]

        from_email = settings.EMAIL_HOST_USER


        send_mail(mail_subject, mail_message, from_email, to_email, fail_silently=False)

        return redirect('listing_detail', pk=pk)
    else:
        return JsonResponse({'error': 'Invalid request method.'})


def generate_report_prompt(request):
    # Assuming you have a range of years (modify this based on your needs)
    years = range(2022, 2030)

    months_years = [(str(year), [(str(i), month_name[i]) for i in range(1, 13)]) for year in years]
    return render(request, 'generate_report_prompt.html', {'months_years': months_years})


def generate_pdf_report_prompt(request):
    if request.method == 'POST':
        selected_month = request.POST.get('month')
        selected_year = request.POST.get('year')

        # Redirect to the generate_pdf_report view with the selected month and year
        return redirect('generate_pdf_report', month=selected_month, year=selected_year)

    # Render the template without report details
    return render(request, 'generate_report_prompt.html', {'report': None})