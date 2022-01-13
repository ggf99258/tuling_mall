from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from tuling_malls import settings
def jiami(user_id):
    tocker=Serializer(secret_key=settings.SECRET_KEY,expires_in=3600*24)
    data=tocker.dumps({'user_id':user_id})
    return data.decode()
def jiemi(tocker):
    tockers = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600 * 24)
    try:
        data=tockers.loads(tocker)
    except:
        return None
    return data.get('user_id')