from rest_framework.decorators import api_view, APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from home.models import Person
from home.serializers import PersonSerializer, LoginSerializer, RegisterSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.paginator import Paginator
from rest_framework.decorators import action



class Register(APIView):

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response({
                'status' : 'False',
                'message': serializer.errors
                }, status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({
                'status' : 'True',
                'message': 'User created'
                }, status.HTTP_201_CREATED)


class Login(APIView):

    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)

        if not serializer.is_valid():
            return Response({
                'status' : 'False',
                'message': serializer.errors
                }, status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
        if not user:
            return Response({
                'status' : 'False',
                'message': 'Invalid Credential'
                }, status.HTTP_400_BAD_REQUEST)
        
        token,_ =  Token.objects.get_or_create(user=user)
        print(token)
        return Response({
                'status' : 'True',
                'message': 'User Logged in',
                'token': str(token)
                }, status.HTTP_200_OK)

# Create your views here.
@api_view(['GET'])
def index(request):
    courses = {
        'Name' : 'Flutter Development Course',
        'Instructor':'Utsav',
        'Duration': '8hrs',
    }
    return Response(courses)

#Using APIView Class
class PersonAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.user)
        objs = Person.objects.filter(comapny__isnull= False)
        try:
            page = request.GET.get('page',1)
            page_size = 1
            paginator  = Paginator(objs, page_size)
            serializer = PersonSerializer(paginator.page(page), many = True)
        except Exception as e:
            return Response({
                'status' : 'False',
                'message': 'Empty Page'
                }, status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        serializer = PersonSerializer(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def put(self, request):
        data = request.data
        obj=Person.objects.get(id = data['id'])
        serializer = PersonSerializer(obj, data= data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def patch(self, request):
        data = request.data
        obj=Person.objects.get(id = data['id'])
        serializer = PersonSerializer(obj, data= data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def delete(self, request):
        data = request.data
        obj=Person.objects.get(id = data['id'])
        obj.delete()
        return Response({'message':'person deleted'})
    


#Using api_view decorator
@api_view(['GET', 'POST', 'PUT', 'PATCH','DELETE'])
def person(request):
    if request.method=='GET':
        objs = Person.objects.filter(comapny__isnull= False)
        serializer = PersonSerializer(objs, many = True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        data = request.data
        serializer = PersonSerializer(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    elif request.method == 'PUT':
        data = request.data
        obj=Person.objects.get(id = data['id'])
        serializer = PersonSerializer(obj, data= data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    elif request.method == 'PATCH':
        data = request.data
        obj=Person.objects.get(id = data['id'])
        serializer = PersonSerializer(obj, data= data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    else:
        data = request.data
        obj=Person.objects.get(id = data['id'])
        obj.delete()
        return Response({'message':'person deleted'})
    

@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data= data)
    if serializer.is_valid():
        data = serializer.data
        print(data)
        return Response({'message':'User logged in'})
    else:
        return Response(serializer.errors)
    

#Using ViewSets
class PersonViewset(ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

    #used for seraching
    def list(self, request):
        search = request.GET.get('search')
        queryset = self.queryset
        
        if search:
            queryset = queryset.filter(name__startswith=search)
        serializer = PersonSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def send_mail(self, request, pk):
        obj = Person.objects.get(pk = pk)
        serializer = PersonSerializer(obj)
        return Response({
                'status' : 'True',
                'data' : serializer.data}, status.HTTP_200_OK)