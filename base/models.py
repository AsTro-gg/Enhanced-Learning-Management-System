from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True # created a class which is common in most of the fields and the subclass meta , abstract le chei database ma table banna dinna


class User(AbstractUser):
    ROLE_CHOICES =[
        ('admin','Admin'),            #predefining choices for code asthetics
        ('instructor','Instructor'),
        ('student','Student'),          #Used inheritence to customise just the required field instead of writing everything
        ('sponsor','Sponsor')
    ]
    username = models.CharField(max_length=300,unique=True)
    password = models.CharField(max_length=300)
    email = models.EmailField(null=True)
    image = models.FileField()
    contact = models.CharField(max_length=12)
    role = models.CharField(max_length=300,choices=ROLE_CHOICES,default='student')

class Course(BaseModel): #automatically inherits models.Model + also has the attributes of mother class
    DIFFICULTY_CHOICES = [
        ('easy','Easy'),            #choices
        ('intermediate','Intermediate'),
        ('hard','Hard')
    ]
    title = models.CharField(max_length=300)
    description = models.TextField()
    instructor = models.ForeignKey(User,limit_choices_to={'role':'instructor'},on_delete=models.CASCADE) # specifiying the type as we didnot write the user model
    difficulty = models.CharField(max_length=13,choices=DIFFICULTY_CHOICES)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)

    def __str__(self): # using str for better understanding as it gives readable representations. instead of just returning titles i returned multiple string values using f string
        return f'{self.title}({self.difficulty})' # i want to know the title by its difficulty so i use f string.

class Enrollment(BaseModel):
    STATUS_CHOICES = [
        ('running','Running'),
        ('completed','Completed')
    ]
    student = models.ForeignKey(User,limit_choices_to={'role':'student'},on_delete=models.CASCADE) #same
    course = models.ForeignKey(Course,on_delete=models.SET_NULL,null=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='running')

    #there can be duplicates so for prevention of duplicates,

    class Meta:
        unique_together = ['student','course']

    def __str__(self):
        return f'{self.student.username} in {self.course.title}' #str for showing student in which course enrolled

class Assesment(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True) # not compulsory
    due_date = models.DateField()
    max_score = models.PositiveIntegerField() #must be positive

    def __str__(self):
        return f'Assesment: {self.title} for {self.course.title}'#showing assesment by course title

class Submission(models.Model):
    assesment = models.ForeignKey(Assesment,on_delete=models.CASCADE)
    student = models.ForeignKey(User,limit_choices_to={'role':'student'},on_delete=models.CASCADE)
    score = models.PositiveIntegerField(null=True,blank=True)
    submitted_file = models.FileField(upload_to='submissions/') #linking url for uploading
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username}'s submission of {self.assesment.title}"
    
class Sponsorship(BaseModel):
    SPONSORED_STATUS = [
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected')
    ]
    sponsor = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'role':'sponsor'},related_name='sponsorships') # as django uses reverse relationships for One to many i use related name as i called 2 datas from same class in a single class which caused conflicts
    student = models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'role':'student'},related_name='sponsored_student')
    amount = models.PositiveIntegerField() # ever got negative sponsorship?(except by your friends??)
    status = models.CharField(max_length=10,choices=SPONSORED_STATUS,default='pending')

    def __str__(self):
        return f"{self.student.username} is sponsored by{self.sponsor.username}"

class Notification(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user.username}'
    
    class Meta:
        ordering = ['-created_at'] # Using basemodel's created at for ordering the notifications
    
#Important things done
#Str for every thing to have better control in admin panel
#limit choice for some parameter to have better control and no need of logics in views
#Simple meta class use for better control on much neeeded fields only
#related name parameter for handling error of calling a single class twice inside another class
#multiple data passed in str with f string for better understanding relationships than the classic title approach
#choices for some fields
## Base model class which has some attributes used by generally all with abstract meta class so that we can inherit basemodel while it isnot written on the database