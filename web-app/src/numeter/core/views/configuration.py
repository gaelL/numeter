from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from core.models import User, Storage
from core.forms import User_EditForm, User_Admin_EditForm, User_PasswordForm, Storage_Form
from core.utils.decorators import login_required


@login_required()
def configuration_index(request):
    return render(request, 'configuration/index.html', {
        'title': 'Numeter - Configuration',
        'EditForm': User_EditForm(instance=request.user),
        'PasswordForm': User_PasswordForm(instance=request.user),
        'Users': User.objects.all(),
        'Groups': Group.objects.all(),
        'Storages': Storage.objects.all(),
    })


@login_required()
def profile_index(request):
    return render(request, 'configuration/profile.html', {
        'EditForm': User_EditForm(instance=request.user),
        'PasswordForm': User_PasswordForm(instance=request.user),
    })


@login_required()
def update_profile(request, user_id):
    U = get_object_or_404(User.objects.filter(pk=user_id))
    F = User_EditForm(data=request.POST, instance=U)
    if F.is_valid():
        F.save()
        messages.success(request, _("Profile updated with success."))
    else:
        for field,error in F.errors.items():
            messages.error(request, '<b>%s</b>: %s' % (field,error))

    return render(request, 'base/messages.html', {})


@login_required()
def update_password(request, user_id):
    if request.user.id != int(user_id):
        if not request.user.is_superuser:
            raise Http404

    U = get_object_or_404(User.objects.filter(pk=user_id))
    F = User_PasswordForm(data=request.POST, instance=U)
    if F.is_valid():
        F.save()
        messages.success(request, _("Password updated with success."))
    else:
        for field,error in F.errors.items():
            messages.error(request, '<b>%s</b>: %s' % (field,error))

    return render(request, 'base/messages.html', {})


@login_required()
def storage_index(request):
    storages = Storage.objects.all()
    storages = Paginator(storages, 20)
    return render(request, 'configuration/storages/index.html', {
        'storages_page': storages.page(1)
    })


@login_required()
def storage_get(request, storage_id):
    S = get_object_or_404(Storage.objects.filter(pk=storage_id))
    F = Storage_Form(instance=S)
    return render(request, 'configuration/storages/storage.html', {
        'Storage_Form': F,
    })


@login_required()
def storage_add(request):
    if request.method == 'POST':
        F = Storage_Form(request.POST)
        if F.is_valid():
            F.save()
            messages.success(request, _("Storage added with success."))
        else:
            for field,error in F.errors.items():
                messages.error(request, '<b>%s</b>: %s' % (field,error))
    else:
        return render(request, 'configuration/storages/storage.html', {
            'Storage_Form': Storage_Form(),
        })


@login_required()
def update_storage(request, storage_id):
    S = get_object_or_404(Storage.objects.filter(pk=storage_id))
    F = Storage_Form(data=request.POST, instance=S)
    if F.is_valid():
        F.save()
        messages.success(request, _("Storage updated with success."))
    else:
        for field,error in F.errors.items():
            messages.error(request, '<b>%s</b>: %s' % (field,error))

    return render(request, 'base/messages.html', {})
