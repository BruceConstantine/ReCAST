from django.conf import settings

'''所有的函数必须定义request作为第一个参数'''
'''真正起作用的是返回的key值，而不是函数名！'''
'''鉴于省去tamplate中调用context-object的麻烦，就把函数名和返回的Key值一致！'''
def navbar_paths (request):
    return {
    "navbar_paths": [
        '/createTask/',
        '/config/',
        '/result/',
        '/modify/',
    ]}

def options_paths (request):
    return {
    "options_paths": [
        '/config/',
        '/result/',
        '/modify/',
    ]}

def static_file_dir(request):
    return {'static_file_dir':settings.STATICFILES_DIRS}

