
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import EscortProfile, EscortRequest
from .forms import EscortProfileForm, EscortRequestForm
from django.views.decorators.http import require_POST
@login_required
def register_escort(request):
    if request.method == 'POST':
        form = EscortProfileForm(request.POST, request.FILES)
        if form.is_valid():
            escort_profile = form.save(commit=False)
            escort_profile.user = request.user
            escort_profile.save()
            return redirect('ourescorts')
    else:
        form = EscortProfileForm()
    return render(request, 'home/escorts/addescort.html', {'form': form})

def escort_list(request):
    escorts = EscortProfile.objects.filter(is_active=True)
    return render(request, 'home/escorts/allescorts.html', {'escorts': escorts})


@require_POST
def store_escort_id(request):
    escort_id = request.POST.get('escort_id')
    
    if 'selected_escort_id' in request.session:
        del request.session['selected_escort_id']  # Remove existing session data if any
    
    request.session['selected_escort_id'] = escort_id  # Set the new escort ID in the session
    
    return JsonResponse({'success': True})

    
def escort_details(request):
    escort_id = request.session.get('selected_escort_id')
    
    if escort_id:
        escort = get_object_or_404(EscortProfile, pk=escort_id)
        # Now render the details page with the escort data
        return render(request, 'home/escorts/escort_details.html', {'escort': escort})
    
    # Handle the case where the session data doesn't exist
    return redirect('some_default_page')
    
    
    

def escort_detail(request, pk):
    escort_profile = get_object_or_404(EscortProfile, pk=pk, is_active=True)
    if request.is_ajax():
        html = render_to_string('profiles/escort_detail_content.html', {'escort': escort_profile}, request=request)
        return JsonResponse({'html': html})
    return render(request, 'profiles/escort_detail.html', {'escort': escort_profile})




@login_required
def escort_request_business(request, pk):
    escort_profile = get_object_or_404(EscortProfile, pk=pk)
    if request.method == 'POST':
        form = EscortRequestForm(request.POST)
        if form.is_valid():
            escort_request = form.save(commit=False)
            escort_request.escort = escort_profile
            escort_request.save()
            return redirect('escort_list')
    else:
        form = EscortRequestForm()
    return render(request, 'profiles/escort_request.html', {'form': form, 'escort': escort_profile})
    
    
    
def EscortsRequetsList(request):
    
    return render(request, 'home/escorts/escortrequestlist.html')