from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from todo.utils.sql_connection import *
import datetime

@csrf_exempt
def create_new_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
                
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            
            
            connect()
            user = check_user_exist(first_name, last_name)
            print("User", user)
            
            if check_user_exist is None:
                populate_user_table(first_name, last_name)
                response_data = {
                    'received_first_name': first_name,
                    'received_last_name': last_name,
                    'status': 'success'
                }
                return JsonResponse(response_data)
            else:
                response_data = {
                    'error': "User already exist",
                }
                return JsonResponse(response_data, status=200)
    
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

@csrf_exempt
def create_todo_list(request):
    if request.method == 'POST':
        try:
            time_completed = datetime.datetime.now()
            
            print( "Datetime", time_completed)
            data = json.loads(request.body)
            
            description = data.get('description')
            complete = data.get('complete')
            incomplete = data.get('incomplete')
            userId = data.get('userId')
            
            connect()
            populate_todo_table(description, complete, incomplete, time_completed, userId)
            response_data = {
                'message': "Todo successfully added",
            }
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
@csrf_exempt
def update_todo_list(request):
    if request.method == 'PUT':
        try:
            time_completed = datetime.datetime.now()
            
            print( "Datetime", time_completed)
            data = json.loads(request.body)
            
            id = data.get('id')
            description = data.get('description')
            complete = data.get('complete')
            incomplete = data.get('incomplete')
            userId = data.get('userId')
            
            connect()
            update_todo_table(id, description, complete, incomplete, time_completed, userId)
            response_data = {
                'message': "Todo successfully updated",
            }
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
@csrf_exempt
def delete_todo(request):
    if request.method == 'DELETE':
        try:
            time_completed = datetime.datetime.now()
            
            print( "Datetime", time_completed)
            data = json.loads(request.body)
            
            id = data.get('id')
            description = data.get('description')
            complete = data.get('complete')
            incomplete = data.get('incomplete')
            userId = data.get('userId')
            
            connect()
            delete_todo_table(id)
            response_data = {
                'message': "Todo successfully deleted",
            }
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)