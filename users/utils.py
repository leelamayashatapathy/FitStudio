from rest_framework_simplejwt.tokens import RefreshToken


def generate_token(user):
    refresh_token = RefreshToken.for_user(user)
    return ({
        'access': str(refresh_token.access_token),
        'refresh':str(refresh_token)
    })
    
    
def refresh_access_token(refresh_token):
    try:
        refresh = RefreshToken(refresh_token)
        return {
            'access': str(refresh.access_token)
        }
    except Exception as e:
        raise ValueError("Invalid refresh token")