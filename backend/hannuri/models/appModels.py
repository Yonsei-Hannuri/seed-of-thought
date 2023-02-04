from ._dependencies import *

class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('must have user email')
        if not name:
            raise ValueError('must have user name')
        user = self.model(
            email = self.normalize_email(email),
            name = name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 관리자 user 생성
    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email,
            name,
            password
        )
        user.is_admin = True
        user.is_staff = True 
        user.is_active = True
        user.is_superuser = True  
        user.save(using=self._db)
        return user

class Season(models.Model):
    is_current = models.BooleanField(default=False, verbose_name="현재 진행 학기")
    year = models.PositiveIntegerField(default=2020, verbose_name="연도")
    semester = models.PositiveIntegerField(default=1, verbose_name="학기")
    title = models.CharField(max_length=100, verbose_name="제목")
    leader = models.CharField(max_length=50, verbose_name="회장")
    sessioner = models.CharField(max_length=50, verbose_name="학술부장")
    socializer = models.CharField(max_length=50, verbose_name="기획부장")
    googleFolderId = models.CharField(max_length=200, blank=True, verbose_name="구글드라이브 폴더ID")
    words = models.TextField(default='', verbose_name="단어 언급 횟수")

    def save(self, *args, **kargs):
        if self.googleFolderId == '':
            from googleapiclient.discovery import build
            creds = googleDriveAPI.getCreds()
            drive_service = build('drive', 'v3', credentials=creds)
            file_metadata = {
                'name': '한누리 {}-{}'.format(self.year, self.semester),
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [settings.ENV('GOOGLE_DRIVE_ROOT_FOLDER')]
            }
            folder_ = drive_service.files().create(body=file_metadata, fields='id').execute()
            self.googleFolderId=folder_.get('id')
        super(Season, self).save(*args, **kargs)

    def __str__(self):
        return f'{self.year}-{self.semester}'
    
    class Meta:
        verbose_name        = '학기'
        verbose_name_plural = '2. 학기'


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True, verbose_name='구글 이메일')
    name = models.CharField(default='', max_length=100, null=False, blank=False, verbose_name='이름')
    generation = models.IntegerField(default=20, blank=True, verbose_name='기수')
    color = models.CharField(default='#000080', max_length=200, null=True, blank=True)
    permissionId = models.CharField(blank=True, max_length=100)
    writerPermissioned = models.BooleanField(default=False)
    act_seasons = models.ManyToManyField(Season)

    # User 모델의 필수 field
    is_active = models.BooleanField(default=False, verbose_name='활동 허가')   
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, verbose_name='임원진') 
    
    # 헬퍼 클래스 사용
    objects = UserManager()

    # 사용자의 username field는 email로 설정
    USERNAME_FIELD = 'email'
    # 필수로 작성해야하는 field
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return '{}기 {}: {}'.format(self.generation, self.name, self.email)

    class Meta:
        verbose_name        = '학회원'
        verbose_name_plural = '0. 학회원'


class Notification(models.Model):
    #SCOPE_CHOICES = (
    #    ('ALL', '전체 공개'),
    #    ('1MEMBER', '한누리 공개'),
    #    ('2MEMBER', '두누리 공개'),
    #    ('ALLMEMBER', '전체 학회원 공개'),
    #    ('CLOSED', '비공개')
    #)
    #scope = models.CharField(max_length=10, choices=SCOPE_CHOICES, verbose_name='공개범위')
    title = models.CharField(max_length=200, verbose_name="제목")
    description = models.TextField(verbose_name="내용")
    date = models.DateTimeField(auto_now_add=True, verbose_name="날짜")
    

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')} 공지: {self.title}"

    class Meta:
        verbose_name        = '공지사항'
        verbose_name_plural = '1. 공지사항'


class Session(models.Model):
    is_current = models.BooleanField(default=False, verbose_name="현재 진행 세션(메인 화면 표시)")
    season = models.ForeignKey(Season, on_delete=models.PROTECT, related_name="session", verbose_name="학기")
    date = models.DateTimeField(auto_now_add=True, verbose_name="날짜")
    week = models.IntegerField(default=1, verbose_name="주차")
    title = models.CharField(max_length=200, verbose_name="제목")
    googleFolderId = models.CharField(max_length=200, blank=True, verbose_name="구글드라이브 폴더ID")

    def save(self, *args, **kargs):
        if self.googleFolderId == '':
            from googleapiclient.discovery import build
            creds = googleDriveAPI.getCreds()
            drive_service = build('drive', 'v3', credentials=creds)
            file_metadata = {
                'name': '세션 {}주차'.format(self.week),
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [self.season.googleFolderId]
            }
            folder_ = drive_service.files().create(body=file_metadata, fields='id').execute()
            self.googleFolderId=folder_.get('id')
        super(Session, self).save(*args, **kargs)
        
    def __str__(self):
        return f'{self.season}, {self.week}주'

    class Meta:
        verbose_name        = '세션'
        verbose_name_plural = '3. 세션'

class SessionReadfile(models.Model):
    parentSession = models.ForeignKey(Session, related_name='readfile', on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='session/', blank=True)
    googleId = models.CharField(max_length=200, blank=True, verbose_name="구글id")

    def __str__(self):
        return f'{self.parentSession}, 읽기자료'


class Detgori(models.Model):
    parentSession = models.ForeignKey(Session, on_delete=models.PROTECT, related_name='detgori', verbose_name="세션")
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='detgori', verbose_name="댓거리 작성자")
    title = models.CharField(max_length=200, verbose_name="제목")
    date = models.DateTimeField(auto_now_add=True, verbose_name="날짜")
    pdf = models.FileField(upload_to='detgori/', blank=True)
    words = models.TextField(blank=True)
    pureText = models.TextField(blank=True)
    googleId = models.CharField(max_length=200, blank=True, verbose_name="구글id")

    def __str__(self):
        return f'{self.parentSession}, {self.author} 댓거리'

class FreeNote(models.Model):
    text = models.TextField(verbose_name="내용")
    page = models.IntegerField(default=1)
    position = models.IntegerField(default=1)

    def __str__(self):
      return f'{self.page}쪽, {self.position+1}칸'

    class Meta:
        verbose_name = '공책'
        verbose_name_plural = '4. 메타동방-공책'