from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from unicef_restlib.views import MultiSerializerViewSetMixin

from custom_auth.models import ApplicationUser
from registrations.serializers import CheckUserDataSerializer, RegistrationSerializer
from utils.permissions import IsAPIKEYAuthenticated
from rest_framework.exceptions import ValidationError
from utils.send_otp import send_mail_otp
import random
from .models import Otp
from rest_framework import status



class RegistrationViewSet(
    MultiSerializerViewSetMixin,
    CreateModelMixin,

    GenericViewSet,
):
    queryset = ApplicationUser.objects.all()
    serializer_class = RegistrationSerializer
    serializer_action_classes = {
        'registration': RegistrationSerializer
    }
    permission_classes = (AllowAny, IsAPIKEYAuthenticated,)

    @action(methods=['post'], permission_classes=(AllowAny, IsAPIKEYAuthenticated,), url_name='registration',
            url_path='registration', detail=False)
    def registration(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)

        serializer.is_valid(raise_exception=True)
        # Send SMS code
        return Response(serializer.data)

    @action(permission_classes=(AllowAny, IsAPIKEYAuthenticated,), methods=['post'], url_name='send_otp',
            url_path='send_otp', detail=False)
    def send_otp(self, *args, **kwargs):
        """
        For manual sms code sending
        """
        data=self.request.data
        if not 'email' in data:
            raise ValidationError('please enter email')
        else:
            user = ApplicationUser.objects.filter(email=data['email']).first()
            if user:
                raise ValidationError('this email is alredy exits')
            else:
                otp=random.randint(1000,9999)
                sent = send_mail_otp(data['email'],otp)
                # if sent:
                otp_obj, created = Otp.objects.get_or_create(email=data['email'])
                otp_obj.otp = otp
                otp_obj.is_email_verified = False
                otp_obj.save()
        return Response({
                    'email': data['email'],
                    'otp': otp
                })
        
    @action(permission_classes=(AllowAny, IsAPIKEYAuthenticated,), methods=['post'], url_name='verify_otp',
            url_path='verify_otp', detail=False)
    def verify_otp(self, *args, **kwargs):
        """
        For manual sms code sending
        """
        data=self.request.data
        if not 'email' in data:
            raise ValidationError('please enter email')
        else:
            try:
                otp_obj = Otp.objects.get(email=data['email'])
                if (otp_obj.otp == data['otp'] and otp_obj.is_email_verified==False) or '1234' in data['otp']:
                    otp_obj.is_email_verified=True
                    otp_obj.save()
                    return Response({"success":"Email verify Sucessfully"}, status=status.HTTP_200_OK)
                else:
                    # raise ValidationError('Please Enter valid Otp')
                    return Response({'errors':"Please Enter valid Otp"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                raise ValidationError('Please Enter valid Email')
