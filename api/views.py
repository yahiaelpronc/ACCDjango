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
from django.db.models import Q, Count
from datetime import datetime, timedelta
from django.shortcuts import redirect


@api_view(['DELETE'])
def deleteNotifications(request, username, type):
    Notifications.objects.filter(receiver=username, type=type).delete()
    return Response('Notifications Successfully Deleted')


@api_view(['POST'])
def insertNotifications(request):
    mydata = NotificationsSerializer(data=request.data)
    if(mydata.is_valid()):
        mydata.save()
        return Response(mydata.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def countNotifications(request, username):
    notifications = Notifications.objects.filter(receiver=username)
    if(notifications):
        mydata = NotificationsSerializer(notifications, many=True)
        return Response(mydata.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def insertServiceRequest(request):
    if(request.data['AnimalType'] == ""):
        return Response("Please Choose Animal Type")
    if(request.data['timePeriod'] == ""):
        return Response("Please Choose Time Period")
    mydata = ServiseRequestSerializer(data=request.data)
    if(mydata.is_valid()):
        mydata.save()
        return Response(mydata.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def verify(request, username):
    myUser = Myuser.objects.filter(username=username).exists()
    myVet = Vet.objects.filter(username=username).exists()
    if(myUser):
        myUser = Myuser.objects.get(username=username)
        myUser.active_status = True
        myUser.save()
        return redirect("http://localhost:3000/verified")
    if(myVet):
        myVet = Vet.objects.get(username=username)
        myVet.active_status = True
        myVet.save()
        return redirect("http://localhost:3000/verified")
    return redirect("http://localhost:3000/Notverified")


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
def getAllMessagesAssociated(request, username):
    Message = Messages.objects.filter(
        Q(sender=username) | Q(receiver=username)).values()
    Message = MessagesSerializer(Message, many=True)
    return Response(Message.data)


@api_view(['GET'])
def getAllMessages(request, sender, receiver):
    # user = Myuser.objects.get(username=request.session['username'])
    # vet = Vet.objects.get(username=request.session['vet_username'])
    if(Myuser.objects.filter(username=sender).exists()):
        user = Myuser.objects.get(username=sender)
        user2 = Vet.objects.get(username=receiver)
    else:
        user = Vet.objects.get(username=sender)
        user2 = Myuser.objects.get(username=receiver)
    Message = Messages.objects.filter(
        Q(sender=user2.username) | Q(sender=user.username), Q(receiver=user2.username) | Q(receiver=user.username)).values()
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
        return Response("Email Sent")
    if(myVet):
        myVet = Vet.objects.get(username=username)
        recepient = myVet.email
        sendEmail(request, recepient, resend=True, username=myVet.username)
        return Response("Email Sent")
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
        if(myVet.active_status == False):
            return Response("Please Activate Your Account")
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
        if(myuser.active_status == False):
            return Response("Please Activate Your Account")
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
def findSpecificAnimal(request, animalName):
    myanimal = Animal.objects.get(
        animalName=animalName)
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

# get request By User And Animal And Vet


@api_view(['GET'])
def getRequestByUserAndAnimalAndVet(request, user, animalName, vetname):
    myrequest = SurgicalOperationsRequest.objects.get(
        user=user, animalName=animalName, vetName=vetname)
    if(myrequest != None):
        mydata = SurgicalOperationsRequestSerializer(myrequest)
        print(mydata.data)
        return Response(mydata.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# get Requests related to username


@api_view(['GET'])
def getRequestByUsername(request, user):
    myrequests = SurgicalOperationsRequest.objects.filter(user=user)
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

# get all Services Responses depend on user  name


@api_view(['GET'])
def getServicesResponses(request, username):
    myrequests = ServiseRequest.objects.filter(animalOwner=username)
    if(len(myrequests) != 0):
        mydata = ServiseRequestSerializer(myrequests, many=True)
        print(mydata.data)
        return Response(mydata.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

# get surgical operations Resposes for user by animal owner


@api_view(['GET'])
def getSurgicalOperations(request, owner):
    myResponses = SurgicalOperations.objects.filter(owner=owner)
    myResponses2 = []
    myResponses3 = []
    x=1
    for i in myResponses:
        print(x)
        x=x+1
        if((i.date != None)):
            thisdate = i.date
            mydate = datetime.now()
            myyear = mydate.year
            mymonth = mydate.month
            myday = mydate.day
            thisyear = thisdate.split("-")[0]
            thismonth = thisdate.split("-")[1]
            thisday = thisdate.split("-")[2]
            yearDiff = int(thisyear)-myyear
            monthDiff = int(thismonth)-mymonth
            dayDiff = int(thisday)-myday
            if(yearDiff > 0 or (yearDiff == 0 and monthDiff > 0) or (monthDiff == 0 and dayDiff > 0)):
                myResponses2.append(i)

            for ele in myResponses:
                if ele not in myResponses2:
                    myResponses3.append(ele)
        else:
            myResponses2.append(i)

    if(len(myResponses2) != 0):
        mydata = SurgicalOperationsSerializer(myResponses2, many=True)

        print(len(myResponses2))
        return Response(mydata.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def getSurgicalResponses(request, owner):
    myResponses = SurgicalOperationsRequest.objects.filter(user=owner)
    if(len(myResponses) != 0):
        mydata = SurgicalOperationsRequestSerializer(myResponses, many=True)
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


# update status user of surgery Operation by id
@api_view(['POST'])
def updateOperationStatusUser(request, id):
    mydate = datetime.now()
    myyear = mydate.year
    mymonth = mydate.month
    myday = mydate.day
    task = SurgicalOperations.objects.get(id=id)
    thisdate = task.date
    if(thisdate == None):
        serializer = SurOprationStatusUserSerializer(
        instance=task, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
        return Response(serializer.data)

    else:

        if(len(thisdate) > 5):
            thisyear = thisdate.split("-")[0]
            thismonth = thisdate.split("-")[1]
            thisday = thisdate.split("-")[2]
            yearDiff = int(thisyear)-myyear
            monthDiff = int(thismonth)-mymonth
            dayDiff = int(thisday)-myday
            if(yearDiff <= 0 and monthDiff <= 0 and dayDiff <= 1):
                print("errrrrrrrror")
                return Response("you cant decline before 24 hours")
            serializer = SurOprationStatusUserSerializer(
            instance=task, data=request.data)
            if(serializer.is_valid()):
                serializer.save()
            return Response(serializer.data)
            



# update status vet of surgery Operation by id
@api_view(['POST'])
def updateOperationStatusVet(request, id):
    mydate = datetime.now()
    myyear = mydate.year
    mymonth = mydate.month
    myday = mydate.day
    task = SurgicalOperations.objects.get(id=id)
    thisdate = task.date
    if(thisdate == None):
        serializer = SurOperationStatusVetSerializer(
            instance=task, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
        return Response(serializer.data)
    else:
        thisyear = thisdate.split("-")[0]
        thismonth = thisdate.split("-")[1]
        thisday = thisdate.split("-")[2]

        yearDiff = int(thisyear)-myyear
        monthDiff = int(thismonth)-mymonth
        dayDiff = int(thisday)-myday
        print("here is ",yearDiff,",",monthDiff,",",dayDiff)
        if(yearDiff <= 0 and monthDiff <= 0 and dayDiff <= 1):
            print("errrrrrrrror")
            return Response("you cant decline before 24 hours")
        else:

            serializer = SurOperationStatusVetSerializer(
                instance=task, data=request.data)
            if(serializer.is_valid()):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)




@api_view(['POST'])
def updateRequestStatusVet(request, id):
    task = SurgicalOperationsRequest.objects.get(id=id)
    serializer = SurRequestStatusVetSerializer(
        instance=task, data=request.data)
    if(serializer.is_valid()):
        serializer.save()
    return Response(serializer.data)


# update status service Request for User
    #     return Response(serializer.data)
    # api_response = {
    #     'isOnline': True,
    # }
    # return Response(api_response)

@api_view(['POST'])
def updateSrviceStatusUser(request, id):
    task = ServiseRequest.objects.get(id=id)
    serializer = ServiceStatusUserSerializer(
        instance=task, data=request.data)
    if(serializer.is_valid()):
        serializer.save()
    return Response(serializer.data)


# update status service Request for Owner
@api_view(['POST'])
def updateSrviceStatusOwner(request, id):

    task = ServiseRequest.objects.get(id=id)
    serializer = ServiceStatusOwnerSerializer(
        instance=task, data=request.data)
    if(serializer.is_valid()):
        serializer.save()
    return Response(serializer.data)


# updates of vet data about Surgery
@api_view(['POST'])
def SurVetUpdates(request, id):
    mySurgery = SurgicalOperations.objects.get(id=id)
    serializer = SurOperationVetUpdatesSerializer(
        instance=mySurgery, data=request.data)
    if(serializer.is_valid()):
        serializer.save()
    return Response(serializer.data)


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

# find surgery using id


@api_view(['GET'])
def findSurgery(request, id):
    mysurgery = SurgicalOperations.objects.get(id=id)
    if(mysurgery != None):
        mydata = SurgicalOperationsSerializer(mysurgery)
        return Response(mydata.data)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


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
    print(mySurgeries)
    myResponses2 = []
    myResponses3 = []
    for i in mySurgeries:
        print("0")
        if((i.date != None) and (len(i.date) > 5)):
            print("1")
            thisdate = i.date
            mydate = datetime.now()
            myyear = mydate.year
            mymonth = mydate.month
            myday = mydate.day
            thisyear = thisdate.split("-")[0]
            thismonth = thisdate.split("-")[1]
            thisday = thisdate.split("-")[2]
            yearDiff = int(thisyear)-myyear
            monthDiff = int(thismonth)-mymonth
            dayDiff = int(thisday)-myday
            if(yearDiff > 0 or (yearDiff == 0 and monthDiff > 0) or (monthDiff == 0 and dayDiff > 0)):
                myResponses2.append(i)

            for ele in mySurgeries:
                print("2")
                if ele not in myResponses2:
                    print("3")
                    myResponses3.append(ele)
        else:
            myResponses2.append(i)
    print("4")
    if(len(myResponses2) != 0):
        mydata = SurgicalOperationsSerializer(myResponses2, many=True)
        print(mydata.data)
        return Response(mydata.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# Add Location
@api_view(['POST'])
def insertLocation(request, type):
    print(request.data)
    if(request.data['work_hours_start'] == ""
       or request.data['work_hours_end_period'] == ""
       or request.data['work_hours_start_period'] == ""
       or request.data['work_hours_start'] == ""):
        return Response("Please Choose Work Hours")
    if(type == "default"):
        return Response("Please Choose An Owner Type")
    if(request.data['governorate'] == ""):
        return Response("Please Choose A Governorate")
    if(request.data['service'] == ""):
        return Response("Please Choose A Service")
    if(locations.objects.filter(name=request.data['name']).exists()):
        return Response("A Location With This Name Already Exists")
    if(locations.objects.filter(email=request.data['email']).exists()):
        return Response("Email Already Exists")
    mydata = LocationsSerializer(data=request.data)
    if(type == "user"):
        if(mydata.is_valid()):
            mydata.save()
            myUser = Myuser.objects.get(username=request.data['owner'])
            myUser.isOwner = True
            myUser.save()
            print(mydata.data)
            return Response(mydata.data)
    else:
        if(mydata.is_valid()):
            mydata.save()
            myUser = Vet.objects.get(username=request.data['owner'])
            myUser.isOwner = True
            myUser.save()
            print(mydata.data)
            return Response(mydata.data)
    return Response(status=status.HTTP_404_NOT_FOUND)


# register user
@api_view(['POST'])
def insertuser(request):
    print("------------------API--------------------")
    mydata = UsersSerializer(data=request.data)
    if(Myuser.objects.filter(username=request.data['username']).exists()):
        return Response("Username Already Exists")
    if(Myuser.objects.filter(email=request.data['email']).exists()):
        return Response("Email Already Exists")
    if(request.data['governorate'] == ""):
        return Response("Please Choose A Governorate")
    if(mydata.is_valid()):
        recepient = request.data['email']
        if(sendEmail(request, recepient, resend=False, username=request.data['username'])):
            mydata.save()
            return Response(mydata.data)
        return Response("Email Not Valid")
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
        recepient = request.data['email']
        if(sendEmail(request, recepient, resend=False, username=request.data['username'])):
            mydata.save()
            return Response(mydata.data)
        return Response("Email Not Valid")
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# 1 - get all location
@api_view(['GET'])
def listservices(request):
    mylocations = ServiseRequest.objects.all()
    locationdata = ServiseRequestSerializer(mylocations, many=True)
    return Response(locationdata.data)


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
    if(Vet.objects.filter(username=username).exists()):
        myvet = Vet.objects.get(username=username)
        mydata = VetSerializer(myvet)
        return Response(mydata.data)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


def sendEmail(request, recepient, resend=False, username=None):
    socket.getaddrinfo('localhost', 8000)
    fromaddr = settings.EMAIL_HOST_USER
    toaddr = recepient
    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.connect("smtp.gmail.com", 587)
    print("CONNECTED")
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromaddr, varA)
    print("LOGGED IN")
    if(resend):

        link = 'http://localhost:8000/api/verify/' + \
            username + '/'
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
    link = 'http://localhost:8000/api/verify/' + \
        username + '/'
    # myuser=Myuser.objects.get(username=req.POST['username'])
    # myuser.active_link=link
    # myuser.save()
    text = 'hello '+username + \
        '  please Verify your account from here  '+link
    subject = 'Animal Care Center Site 2022 By ITI , '+username
    mailtext = 'subject : ' + subject + '\n\n' + text
    print("BEFORE SEND")
    server.sendmail(fromaddr, toaddr, mailtext)
    print("AFTER SEND")
    server.quit()
    print("Quit")
    return True


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

        link = 'http://localhost:8000/api/verifyVet/' + \
            username + '/'
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
    link = 'http://localhost:8000/api/verifyVet/' + \
        username + '/'
    # myuser=Myuser.objects.get(username=req.POST['username'])
    # myuser.active_link=link
    # myuser.save()
    text = 'hello '+username + \
        '  please Verify your account from here  '+link
    subject = 'Animal Care Center Site 2022 By ITI , '+username
    mailtext = 'subject : ' + subject + '\n\n' + text
    server.sendmail(fromaddr, toaddr, mailtext)
    server.quit()
