from django.shortcuts import render
from .models import Student
from .filters import StudentFilter
from home.views import paginate
from datetime import datetime
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from urllib.parse import urlencode
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import requests
import logging
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentSerializer

import environ

env = environ.Env()
environ.Env.read_env()


ybi_moodle_api_token= env('ybi_moodle_api_token')
bbi_moodle_api_token= env('bbi_moodle_api_token')
lrh_moodle_api_token= env('lrh_moodle_api_token')

# Get an instance of a logger
logger = logging.getLogger(__name__)

def studentmgtview(request):

    f = StudentFilter(request.GET, queryset=Student.objects.all())


    paginator,current_page,is_paginated,Items = paginate(f.qs,request,50,1)

    context = {
        'current_page': current_page,
        'is_paginated': is_paginated,
        'paginator': paginator,
        "Items": Items,
        'filter': f,
    }

    return render(request, "aduser/adusermgt.html", context)

def changecomputerpwview(request, samaccountname, password):

    url = "http://10.0.0.30:5000/change_user_password"
    headers = {"Content-Type": "application/json"}
    data = {
        "username": samaccountname,
        "password": password
    }

    response = requests.post(url, headers=headers, json=data)

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    context = {
        "result": "Password for user " + samaccountname + " has been changed to " + password
    }

    return render(request, "aduser/result.html", context)

@api_view(['POST'])
def receive_json(request):
    print(request.data)  
    
    receive_name = request.data.get('name')
    # Get all student names from the database
    student_names = Student.objects.values_list('name', flat=True)
    
    # Check if the received name already exists
    if receive_name in student_names:
        return Response({'message': 'Student already exists'}, status=200)

    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            # This block will not typically catch validation errors from serializer.save()
            # They are caught in serializer.is_valid() check.
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    # This block handles the validation errors from serializer.is_valid()
    print(serializer.errors)
    if 'student with this name already exists' in str(serializer.errors):
        return Response({'log': 'Student with this name already exists.'}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

import requests
from django.http import JsonResponse
from .models import Student


@api_view(['GET'])
def create_students_in_ad(request):
    # Step 1: Fetch students with is_in_AD = "n"
    students = Student.objects.filter(is_in_AD='n')

    if not students.exists():
        return JsonResponse({"message": "No students found to create in AD."}, status=404)
    # Step 2: Prepare the list to store results
    results = []

    # Step 3: Iterate over the students and call the API
    for student in students:
        payload = {
            "name": student.name,
            "path": student.path,
            "givenName": student.givenname,
            "surname": student.surname,
            "samAccountName": student.samaccountname,
            "displayName": student.displayname,
            "password": student.password
        }

        try:
            # Step 4: Send the data to the external API
            response = requests.post('http://10.0.0.30:5000/create_user', json=payload)

            if response.status_code == 200:
                if "User created successfully" not in response.text and "User already exists" not in response.text:
                    # Add the result to the list
                    results.append({
                        "id": student.id,
                        "name": student.name,
                        "status": "Failed",  # You may want to indicate failure here
                        "api_response": response.text
                    })
                else:
                    # If successful (and no failure message in response text)
                    student.is_in_AD = 'y'
                    student.save()

                    # Add the result to the list
                    results.append({
                        "id": student.id,
                        "name": student.name,
                        "status": "Created",
                        "api_response": response.json()
                    })

        except requests.RequestException as e:
            # Handle exceptions such as network errors
            results.append({
                "id": student.id,
                "name": student.name,
                "status": "Error",
                "error": str(e)
            })

    # Step 5: Return the results as a JSON response
    return JsonResponse({"results": results})


@api_view(['GET'])
def create_students_in_moodle(request):
 
    # Fetch students with is_in_Elearning = 'n'
    students = Student.objects.filter(is_in_Elearning='n')
    results = []
    
    if not students.exists():
        return JsonResponse({"message": "No students found to create in Moodle."}, status=404)

    # Prepare users data for Moodle API
    for student in students:
        moodle_url = ""
        api_token = ""
        username = ""
        password = ""

        if student.campus == 'YBI':
            moodle_url = "https://elearning.york.edu.au/webservice/rest/server.php"
            api_token = ybi_moodle_api_token
            username = student.samaccountname[3:]
            password = student.password[3:]
        elif student.campus == 'BBI': 
            moodle_url = "https://elearning.berkeley.nsw.edu.au/webservice/rest/server.php"
            api_token = bbi_moodle_api_token
            username = student.samaccountname[:3].lower() + student.samaccountname[3:]
            password = student.password[3:]
        elif student.campus == 'LRH': 
            moodle_url = "https://elearning.lerosey.edu.au/webservice/rest/server.php"
            api_token = lrh_moodle_api_token
            username = student.samaccountname[:3].lower() + student.samaccountname[3:]
            password = student.password

        payload = {
        "wstoken": api_token,
        "wsfunction": "core_user_create_users",
        "moodlewsrestformat": "json",
        "users[0][username]": username,
        "users[0][password]": password,
        "users[0][firstname]": student.givenname,
        "users[0][lastname]": student.surname,
        "users[0][email]": student.email
        }

        try:
            # Send the POST request to Moodle API
            response = requests.post(moodle_url, data=payload)

            # Check the response from Moodle API
            if response.status_code == 200:
                # Parse the XML response
                print(response.text)
                student.is_in_Elearning = 'y'
                student.save()


                if "username" in response.text:
                    # Update the students' is_in_Elearning status to 'y'
                    
                    # Return success response with data
                    results.append({
                        "name": username,
                        "status": "Success",  # You may want to indicate failure here
                        "Students created successfully in Moodle": response.text
                    })
                else:
                    results.append({
                        "name": username,
                        "status": "Ignore",  # You may want to indicate failure here
                        "user exists, Don't need to create students in Moodle": response.text
                    })

            else:
                return JsonResponse({"error": "Failed to create users in Moodle.", "response": response.text}, status=response.status_code)

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"results": results})

# Change Moodle User password

def get_user_by_username(request, moodle_url, api_token, username, samaccountname):

    data = {
        'wstoken': api_token,
        'wsfunction': 'core_user_get_users',
        'moodlewsrestformat': 'json',
        'criteria[0][key]': 'username',
        'criteria[0][value]': username
    }
    user_id = ""
    try:
        response = requests.post(moodle_url, data=data)
        result = response.json()

        if not result['users']:
            print("samaccountname is not in Moodle, will create it")
            re = create_students_in_moodle_by_username(moodle_url, api_token,samaccountname)
            print("re", re)
            user_id = re[0]["id"]
            print("new",user_id)
        else:
            user_id = result['users'][0]['id']
        return user_id

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

def change_moodle_user_password(request, campus, samaccountname, password):

    moodle_url = ""
    api_token = ""
    username = ""
    new_password = ""

    if campus == 'YBI':
        moodle_url = "https://elearning.york.edu.au/webservice/rest/server.php"
        api_token = ybi_moodle_api_token
        username = samaccountname[3:]
        new_password = password[3:]
    elif campus == 'BBI': 
        moodle_url = "https://elearning.berkeley.nsw.edu.au/webservice/rest/server.php"
        api_token = bbi_moodle_api_token
        username = samaccountname[:3].lower() + samaccountname[3:]
        new_password = password[3:]
    elif campus == 'LRH': 
        moodle_url = "https://elearning.lerosey.edu.au/webservice/rest/server.php"
        api_token = lrh_moodle_api_token
        username = samaccountname[:3].lower() + samaccountname[3:]
        new_password = password
    
    # Get the user ID by username
    user_id = get_user_by_username(request, moodle_url, api_token, username, samaccountname)
    
    print("user_id:", user_id)
    if not user_id:
        return JsonResponse({"message": "No students found to create in Moodle."}, status=404)

    data = {
        'wstoken': api_token,
        'wsfunction': 'core_user_update_users',
        'moodlewsrestformat': 'json',
        'users[0][id]': user_id,
        'users[0][password]': new_password
    }

    try:
        
        # Send the request to the Moodle API
        response = requests.post(moodle_url, data=data)
        
        # Parse the JSON response
        if response.status_code == 200:
            context = {
            "result": "Password for user " + username + " has been changed to " + new_password
                }

            return render(request, "aduser/result.html", context)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)


def create_students_in_moodle_by_username(moodle_url, api_token,samaccountname):
 
    # Fetch students with is_in_Elearning = 'n'
    students = Student.objects.filter(samaccountname=samaccountname)
    
    if not students.exists():
        return JsonResponse({"message": "No students found to create in Moodle."}, status=404)

    # Prepare users data for Moodle API
    for student in students:
        username = ""
        password = ""

        if student.campus == 'YBI':
            username = student.samaccountname[3:]
            password = student.password[3:]
        elif student.campus == 'BBI': 
            username = student.samaccountname[:3].lower() + student.samaccountname[3:]
            password = student.password[3:]
        elif student.campus == 'LRH': 
            username = student.samaccountname[:3].lower() + student.samaccountname[3:]
            password = student.password

        payload = {
        "wstoken": api_token,
        "wsfunction": "core_user_create_users",
        "moodlewsrestformat": "json",
        "users[0][username]": username,
        "users[0][password]": password,
        "users[0][firstname]": student.givenname,
        "users[0][lastname]": student.surname,
        "users[0][email]": student.email
        }

        try:
            # Send the POST request to Moodle API
            response = requests.post(moodle_url, data=payload)

            # Check the response from Moodle API
            if response.status_code == 200:
                # Parse the XML response
                print(response.text)

                if "username" in response.text:
                    # Return success response with data
                    return json.loads(response.text)
                else:
                    return JsonResponse({"error": "May user exists, failed to create students in Moodle.", "response": response.text}, status=400)

            else:
                return JsonResponse({"error": "Failed to create users in Moodle.", "response": response.text}, status=response.status_code)

        except requests.exceptions.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)
