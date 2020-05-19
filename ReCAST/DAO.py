from ReCAST.models import Task, Config, User, Customer_CMAD, Result

def getMaxID(modelName):
    if modelName == 'Task':
        return Task.objects.last().tid
    elif modelName == 'Customer_CMAD':
        return Customer_CMAD.objects.last().cid
    elif modelName == 'Result':
        return Result.objects.last().rid
    elif modelName == 'Config':
        return Config.objects.last().id

def getUserCount():
    return User.objects.count()