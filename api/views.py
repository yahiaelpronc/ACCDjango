from logging.handlers import MemoryHandler
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import status
# Create your views here.


from django.core.mail import EmailMessage
from django.conf import settings
import json
import smtplib
import socket
from datetime import date
from datetime import datetime, timedelta
from vars import *
import re
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models import Q


@api_view(['POST'])
def addMedication(request):
    mydata = MedicationSerializer(data=request.data)
    if(mydata.is_valid()):
        mydata.save()
        return Response(mydata.data)
    else:
        return Response(mydata.errors)


@api_view(['GET'])
def findAnimals(request, ownerusername):
    myAnimals = Animal.objects.filter(ownerUsername=ownerusername)
    print(myAnimals)
    if(len(myAnimals) != 0):
        mydata = AnimalSerializer(myAnimals, many=True)
        return Response(mydata.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def checkUserOnline(request, username):
    myUser = Myuser.objects.get(username=username)
    if(myUser.isOnline):
        api_response = {
            'isOnline': True,
        }
        return Response(api_response)
    api_response = {
        'isOnline': False,
    }
    return Response(api_response)


@api_view(['GET'])
def checkVetOnline(request, username):
    myVet = Vet.objects.get(username=username)
    if(myVet.isOnline):
        api_response = {
            'isOnline': True,
        }
        return Response(api_response)
    api_response = {
        'isOnline': False,
    }
    return Response(api_response)


@api_view(['POST'])
def addMessage(request):
    mydata = MessagesSerializer(data=request.data)
    if(mydata.is_valid()):
        mydata.save()
        return Response(mydata.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def getAllMessages(request, sender, receiver):
    # user = Myuser.objects.get(username=request.session['username'])
    # vet = Vet.objects.get(username=request.session['vet_username'])
    user = Myuser.objects.get(username=sender)
    vet = Vet.objects.get(username=receiver)
    Message = Messages.objects.filter(
        Q(sender=vet.username) | Q(sender=user.username), Q(receiver=vet.username) | Q(receiver=user.username)).values()
    Message = MessagesSerializer(Message, many=True)
    return Response(Message.data)


@api_view(['GET'])
def logout(request, username):
    myuser = Myuser.objects.get(username=username)
    myuser.isOnline = False
    myuser.save()
    request.session.clear()
    api_response = {
        'didLogout': True,
    }
    return Response(api_response)


@api_view(['GET'])
def logoutVet(request, username):
    myVet = Vet.objects.get(username=username)
    myVet.isOnline = False
    myVet.save()
    request.session.clear()
    api_response = {
        'didLogout': True,
    }
    return Response(api_response)


@api_view(['GET'])
def resendEmail(request, username):
    myUser = Myuser.objects.filter(username=username).exists()
    myVet = Vet.objects.filter(username=username).exists()
    if(myUser):
        myUser = Myuser.objects.get(username=username)
        recepient = myUser.email
        sendEmail(request, recepient, resend=True, username=myUser.username)
        api_response = {
            'didResend': True,
        }
        return Response(api_response)
    if(myVet):
        myVet = Vet.objects.get(username=username)
        recepient = myVet.email
        sendEmail(request, recepient, resend=True, username=myVet.username)
        api_response = {
            'didResend': True,
        }
        return Response(api_response)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def checkVerified(request, username):
    myUser = Myuser.objects.filter(username=username).exists()
    myVet = Vet.objects.filter(username=username).exists()
    if(myUser):
        myUser = Myuser.objects.get(username=username)
        if(myUser.active_status):
            api_response = {
                'isActive': True,
            }
            return Response(api_response)
        else:
            api_response = {
                'isActive': False,
            }
            return Response(api_response)
    if(myVet):
        myVet = Vet.objects.get(username=username)
        if(myVet.active_status):
            api_response = {
                'isActive': True,
            }
        else:
            api_response = {
                'isActive': False,
            }
            return Response(api_response)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def loginVet(request, username, password):
    if(Vet.objects.filter(username=username, password=password).exists()):
        myVet = Vet.objects.get(username=username, password=password)
        myVet.isOnline = True
        myVet.save()
        request.session['vet_username'] = myVet.username
        vetData = VetSerializer(myVet)
        return Response(vetData.data)
    return Response("Incorrect Credintials")


@api_view(['GET'])
def loginUser(request, username, password):
    if(Myuser.objects.filter(username=username, password=password).exists()):
        myuser = Myuser.objects.get(username=username, password=password)
        myuser.isOnline = True
        myuser.save()
        request.session['username'] = myuser.username
        print("----------------------------------"+request.session['username'])
        userData = UsersSerializer(myuser)
        return Response(userData.data)
    return Response("Incorrect Credintials")


@api_view(['GET'])
def listAnimals(request, username):
    myAnimals = Animal.objects.filter(ownerUsername=username).exists()
    if(myAnimals):
        myAnimals = Animal.objects.filter(ownerUsername=username)
        animalsData = AnimalSerializer(myAnimals, many=True)
        return Response(animalsData.data)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# Add Animal
@api_view(['POST'])
def insertAnimal(request):
    mydata = AnimalSerializer(data=request.data)
    if(Animal.objects.filter(animalName=request.data['animalName']).exists()):
        return Response("An Animal Of Yours Already Has That Name")
    if(request.data['gender'] == ""):
        return Response("Please Choose A Gender")
    if(request.data['gender'] == "female"):
        print(request.data['female_state'])
        if(request.data['female_state'] == ""):
            return Response("Please Choose A Female State")
    if(request.data['species'] == ""):
        return Response("Please Choose A Species")

    if(mydata.is_valid()):
        mydata.save()
        print(mydata.data)
        return Response(mydata.data)
    else:
        return Response(mydata.errors)

# addSurgeryRequest


@api_view(['POST'])
def insertRequest(request):
    mydata = SurgicalOperationsRequestSerializer(data=request.data)
    if(mydata.is_valid()):
        mydata.save()
        print(mydata.data)
        return Response(mydata.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# find an animal wth usrname and animal name


@api_view(['GET'])
def findSpecificAnimal(request, username, animalName):
    myanimal = Animal.objects.get(
        animalName=animalName, ownerUsername=username)
    print(myanimal)
    if(myanimal != None):
        mydata = AnimalSerializer(myanimal)
        return Response(mydata.data)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# get all requests depend on Vetusername

@api_view(['GET'])
def getRequests(request, VetUserName):
    myrequests = SurgicalOperationsRequest.objects.filter(vetName=VetUserName)
    if(len(myrequests) != 0):
        mydata = SurgicalOperationsRequestSerializer(myrequests, many=True)
        print(mydata.data)
        return Response(mydata.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# get all Services requests depend on owner  name


@api_view(['GET'])
def getServicesRequests(request, locationOwner):
    myrequests = ServiseRequest.objects.filter(locationOwner=locationOwner)
    if(len(myrequests) != 0):
        mydata = ServiseRequestSerializer(myrequests, many=True)
        print(mydata.data)
        return Response(mydata.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# get surgical operations Resposes for user by animal owner


@api_view(['GET'])
def getSurgicalResponses(request, owner):
    myResponses = SurgicalOperations.objects.filter(owner=owner)
    if(len(myResponses) != 0):
        mydata = SurgicalOperationsSerializer(myResponses, many=True)
        print(mydata.data)
        return Response(mydata.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# update status of surgery request by id
@api_view(['POST'])
def updateRequestStatusUser(request, id):
    task = SurgicalOperationsRequest.objects.get(id=id)
    serializer = SurRequestStatusUserSerializer(
        instance=task, data=request.data)
    if(serializer.is_valid()):
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def updateRequestStatusVet(request, id):
    task = SurgicalOperationsRequest.objects.get(id=id)
    serializer = SurRequestStatusVetSerializer(
        instance=task, data=request.data)
    if(serializer.is_valid()):
        serializer.save()
        return Response(serializer.data)
    api_response = {
        'isOnline': True,
    }
    return Response(api_response)


# # update status of surgery request by id
# @api_view(['POST'])
# def updateRequestStatuss(request, id):
#     myrequest = SurgicalOperationsRequest.objects.get(id=id)
#     mydata = SurgicalOperationsRequestSerializer(
#         instance=myrequest, data=request.data)
#     if(mydata.is_valid()):
#         mydata.save()
#         return Response(mydata.data)
#     else:
#         return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def findRequest(request, id):
    myrequest = SurgicalOperationsRequest.objects.get(id=id)
    if(myrequest != None):
        mydata = SurgicalOperationsRequestSerializer(myrequest)
        return Response(mydata.data)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# addSurgery
@api_view(['POST'])
def insertSurgry(request):
    mydata = SurgicalOperationsSerializer(data=request.data)
    if(mydata.is_valid()):
        mydata.save()
        print(mydata.data)
        return Response(mydata.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# get A medication


@api_view(['GET'])
def getMedication(request, animalName):

    myMedications = Medication.objects.filter(animalName=animalName)
    if(len(myMedications) != 0):
        mydata = MedicationSerializer(myMedications, many=True)
        return Response(mydata.data)
        print(mydata.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# get A Surgery
@api_view(['GET'])
def getSurgery(request, VetName):

    mySurgeries = SurgicalOperations.objects.filter(vetName=VetName)
    if(len(mySurgeries) != 0):
        mydata = SurgicalOperationsSerializer(mySurgeries, many=True)
        return Response(mydata.data)
        print(mydata.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# Add Location
@api_view(['POST'])
def insertLocation(request):
    print(request.data)
    if(request.data['work_hours_start'] == ""
       or request.data['work_hours_end_period'] == ""
       or request.data['work_hours_start_period'] == ""
       or request.data['work_hours_start'] == ""):
        return Response("Please Choose Work Hours")
    print("1")
    if(request.data['governorate'] == ""):
        return Response("Please Choose A Governorate")
    if(request.data['service'] == ""):
        return Response("Please Choose A Service")
    print("1")
    if(locations.objects.filter(name=request.data['name']).exists()):
        return Response("A Location With This Name Already Exists")
    if(locations.objects.filter(email=request.data['email']).exists()):
        return Response("Email Already Exists")
    print("1")
    mydata = LocationsSerializer(data=request.data)
    if(mydata.is_valid()):
        mydata.save()
        print(mydata.data)
        return Response(mydata.data)
    else:
        return Response(mydata.errors)


# register user
@api_view(['POST'])
def insertuser(request):
    print("------------------API--------------------")
    mydata = UsersSerializer(data=request.data)
    if(Myuser.objects.filter(username=request.data['username']).exists()):
        return Response("Username Already Exists")
    if(Myuser.objects.filter(email=request.data['email']).exists()):
        return Response("Email Already Exists")
    if(mydata.is_valid()):
        mydata.save()
        print(mydata.data)
        print(mydata.data['email'])
        recepient = mydata.data['email']
        sendEmail(request, recepient, resend=False,
                  username=mydata.data['username'])
        return Response(mydata.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# register vet


@api_view(['POST'])
def insertVet(request):
    mydata = VetSerializer(data=request.data)
    if(Vet.objects.filter(username=request.data['username']).exists()):
        return Response("Username Already Exists")
    if(Vet.objects.filter(email=request.data['email']).exists()):
        return Response("Email Already Exists")
    if(request.data['specialization'] == ""):
        return Response("Specialization Field Is Required")
    if(mydata.is_valid()):
        mydata.save()
        print(mydata.data)
        recepient = mydata.data['email']
        sendEmail(request, recepient, resend=False,
                  username=mydata.data['username'])
        return Response(mydata.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# 1 - get all location
@api_view(['GET'])
def listlocation(request):
    mylocations = locations.objects.all()
    locationdata = LocationsSerializer(mylocations, many=True)
    return Response(locationdata.data)


# 2 - get certain location details (id)

@api_view(['GET'])
def locationDetails(request, id):
    mylocation = locations.objects.get(id=id)
    if(mylocation != None):
        locationdata = LocationsSerializer(mylocation)
        return Response(locationdata.data)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# 3 - get all users


@api_view(['GET'])
def listusers(request):
    allusers = Myuser.objects.all()
    if(len(allusers) != 0):
        mydata = UsersSerializer(allusers, many=True)
        return Response(mydata.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# 4 - get certain user (username)


@api_view(['GET'])
def finduser(request, username):
    myuser = Myuser.objects.get(username=username)
    if(myuser != None):
        mydata = UsersSerializer(myuser)
        return Response(mydata.data)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# 5 - get all vets

@api_view(['GET'])
def listVets(request):
    allVets = Vet.objects.all()
    if(len(allVets) != 0):
        mydata = VetSerializer(allVets, many=True)
        return Response(mydata.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# 6 - get certain vet (vet_username)


@api_view(['GET'])
def findvet(request, username):
    myvet = Vet.objects.get(username=username)
    if(myvet != None):
        mydata = VetSerializer(myvet)
        return Response(mydata.data)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET'])
# def usersList(request):
#     users = Myuser.objects.all()
#     serializer = UsersSerializer(users, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def getUser(request, username):
#     user = Myuser.objects.get(username=username)
#     serializer = UsersSerializer(user)
#     return Response(serializer.data)


# @api_view(['DELETE'])
# def deleteUser(request, username):
#     user = Myuser.objects.get(username=username)
#     user.delete()
#     return Response('Item Successfully Deleted')

# @api_view(['GET'])
# def apiOverview(request):
#     api_urls = {
#         'isVerified': True,
#     }
#     return Response(api_urls)


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


def sendEmail(request, recepient, resend=False, username=None):
    socket.getaddrinfo('localhost', 8000)
    fromaddr = settings.EMAIL_HOST_USER
    toaddr = recepient
    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.connect("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromaddr, varA)
    if(resend):

        link = 'http://127.0.0.1:8000/verify/' + \
            username + '/' + str(date.today())
        # myuser=Myuser.objects.get(username=username)
        # myuser.active_link=link
        # myuser.save()
        text = 'hello  '+username+'  please Verify your account here  ' + link
        subject = 'Animal Care Center Site 2022 By ITI  , ' + \
            username
        mailtext = 'subject : ' + subject+'\n\n'+text
        server.sendmail(fromaddr, toaddr, mailtext)
        server.quit()
        return True
    link = 'http://127.0.0.1:8000/verify/' + \
        username + '/'+str(date.today())
    # myuser=Myuser.objects.get(username=req.POST['username'])
    # myuser.active_link=link
    # myuser.save()
    text = 'hello '+username + \
        '  please Verify your account from here  '+link
    subject = 'Animal Care Center Site 2022 By ITI , '+username
    mailtext = 'subject : ' + subject + '\n\n' + text
    server.sendmail(fromaddr, toaddr, mailtext)
    server.quit()


def sendEmailVet(request, recepient, resend=False, username=None):

    socket.getaddrinfo('localhost', 8000)
    fromaddr = settings.EMAIL_HOST_USER
    toaddr = recepient
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.connect("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromaddr, varA)
    if(resend):

        link = 'http://127.0.0.1:8000/verifyVet/' + \
            username + '/' + str(date.today())
        # myuser=Myuser.objects.get(username=username)
        # myuser.active_link=link
        # myuser.save()
        text = 'hello  '+username+'  please Verify your account here  ' + link
        subject = 'Animal Care Center Site 2022 By ITI  , ' + \
            username
        mailtext = 'subject : ' + subject+'\n\n'+text
        server.sendmail(fromaddr, toaddr, mailtext)
        server.quit()
        return True
    link = 'http://127.0.0.1:8000/verifyVet/' + \
        username + '/'+str(date.today())
    # myuser=Myuser.objects.get(username=req.POST['username'])
    # myuser.active_link=link
    # myuser.save()
    text = 'hello '+username + \
        '  please Verify your account from here  '+link
    subject = 'Animal Care Center Site 2022 By ITI , '+username
    mailtext = 'subject : ' + subject + '\n\n' + text
    server.sendmail(fromaddr, toaddr, mailtext)
    server.quit()


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
