from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from artseenapi.models import Artist, City, Manager, Gallery, Viewer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a author

    Method arguments:
      request -- The full HTTP request object
    '''
    username = request.data['username']
    password = request.data['password']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    authenticated_user = authenticate(username=username, password=password)

    # If authentication was successful, respond with their token
    if authenticated_user is not None:
        try:
            artist = Artist.objects.get(user=authenticated_user)
            permissions = 'artist'
        except Artist.DoesNotExist:
            pass

        try:
            viewer = Viewer.objects.get(user=authenticated_user)
            permissions = 'viewer'
        except Viewer.DoesNotExist:
            pass

        try:
            manager = Manager.objects.get(user=authenticated_user)
            permissions = 'manager'
        except Manager.DoesNotExist:
            pass
                
    
        token = Token.objects.get(user=authenticated_user)
        data = {
            'valid': True,
            'token': token.key,
            'permissions': permissions
        }
        return Response(data)
    
    else:
        # Bad login details were provided. So we can't log the user in.
        data = {'valid': False}
        return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new author for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
        username=request.data['username'],
        email=request.data['email'],
        password=request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name']
    )

    city = City.objects.get(pk=request.data['city_id'])

    if 'artist' in request.query_params:
        artist = Artist.objects.create(
            bio=request.data['bio'],
            image_url=request.data['image_url'],
            user=new_user,
            city=city,
            phone_number=request.data['phone'],
            website=request.data['website']
        )
        token = Token.objects.create(user=artist.user)
        permissions = 'artist'

    elif 'viewer' in request.query_params:
        viewer = Viewer.objects.create(
            user=new_user,
            city=city,
            phone_number=request.data['phone']
        )
        token = Token.objects.create(user=viewer.user)
        permissions = 'viewer'

    elif 'manager' in request.query_params:
        gallery = Gallery.objects.get(pk=request.data['gallery_id'])
    
        manager = Manager.objects.create(
            user=new_user,
            city=city,
            gallery=gallery,
            phone_number=request.data['phone']
        )
        token = Token.objects.create(user=manager.user)
        permissions = 'manager'

    data = {'token': token.key, 'permissions': permissions}
    return Response(data)
