from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from urllib import parse
from channels.db import database_sync_to_async


# @database_sync_to_async
# def get_user(token_key):
#     try:
#         return Token.objects.get(key=token_key).user
#     except Token.DoesNotExist:
#         return AnonymousUser()

# class TokenAuthMiddleware:
#     """
#     Token authorization middleware for Django Channels 2
#     """

#     def __init__(self, inner):
#         self.inner = inner

#     def __call__(self, scope):
#         headers = dict(scope['headers'])
#         # token = parse(scope['query_string']).decode('utf-8')
#         # print(token)
#         new_scope = dict(scope)
#         print(new_scope)
#         if b'' in new_scope['query_string']:
#             print('normaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaallllllllllllllllllllll')
#         else:
#             print('duuuuuuuuuuuuuuuuuuuuuuuuuummmmmmmmmmmmmmmmmmmmbbbbbbbbbbbbbbbb')
#         if b'' in new_scope['query_string']:
#             print(new_scope['query_string'].decode('utf-8'))
#             token_name, token_key = new_scope['query_string'].decode('utf-8').split('=')
#             print(token_name, token_key)
#             scope['user'] = get_user(token_key)
#             print('not here??!!')
#         return self.inner(scope)

# TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))













@database_sync_to_async
def get_user(token_key):
    try:
        return Token.objects.get(key=token_key).user
    except Token.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    see:
    https://channels.readthedocs.io/en/latest/topics/authentication.html#custom-authentication
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)


class TokenAuthMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        # headers = dict(self.scope['headers'])
        new_scope = dict(self.scope)
        if b'' in new_scope['query_string']:
            print(new_scope['query_string'].decode('utf-8'))
            token_name, token_key = new_scope['query_string'].decode('utf-8').split('=')
            print(token_name, token_key)
            self.scope['user'] = await get_user(token_key)
        inner = self.inner(self.scope)
        return await inner(receive, send) 


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))


