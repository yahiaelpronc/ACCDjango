from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *
# Create your views here.


@api_view(['GET'])
def usersList(request):
    users = Myuser.objects.all()
    serializer = UsersSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getUser(request, username):
    user = Myuser.objects.get(username=username)
    serializer = UsersSerializer(user)
    return Response(serializer.data)


@api_view(['DELETE'])
def deleteUser(request, username):
    user = Myuser.objects.get(username=username)
    user.delete()
    return Response('Item Successfully Deleted')


# @api_view(['GET'])
# def taskDetail(request, pk):
#     tasks = Task.objects.get(id=pk)
#     serializer = TaskSerializer(tasks, many=False)
#     return Response(serializer.data)


# @api_view(['POST'])
# def taskCreate(request):
#     serializer = TaskSerializer(data=request.data)
#     if(serializer.is_valid()):
#         serializer.save()
#     return Response(serializer.data)


# @api_view(['POST'])
# def taskUpdate(request, pk):
#     task = Task.objects.get(id=pk)
#     serializer = TaskSerializer(instance=task, data=request.data)
#     if(serializer.is_valid()):
#         serializer.save()
#     return Response(serializer.data)


# @api_view(['DELETE'])
# def taskDelete(request, pk):
#     task = Task.objects.get(id=pk)
#     task.delete()
#     return Response('Item Successfully Deleted')


# def home(request):
#     return render(request, 'home.html')


# def addAnimal(request):
#     if(request.method == 'GET'):
#         return render(request, 'addAnimal.html')
#     else:
#         context = {}
#         # Backend Validation
#         if(len(request.POST['animalName']) < 3 or len(request.POST['animalName']) > 30):
#             context['errAnimalName'] = 'This name is not valid , Please Try Again'
#             return render(request, 'addAnimal.html', context)
#         if(Animal.objects.filter(animalName=request.POST['animalName']+"_"+request.session['username']).exists()):
#             context['errAnimalExists'] = 'An Animal Of Yours Is Already Registered With This Name , Please Try A Different Name'
#             return render(request, 'addAnimal.html', context)

#         # If Female Add female_state
#         if(request.POST['gender'] == "f"):
#             animal = Animal.objects.create(animalName=request.POST['animalName']+"_"+request.session['username'],
#                                            ownerUsername=request.session['username'],
#                                            weight=request.POST['weight'],
#                                            gender=request.POST['gender'],
#                                            female_state=request.POST['female_state'],
#                                            species=request.POST['species'],
#                                            b_date=request.POST['b_date'])
#             context['success'] = "Your Animal Is Now Registered"
#             return render(request, 'addAnimal.html', context)

#         # If Male Do Not Add female_state
#         animal = Animal.objects.create(animalName=request.POST['animalName']+"_"+request.session['username'],
#                                        ownerUsername=request.session['username'],
#                                        weight=request.POST['weight'],
#                                        gender=request.POST['gender'],
#                                        species=request.POST['species'],
#                                        b_date=request.POST['b_date'])
#         context['success'] = "Your Animal Is Now Registered"
#         return render(request, 'addAnimal.html', context)


# def logout(request):
#     request.session.clear()
#     return render(request, 'home.html')


# def viewMessages(request):
#     user = Myuser.objects.get(username=request.session['username'])
#     vet = Vet.objects.get(username=request.session['vet_username'])
#     Message = Messages.objects.filter(
#         Q(sender=vet.username) | Q(sender=user.username), Q(receiver=vet.username) | Q(receiver=user.username)).values()
#     user_firstname = user.firstname
#     vet_firstname = vet.firstname
#     return JsonResponse({"Messages": list(Message), "user_firstname": user_firstname, "vet_firstname": vet_firstname})


# def sendMessage(request, contents=""):
#     print("inside view ------------------------------------------------")
#     user = Myuser.objects.get(username=request.session['username'])
#     vet = Vet.objects.get(username=request.session['vet_username'])
#     messages = Messages.objects.create(
#         content=contents, sender=user.username, receiver=vet.username)
#     json_response = {'message': {'content': messages.content,
#                                  'vet': vet.username, 'user': user.username}}
#     return HttpResponse(json.dumps(json_response), content_type='application/json')


# def locationDetails(request, id):
#     mylocation = locations.objects.get(id=id)
#     context = {}
#     context['location'] = mylocation
#     return render(request, 'details.html', context)


# def listlocations(request):
#     myloctions = locations.objects.all()
#     context = {}
#     context['locations'] = myloctions
#     return render(request, 'locations.html', context)


# def addlocation(request):
#     if(request.method == 'GET'):
#         return render(request, 'Admin.html')
#     else:
#         name_reg = r"^[a-zA-Z ,.'-]{4,30}$"
#         email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#         phone_regex = r'^01[0125][0-9]{8}$'
#         address_reg = r"^[a-zA-Z ,.'-]{4,40}$"

#         if(re.search(name_reg, request.POST['name']) == None):
#             context = {}
#             context['errname'] = 'this name is not valid ,type a valid one'
#             return render(request, 'Admin.html', context)
#         if(re.search(address_reg, request.POST['address']) == None):
#             context = {}
#             context['erraddress'] = 'this address is not valid ,type a valid one'
#             return render(request, 'Admin.html', context)
#         if(int(request.POST['work_start']) > 12 or int(request.POST['work_start']) < 0):
#             context = {}
#             context['errworkstart'] = 'please enter a number btw 1 and 12'
#             return render(request, 'Admin.html', context)
#         if(int(request.POST['work_end']) > 12 or int(request.POST['work_end']) < 0):
#             context = {}
#             context['errworkend'] = 'please enter a number btw 1 and 12'
#             return render(request, 'Admin.html', context)

#         if(re.search(email_regex, request.POST['email']) == None):
#             context = {}
#             context['erremail'] = 'this email is not valid ,type a valid one'
#             return render(request, 'Admin.html', context)

#         if(re.search(phone_regex, request.POST['mobile']) == None):
#             context = {}
#             context['errmobile'] = 'this mobile is not valid ,type a valid one'
#             return render(request, 'Admin.html', context)
#         else:
#             location = locations.objects.create(name=request.POST['name'], email=request.POST['email'],
#                                                 address=request.POST['address'], mobile=request.POST['mobile'],
#                                                 website_link=request.POST['website_link'], picture=request.FILES['picture'],
#                                                 work_hours_start=request.POST[
#                                                     'work_start'], work_hours_end=request.POST['work_end'],
#                                                 work_hours_start_period=request.POST['start_period'],
#                                                 work_hours_end_period=request.POST['end_period'],

#                                                 )
#             return render(request, 'Admin.html')


# def getVetFirstName(request, vet_username):
#     print("inside view ------------------------------------------------")
#     vet = Vet.objects.get(username=vet_username)
#     first_name = vet.firstname
#     request.session['vet_username'] = vet_username
#     json_response = {'vet': {'firstname': first_name}}
#     return HttpResponse(json.dumps(json_response), content_type='application/json')


# def emergency(request):
#     if(request.method == "POST"):
#         return render(request, 'Emergency Animal.html')
#     vets = Vet.objects.all()
#     Locations = locations.objects.all()
#     context = {}
#     context['vets'] = vets
#     context['Locations'] = Locations
#     return render(request, 'Emergency Animal.html', context)


# def verifyUser(request, username, dates):
#     myuser = Myuser.objects.get(username=username)

#     date1 = str(dates)
#     date1 = dates.split('-')
#     # Creation Dates
#     CreationDay = int(date1[2])
#     CreationMonth = int(date1[1])
#     CreationYear = int(date1[0])
#     # Expiration Dates
#     expireDay = str(date.today())
#     expireDay = expireDay.split('-')
#     expireDay = int(expireDay[2]) - CreationDay
#     expireMonth = str(date.today())
#     expireMonth = expireMonth.split('-')
#     expireMonth = int(expireMonth[1]) - CreationMonth
#     expireYear = str(date.today())
#     expireYear = expireYear.split('-')
#     expireYear = int(expireYear[0]) - CreationYear

#     if(myuser != None):
#         if(expireDay > 0 or expireMonth > 0 or expireYear > 0):

#             didResend = sendEmail(request, myuser.email,
#                                   resend=True, username=myuser.username)

#             didResend = sendEmail(
#                 request, myuser.email, resend=True, username=myuser.username)

#             if(didResend):
#                 return render(request, 'resendEmail.html')
#             else:
#                 return render(request, 'ResendFailed.html')
#         else:
#             if(myuser.active_status):
#                 return render(request, 'alreadyVerified.html')
#             else:
#                 myuser.active_status = True
#                 myuser.save()
#                 return render(request, 'successVerified.html')
#     else:
#         return HttpResponse("The User You're Trying to Verify Doesn't Exist")


# def verifyVet(request, username, dates):
#     myvet = Vet.objects.get(username=username)

#     date1 = str(dates)
#     date1 = dates.split('-')
#     # Creation Dates
#     CreationDay = int(date1[2])
#     CreationMonth = int(date1[1])
#     CreationYear = int(date1[0])
#     # Expiration Dates
#     expireDay = str(date.today())
#     expireDay = expireDay.split('-')
#     expireDay = int(expireDay[2]) - CreationDay
#     expireMonth = str(date.today())
#     expireMonth = expireMonth.split('-')
#     expireMonth = int(expireMonth[1]) - CreationMonth
#     expireYear = str(date.today())
#     expireYear = expireYear.split('-')
#     expireYear = int(expireYear[0]) - CreationYear

#     if(myvet != None):
#         if(expireDay > 0 or expireMonth > 0 or expireYear > 0):

#             didResend = sendEmail(request, myvet.email,
#                                   resend=True, username=myvet.username)

#             didResend = sendEmailVet(
#                 request, myvet.email, resend=True, username=myvet.username)

#             if(didResend):
#                 return render(request, 'resendEmail.html')
#             else:
#                 return render(request, 'ResendFailed.html')

#         else:
#             if(myvet.active_status):
#                 return render(request, 'alreadyVerified.html')

#             else:
#                 myvet.active_status = True
#                 myvet.save()
#                 return render(request, 'successVerified.html')

#     else:
#         return HttpResponse("The User You're Trying to Verify Doesn't Exist")


# # def sendEmail(request,recepient,resend=False,username=None):
# #     socket.getaddrinfo('localhost',8000)
# #     fromaddr=settings.EMAIL_HOST_USER
# #     toaddr=recepient
# #     server=smtplib.SMTP('smtp.gmail.com', 587)


# def sendEmail(request, recepient, resend=False, username=None):
#     socket.getaddrinfo('localhost', 8000)
#     fromaddr = settings.EMAIL_HOST_USER
#     toaddr = recepient
#     server = smtplib.SMTP('smtp.gmail.com', 587)

#     server.connect("smtp.gmail.com", 587)
#     server.ehlo()
#     server.starttls()
#     server.ehlo()
#     server.login(fromaddr, varA)
#     if(resend):

#         link = 'http://127.0.0.1:8000/verify/' + \
#             request.POST['username'] + '/' + str(date.today())
#         # myuser=Myuser.objects.get(username=username)
#         # myuser.active_link=link
#         # myuser.save()
#         text = 'hello  '+username+'  please Verify your account here  ' + link
#         subject = 'Animal Care Center Site 2022 By ITI  , ' + \
#             request.POST['username']
#         mailtext = 'subject : ' + subject+'\n\n'+text
#         server.sendmail(fromaddr, toaddr, mailtext)
#         server.quit()
#         return True
#     link = 'http://127.0.0.1:8000/verify/' + \
#         request.POST['username'] + '/'+str(date.today())
#     # myuser=Myuser.objects.get(username=req.POST['username'])
#     # myuser.active_link=link
#     # myuser.save()
#     text = 'hello '+request.POST['username'] + \
#         '  please Verify your account from here  '+link
#     subject = 'Animal Care Center Site 2022 By ITI , '+request.POST['username']
#     mailtext = 'subject : ' + subject + '\n\n' + text
#     server.sendmail(fromaddr, toaddr, mailtext)
#     server.quit()


# def sendEmailVet(request, recepient, resend=False, username=None):

#     socket.getaddrinfo('localhost', 8000)
#     fromaddr = settings.EMAIL_HOST_USER
#     toaddr = recepient
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.connect("smtp.gmail.com", 587)
#     server.ehlo()
#     server.starttls()
#     server.ehlo()
#     server.login(fromaddr, varA)
#     if(resend):

#         link = 'http://127.0.0.1:8000/verifyVet/' + \
#             request.POST['username'] + '/' + str(date.today())
#         # myuser=Myuser.objects.get(username=username)
#         # myuser.active_link=link
#         # myuser.save()
#         text = 'hello  '+username+'  please Verify your account here  ' + link
#         subject = 'Animal Care Center Site 2022 By ITI  , ' + \
#             request.POST['username']
#         mailtext = 'subject : ' + subject+'\n\n'+text
#         server.sendmail(fromaddr, toaddr, mailtext)
#         server.quit()
#         return True
#     link = 'http://127.0.0.1:8000/verifyVet/' + \
#         request.POST['username'] + '/'+str(date.today())
#     # myuser=Myuser.objects.get(username=req.POST['username'])
#     # myuser.active_link=link
#     # myuser.save()
#     text = 'hello '+request.POST['username'] + \
#         '  please Verify your account from here  '+link
#     subject = 'Animal Care Center Site 2022 By ITI , '+request.POST['username']
#     mailtext = 'subject : ' + subject + '\n\n' + text
#     server.sendmail(fromaddr, toaddr, mailtext)
#     server.quit()


# def registerUser(request):
#     if(request.method == 'GET'):
#         return render(request, 'Registration.html')
#     else:
#         name_reg = r"^[a-zA-Z ,.'-]{4,20}$"
#         email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#         phone_regex = r'^01[0125][0-9]{8}$'

#         if(re.search(name_reg, request.POST['username']) == None):
#             context = {}
#             context['errusername'] = 'This Username Is Not Valid, Enter Valid UserName'
#             return render(request, 'Registration.html', context)

#         if(re.search(name_reg, request.POST['firstname']) == None):
#             context = {}
#             context['errfirstname'] = 'This firstname Is Not Valid, Enter Valid firstname'
#             return render(request, 'Registration.html', context)

#         if(re.search(name_reg, request.POST['lastname']) == None):
#             context = {}
#             context['errlastname'] = 'This lastname Is Not Valid, Enter Valid lastname'
#             return render(request, 'Registration.html', context)

#         if(re.search(email_regex, request.POST['email']) == None):
#             context = {}
#             context['erremail'] = 'This email Is Not Valid, Enter Valid email'
#             return render(request, 'Registration.html', context)

#         if(re.search(phone_regex, request.POST['mobile']) == None):
#             context = {}
#             context['errmobile'] = 'This mobile Is Not Valid, Enter Valid mobile'
#             return render(request, 'Registration.html', context)
#         if(request.POST['password'] != request.POST['confirmpassword']):
#             context = {}
#             context['errnotequal'] = 'confirm password must equal to password'
#             return render(request, 'Registration.html', context)
#         else:

#             username = request.POST['username']
#             firstname = request.POST['firstname']
#             lastname = request.POST['lastname']
#             profile_pic = request.FILES['profile_pic']
#             email = request.POST['email']
#             password = request.POST['password']
#             confirmpassword = request.POST['confirmpassword']
#             mobile = request.POST['mobile']
#             b_date = request.POST['b_date']
#             country = request.POST['country']
#             face_link = request.POST['face_link']

#             myuser = Myuser.objects.create(username=username, firstname=firstname, lastname=lastname, profile_pic=profile_pic,
#                                            email=email, password=password, mobile=mobile, b_date=b_date, country=country,
#                                            face_link=face_link)
#             recepient = request.POST['email']
#             sendEmail(request, recepient)

#             return render(request, 'welcome.html')


# def registervet(request):
#     if(request.method == 'GET'):
#         return render(request, 'registervet.html')
#     else:
#         name_reg = r"^[a-zA-Z ,.'-]{4,20}$"
#         email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#         phone_regex = r'^01[0125][0-9]{8}$'
#         address_reg = r"^[a-zA-Z ,.'-]{4,40}$"
#         if(re.search(name_reg, request.POST['username']) == None):
#             context = {}
#             context['errusername'] = 'This Username Is Not Valid, Enter Valid UserName'
#             return render(request, 'registervet.html', context)
#         if (re.search(name_reg, request.POST['firstname']) == None):
#             context = {}
#             context['errfirstname'] = 'This firstname Is Not Valid, Enter Valid firstname'
#             return render(request, 'registervet.html', context)

#         if (re.search(name_reg, request.POST['lastname']) == None):
#             context = {}
#             context['errlastname'] = 'This lastname Is Not Valid, Enter Valid lastname'
#             return render(request, 'registervet.html', context)

#         if (re.search(email_regex, request.POST['email']) == None):
#             context = {}
#             context['erremail'] = 'This email Is Not Valid, Enter Valid email'
#             return render(request, 'registervet.html', context)

#         if (re.search(phone_regex, request.POST['mobile']) == None):
#             context = {}
#             context['errmobile'] = 'This mobile Is Not Valid, Enter Valid mobile'
#             return render(request, 'registervet.html', context)
#         if (request.POST['password'] != request.POST['confirmpassword']):
#             context = {}
#             context['errnotequal'] = 'confirm password must equal to password'
#             return render(request, 'registervet.html', context)
#         if(re.search(address_reg, request.POST['address']) == None):
#             context = {}
#             context['erraddress'] = 'this address is not valid '
#             return render(request, 'registervet.html', context)

#         else:
#             username = request.POST['username']
#             firstname = request.POST['firstname']
#             lastname = request.POST['lastname']
#             profile_pic = request.FILES['profile_pic']
#             email = request.POST['email']
#             password = request.POST['password']
#             mobile = request.POST['mobile']
#             b_date = request.POST['b_date']
#             country = request.POST['country']
#             face_link = request.POST['face_link']
#             specialization = request.POST['specialization']
#             address = request.POST['address']

#             MYvet = Vet.objects.create(username=username, firstname=firstname, lastname=lastname, profile_pic=profile_pic,
#                                        email=email, password=password, mobile=mobile, b_date=b_date, country=country,
#                                        face_link=face_link, specialization=specialization, address=address)
#             recepient = request.POST['email']
#             sendEmailVet(request, recepient)

#             return render(request, 'welcome.html')


# def logingeneral(request):
#     return render(request, 'loginUsers.html')


# def testwel(request):
#     return render(request, 'welcome.html')


# def login(request):
#     if(request.method == 'GET'):
#         return render(request, 'login.html')
#     else:

#         myuser = Myuser.objects.filter(
#             username=request.POST['username'], password=request.POST['password'])

#         if(len(myuser) != 0):
#             myuser1 = Myuser.objects.get(username=request.POST['username'])
#             if(myuser1.active_status == False):
#                 return render(request, 'notVerified.html')
#             else:
#                 request.session['username'] = request.POST['username']
#                 request.session['firstname'] = myuser1.firstname
#                 request.session['pic_url'] = myuser1.profile_pic.url
#                 return render(request, 'home.html')
#         else:
#             context = {}
#             context['notfound'] = 'this username and password are not correct'
#             return render(request, 'login.html', context)


# def loginVet(request):
#     if(request.method == 'GET'):
#         return render(request, 'login.html')
#     else:
#         myvet = Vet.objects.filter(
#             username=request.POST['username'], password=request.POST['password'])
#         if(len(myvet) != 0):
#             vet1 = Vet.objects.get(
#                 username=request.POST['username'], password=request.POST['password'])
#             if(vet1.active_status):
#                 request.session['vet_username'] = request.POST['username']
#                 return render(request, 'home.html')
#             else:
#                 return render(request, 'notVerified.html')
#         else:
#             context = {}
#             context['notfound'] = 'this username and password are not correct'
#             return render(request, 'login.html', context)


# def test(request):
#     return render(request, 'Admin.html')
