from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CreateSessionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from Bookings.models import Booking, Session, IndividualSession 
from .models import Profile
from datetime import datetime, timedelta
from django.http import JsonResponse 
import json # for js we need json format

tmrtime = datetime.now() + timedelta(hours = 24)#used in filtering bookings for profile
def CustomLoginView(LoginView):
    if request.method == "POST":
        form = authentication_form(request.POST, instance=request.user)
        if form.is_valid and request.user.profile.is_teacher:
            form.save()
    return render(request, 'users/teacherprofile.html')

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)#creates a form with the POST data so if not valid some data still in the form
        if form.is_valid():
            form.save() # auto hashes password for security
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}, you can now login!') # pop up message for user
            return redirect("login")
    else:
        form = UserRegisterForm()
    #checks if post request try to validate the form data, otherwise instantiate empty form
    return render(request, 'users/register.html', {'form': form})

def get_data(request, *args, **kwargs):
    labels1 = []    
    data1vals = [] #contains values
    data1 = []   #contains the count
    chartdata = Booking.objects.all().filter(user = request.user).order_by("individualsession__sessiontime")  # get queryset for chart
    #for session in chartlabels:
     #   labels1.append(session.title)  this gets all sessions we want only user booked 
    for each in chartdata:
        data1vals.append(each.individualsession.session.id)
    #if of all 
    data1vals = set(data1vals) # get unique items rid of dupes
    data1vals = list(data1vals)
    for index in data1vals:
        session = Session.objects.all().filter(id=index).get()
        labels1.append(session.title)
    #returns the constant variables but only for sessions a user has booked using index from booking id
    for val in range(len(data1vals)):
        data1.append(0)
    #populate data with 0s for each unique session
    for booking in chartdata:  # go through queryset for bookings
        for index in range(len(data1vals)):   #for every booking, for every value in session index list
            if booking.individualsession.session.id == data1vals[index]:  #for every booking this user has for a specific session we raise counter by 1
                data1[index] += 1
    #make vals list with id for ecah session a person has booked
    #make a data list with 0 for each session booked
    # compare bookng session id with id in list and increment by 1 to get total for each item
    #BELOW CHART DATA FOR TEACHERP
    tlabels = []
    tspaces = []
    tbooked = []
    sessionid = []
    session = IndividualSession.objects.all().filter(session__teacher = request.user) # get sessions which specific teacherteaches
    bookings = Booking.objects.all()
    for each in session:
        label = str(each.session),":",str(each.sessiontime) # contain string for lavel
        tlabels.append(label) # sessions asscociated with certain teacher
        sessionid.append(each.id)   #id utilized for bookingcount matching to correct session
    print(tlabels,sessionid)
    for each in session:
        tspaces.append(each.session.spaces) # get max spaces
    for x in range(len(session)):
        tbooked.append(0)
    print(tbooked)
    for each in bookings:
        for index in range(len(sessionid)):
            if each.individualsession.id == sessionid[index]:
                tbooked[index] +=1
    print(tbooked)



    data = {
        "labels": labels1,   
        "data": data1,
        "tlabels": tlabels,
        "tspaces": tspaces,
        "tbooked": tbooked
    }
    return JsonResponse(data)
    #we get jsonresponse not htmlresp so we can get json data to use in any page

@login_required  #login decorator user must be logged in to view this page , this is the reason we dont pass user data as a user must be logged in 
def profile(request):
    #for loop to get chart vals
    if request.user.profile.is_teacher:
        return redirect("teacherprofile")
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user) # pass in current users info to the forms
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES,
                                   instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account Updated Successfully') # pop up message for user
            return redirect("profile")
    
    else: 
        u_form = UserUpdateForm(instance=request.user) # pass in current users info to the forms
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'bookings': Booking.objects.all().filter(user = request.user, individualsession__sessiontime__gt = tmrtime) #24 hours future
        # dynamic filtering above using foreign key attrs 
     }
    return render(request, 'users/profile.html', context)


#same as user profile in terms of form however different stuff overall page
#COMMENTS REQUIRED
@login_required
def teacherprofile(request):
    if not request.user.profile.is_teacher:
        return redirect("profile")
    u_form = UserUpdateForm(instance=request.user) # pass in current users info to the forms
    p_form = ProfileUpdateForm(instance=request.user.profile)
    newsession_form = CreateSessionForm()
    sessionlist = IndividualSession.objects.all().filter(session__teacher = request.user).order_by('sessiontime', 'id')
    bookinglist = Booking.objects.all().filter(individualsession__session__teacher = request.user).order_by('individualsession')
   # print(bookinglist)
   # print(sessionlist)
    if request.method == "POST": 
        if 'profileupdateform' in request.POST:
            u_form = UserUpdateForm(request.POST, instance=request.user) # pass in current users info to the forms
            p_form = ProfileUpdateForm(request.POST, 
                                    request.FILES,
                                    instance=request.user.profile)
            
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Account Updated Successfully') # pop up message for user
                return redirect("profile")
       
        # elif statement to separate post reqs below handles delete functionality
        elif 'pk' in request.POST:
           #p print(request.POST['pk'])
            Booking.objects.all().filter(pk=request.POST['pk']).delete()
            return redirect('profile')
        
        elif 'createsession' in request.POST:
            newsession_form = CreateSessionForm(request.POST)
            if newsession_form.is_valid():
                newsession_form.save()
                messages.success(request, f'Session Created Successfully')
                return redirect('profile')
   
    else: 
        u_form = UserUpdateForm(instance=request.user) # pass in current users info to the forms
        p_form = ProfileUpdateForm(instance=request.user.profile)
        newsession_form = CreateSessionForm()
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'newsession_form': newsession_form, 
        'pagetitle': 'Teacher',
        'booking': bookinglist,
        'session': sessionlist
        

    }
    return render(request, 'users/teacherprofile.html', context)

