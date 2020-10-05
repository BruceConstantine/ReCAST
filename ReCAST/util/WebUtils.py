import hashlib

def getRouter(url_fullpath):
    parts = url_fullpath.split('/')
    i_upbound = len(parts) - 1
    i = 0
    for part in parts:
        if part.endswith('8000') and i < i_upbound:
            return parts[i + 1]
        else:
            i += 1
    return None;

def getTaskAtSession(request):
    task = request.session.get("task")
    print("in function getTaskAtSession(request): task = ")
    print(task)
    if task == None:
        task = {}
    return task

def get_hashDigest_0x(password):
    h = hashlib.md5()
    h.update(password.encode('utf-8'))
    return h.hexdigest()

