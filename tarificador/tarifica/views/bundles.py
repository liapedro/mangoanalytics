#Views for bundles

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from tarifica import forms
from tarifica.tools.asteriskMySQLManager import AsteriskMySQLManager
from tarifica.models import *

def createBundle(request, destination_group_id):
    destination_group = get_object_or_404(DestinationGroup, id=destination_group_id)
    if request.method == 'POST': # If the form has been submitted...
        form = forms.createBundle(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            name = form.cleaned_data['name']
            tariff_mode = TariffMode.objects.get(id=form.cleaned_data['tariff_mode'])
            cost = form.cleaned_data['cost']
            amount = form.cleaned_data['amount']
            destination_group.has_bundles=True
            destination_group.save()
            priority = form.cleaned_data['priority']
            b = Bundle(
                priority = priority,
                name=name,
                destination_group=destination_group,
                tariff_mode=tariff_mode,
                cost=cost,
                amount=amount
                )
            b.save()
            return HttpResponseRedirect('/tarifica/setup') # Redirect after POST
    else:
        form = forms.createBundle() # An unbound form

    return render(request, 'tarifica/bundleCreate.html', {
        'form': form,
        'destination_group': destination_group
    })

def updateBundle(request, bundle_id):
    b = get_object_or_404(Bundle, id = bundle_id)
    if request.method == 'POST': # If the form has been submitted...
        form = forms.createBundle(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            b.name = form.cleaned_data['name']
            b.tariff_mode = TariffMode.objects.get(id=form.cleaned_data['tariff_mode'])
            b.cost = form.cleaned_data['cost']
            b.amount = form.cleaned_data['amount']
            b.priority = form.cleaned_data['priority']
            b.save()
            return HttpResponseRedirect('/tarifica/setup') # Redirect after POST
    else:
        form = forms.createBundle(initial=
        {'name': b.name,
         'destination_group': b.destination_group,
         'tariff_mode': b.tariff_mode,
         'cost': b.cost,
         'amount': b.amount,
         'priority': b.priority,
        }) # An unbound form

    return render(request, 'tarifica/bundleUpdate.html', {
        'form': form,
        'bundle' : b,
    })

def deleteBundle(request, bundle_id):
    bundle = get_object_or_404(Bundle, id = bundle_id)
    bundle.delete()
    return HttpResponseRedirect('/tarifica/setup')