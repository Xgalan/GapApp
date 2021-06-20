from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests


@api_view(['GET',])
def delivers_by_partnumber(request):
    r = requests.get('http://127.0.0.1:8001/AME/AME_2021.json')
    return Response({"objects": r.json()})
