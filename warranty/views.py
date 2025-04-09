from django.shortcuts import render, get_object_or_404
from .models import Claim
from django.utils.timezone import now
from django.http import HttpResponseRedirect
from django.urls import reverse


def claims_landing(request):
    """ Display claims pending a decision and show a policy search form """
    pending_claims = Claim.objects.filter(status='Pending')
    return render(request, 'warranty/claims_landing.html', {
        'pending_claims': pending_claims
    })


def claims_list(request):
    """ Display all valid warranty claims in a list/table """
    # Filter to only include claims that have essential fields filled in
    claims = Claim.objects.exclude(claim_number__isnull=True).exclude(claim_number__exact='').order_by('-date_issued')
    return render(request, 'warranty/claims_list.html', {
        'claims': claims
    })


def claim_detail(request, claim_id):
    """ View the details of a specific claim """
    claim = get_object_or_404(Claim, pk=claim_id)
    return render(request, 'warranty/claims_detail.html', {
        'claim': claim
    })



def policies_search(request):
    results = []
    customer_name = request.GET.get('customer_name', '').strip()
    claim_number = request.GET.get('claim_number', '').strip()

    if customer_name or claim_number:
        results = Claim.objects.all()
        if customer_name:
            results = results.filter(customer_name__icontains=customer_name)
        if claim_number:
            results = results.filter(claim_number__icontains=claim_number)

    return render(request, 'warranty/policies_search.html', {'results': results})

def update_claim(request):
    """ Handle form submission for updating an existing claim (e.g. assign, resolve, status). """
    if request.method == 'POST':
        claim_number = request.POST.get('claim_number')
        claim = get_object_or_404(Claim, claim_number=claim_number)

        # Update claim fields from form inputs
        claim.status = request.POST.get('status')
        claim.assigned_to = request.POST.get('assigned_to')
        claim.c3_notes = request.POST.get('c3_notes')
        claim.save()

        return HttpResponseRedirect(reverse('users:dealer_dashboard'))  # or another success page

    return render(request, 'users/dealer_dashboard.html')







