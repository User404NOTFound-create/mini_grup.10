from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        fullname = request.body.get("fullname", None)
        username = request.body.get("username", None)
        age = request.body.get('age', None)
        gender = request.body.get("gender", None)
        role = request.body.get("role", None)

        if None in [fullname, username, age, gender, role]:
            return Response({
                "error": "kerakli, polyalar to'lliq emas"
            }, status=403)

        # user = User.objects.







