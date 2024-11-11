from django.shortcuts import render

from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import EmailSerializer

class SendEmailView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        
        if serializer.is_valid():
            # Send email using Django's send_mail function
            try:
                send_mail(
                    serializer.validated_data['subject'],
                    serializer.validated_data['message'],
                    'intranet@york.edu.au',  # From email (set your email)
                    [serializer.validated_data['recipient']],
                    fail_silently=False,
                )
                return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
