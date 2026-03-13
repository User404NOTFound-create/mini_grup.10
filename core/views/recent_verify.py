import random
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from core.models.auth_models import User, VerifivationCode
from rest_framework.exceptions import AuthenticationFailed

class ResentVerifyCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        if not email:
            raise AuthenticationFailed("Email kiritilishi shart")

        user = User.objects.filter(email=email).first()

        if not user:
            raise AuthenticationFailed("bunday email bilan foydalanuvchi to'pilmadi ")

        if user.is_active:
            return Response({
                "message": "foydalanuvchi allaqachon tasdiqlangan"
            }, status=400)

        new_code = str(random.randint(100000, 999999))

        verification_record, created = VerifivationCode.objects.get_or_create(user=user)
        verification_record.code = new_code
        verification_record.created_at = timezone.now()
        verification_record.save()

        try:
            send_mail(
                subject="yangi tasdiqlash kodi:",
                message=f"Assalomu Aleykum {user.fullname}, sizning\n yangi tasdiqlash kodingiz -> {new_code}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False
            ),
            return Response({
                "message": "yangi tasdiqlash kod emailga yuborildi"
            })
        except Exception as e:
            return Response({
                        "error": f"Email yuborishda xatolik yuz berdi: {str(e)}"
                    }, status=500)
