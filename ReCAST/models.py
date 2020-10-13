from django.db import models
# Create your models here.

class Config(models.Model):
    MBS = models.TextField(null=True)   # Min. Buffer Stock Stringfied value: '100000,1000,...'
    RBS = models.TextField(null=True)   # Reserved. Buffer Stock Stringfied value: '100000,1000,...'
    PGL = models.TextField(null=True)   # Possible Loss or Gain Stringfied value: '100000,1000,...'
    VulATP = models.TextField(null=True)   # VulnerableATP (if applied) Stringfied value: 'True,False,...'

class Task(models.Model):
    tid = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='tid')
    # The ID of Task not need to be created here, as ORM framework can maintain id automatically
    # Task descriptions
    taskName = models.CharField(max_length=32, default='ReCAST Task')
    taskDescription = models.CharField(max_length=128, default='')
    # Time Stamp for creating this task.
    date = models.DateTimeField(auto_now_add=True)

    # No ".html" added into DB, we need to take it from DB and add the extension in code.
    currentPage = models.CharField(max_length=32, default='createTask')
    # RLC's Username
    username = models.CharField(max_length=32,null=True)

    #Product ID
    pid = models.CharField(max_length=32,null=True)

    CW_start = models.IntegerField(null=True)
    CW_end = models.IntegerField(null=True)
    enableRub = models.BooleanField(null=True)
    # This is a big string for stroing all vlaues of plant ATP
    plantATP = models.TextField(null=True)
    ATP_NTA = models.IntegerField(null=True)
    maxDelay = models.IntegerField(null=True)
    packingUnit = models.IntegerField(null=True)

    #The rid of result scenario. aka. Target allocation which selected by RLC's final decision
    TA_rid = models.IntegerField(null=True)
    # Reference to Config table 使用ForeignKey扩展Task表
    cid = models.IntegerField(null=True) #ForeignKey(Config,on_delete=models.CASCADE, null=True)

    def getDict(self):
        return {
            "tid": self.tid,
            "taskName": self.taskName,
            "taskDescription": self.taskDescription,
            "date": self.date,
            "currentPage": self.currentPage,
            "username": self.username,
            "pid": self.pid,
            "CW_start": self.CW_start,
            "CW_end": self.CW_end,
            "enableRub": self.enableRub,
            "plantATP": self.plantATP,
            "ATP_NTA": self.ATP_NTA,
            "maxDelay": self.maxDelay,
            "packingUnit": self.packingUnit,

            # The rid of result scenario. aka. Target allocation which selected by RLC's final decision
            "TA_rid": self.TA_rid,
            # Reference to Config table 使用ForeignKey扩展Task表
            "cid": self.cid
        };
    def __str__(self):
        return str( self.getDict() );

class Customer_CMAD(models.Model):
    cid = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='cid')
    #reference to task id
    tid = models.IntegerField() #ForeignKey(Task.tid,on_delete=models.CASCADE)
    #Not Nullable as name is essential
    customerName = models.CharField(max_length=32)
    #Allowance of Using ATP 'True,False,...'
    allowList = models.TextField(null=True)
    #Same as allowList
    valueList = models.TextField(null=True)

class Result(models.Model):
    rid = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='rid')
    tid = models.IntegerField() #ForeignKey(Task.tid,on_delete=models.CASCADE)
    #Not null, max_length=32
    customerName = models.CharField(max_length=32)

    #Astock + AATP = Sum
    #Nullable-> if RLC save task's scenario weight and no running ReCAST.
    AATP = models.TextField(null=True)      #AATP value for a customer during CW_start to CW_end
    Astock = models.TextField(null=True)

    #Scenario config Not Null
    cusW = models.FloatField()  #Customer Weight [0,1]
    stoW = models.FloatField()  #Stock  Weight   [0,1]

class User(models.Model):
    #set username string as the primary key
    username = models.CharField(max_length=32, primary_key=True)
    hassPW = models.CharField(max_length=128)
    userType = models.IntegerField(default=1) # 0-> admin  1-> RLC
    employeeID = models.CharField(max_length=32)
    email = models.CharField(max_length=32, null=True)

