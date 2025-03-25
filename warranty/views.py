from django.shortcuts import render, get_object_or_404
from .models import Claim, Policy


def claims_landing(request):
    """ Display claims pending a decision and show a policy search form """
    pending_claims = Claim.objects.filter(status='Pending')
    return render(request, 'warranty/claims_landing.html', {
        'pending_claims': pending_claims
    })


def claims_list(request):
    """ Display all warranty claims in a list/table """
    claims = Claim.objects.all().order_by('-date_issued')
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
    """ Search for warranty policies using optional filters """
    policies = Policy.objects.all()

    if request.method == "GET":
        first_name = request.GET.get("first_name")
        last_name = request.GET.get("last_name")
        email = request.GET.get("email")
        phone = request.GET.get("phone")
        policy_number = request.GET.get("policy_number")

        if first_name:
            policies = policies.filter(first_name__icontains=first_name)
        if last_name:
            policies = policies.filter(last_name__icontains=last_name)
        if email:
            policies = policies.filter(email__icontains=email)
        if phone:
            policies = policies.filter(phone__icontains=phone)
        if policy_number:
            policies = policies.filter(policy_number__icontains=policy_number)

    return render(request, 'warranty/policies_search.html', {
        'results': policies
    })

