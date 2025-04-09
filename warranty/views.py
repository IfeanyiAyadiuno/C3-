from django.shortcuts import render, get_object_or_404, redirect
from .models import Claim
from django.utils.timezone import now
from decimal import Decimal, InvalidOperation

def claims_landing(request):
    pending_claims = Claim.objects.filter(status='Pending')
    return render(request, 'warranty/claims_landing.html', {
        'pending_claims': pending_claims
    })

def claims_list(request):
    claims = Claim.objects.exclude(claim_number__isnull=True).exclude(claim_number__exact='').order_by('-date_issued')
    return render(request, 'warranty/claims_list.html', {
        'claims': claims
    })

def claim_detail(request, claim_id):
    claim = get_object_or_404(Claim, pk=claim_id)

    if request.method == 'POST':
        claim.status = request.POST.get('status')
        claim.assigned_to = request.POST.get('assigned_to')
        claim.c3_notes = request.POST.get('c3_notes')

        estimate_input = request.POST.get('estimate_amount')
        if estimate_input:
            try:
                claim.estimate_amount = Decimal(estimate_input)
            except InvalidOperation:
                claim.estimate_amount = None
        else:
            claim.estimate_amount = None

        claim.save()
        return redirect('warranty:claim_detail', claim_id=claim.id)

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










