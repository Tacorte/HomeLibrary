from django.shortcuts import render, get_object_or_404
from .forms import ProfileForm
from django.shortcuts import redirect


def info(request):
    user = request.user.username
    return render(request, 'UserInterfaceapp/welcome.html', {'user': user})


def userinfo(request):
    profile = request.user.profile

    # profile = Profile.object.get(user=request.user.username)
    return render(request, "UserInterfaceapp/user.html",{'profile': profile})


def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            #profile.name = form.name
            #profile.surname = request.profile.surname
            #profile.middle_name = request.profile.middle_name
            profile.save()
            return redirect('user_info')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'UserInterfaceapp/edit.html', {'form': form})



