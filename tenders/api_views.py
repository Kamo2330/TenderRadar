from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AlertPreference, Tender
from .serializers import (
    AlertPreferenceSerializer,
    LoginSerializer,
    TenderSerializer,
    UserSerializer,
)
from .tender_queryset import filter_tenders

User = get_user_model()


class TenderListAPIView(generics.ListAPIView):
    serializer_class = TenderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        params = self.request.query_params
        return filter_tenders(
            q=params.get("q", "").strip(),
            tender_type=params.get("tender_type", "").strip(),
            province=params.get("province", "").strip(),
            source=params.get("source", "").strip(),
            date_filter=params.get("date_filter", "open").strip() or "open",
            sort=params.get("sort", "newest").strip() or "newest",
        )


class TenderDetailAPIView(generics.RetrieveAPIView):
    serializer_class = TenderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Tender.objects.select_related("source").all()


class TenderMetaAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "tender_types": [
                    {"value": value, "label": label}
                    for value, label in Tender.TenderType.choices
                ],
                "provinces": list(
                    Tender.objects.exclude(province="")
                    .values_list("province", flat=True)
                    .distinct()
                    .order_by("province")
                ),
                "sources": [
                    {"slug": slug, "name": name}
                    for slug, name in Tender.objects.values_list(
                        "source__slug", "source__name"
                    )
                    .distinct()
                    .order_by("source__name")
                ],
            }
        )


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if user is None:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user": UserSerializer(user).data,
            }
        )


class LogoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class AlertPreferenceAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = AlertPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        prefs, _ = AlertPreference.objects.get_or_create(user=self.request.user)
        return prefs
