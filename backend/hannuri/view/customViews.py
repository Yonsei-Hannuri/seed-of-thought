from ._dependencies import *

def Login(request):
    #google 에서 code 받고 그 code로 token을 받아서 그 token에 해당하는 email 받기
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        './secret/client_secret.json',
        scopes = 'openid https://www.googleapis.com/auth/userinfo.email'
        )
    flow.redirect_uri = settings.API_URL + '/login'
    flow.fetch_token(code=request.GET.get('code'))
    credentials = flow.credentials
    token = credentials.token
    response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?access_token={}'.format(token))
    email = response.json()['email']
    #받은 이메일을 통해서 로그인 시켜주기
    try: 
        user = User.objects.get(email=email)
        login(request, user)
        response = redirect(settings.FRONT_URL)
        response.set_cookie('isLogin', 'true', domain=settings.ENV('DOMAIN'), max_age=60*60*4)
        return response
    except:
        return redirect(settings.FRONT_URL+'?login=error')
    return redirect(settings.FRONT_URL+'?login=error')

def Signin(request):
    #google 에서 code 받고 그 code로 token을 받아서 그 token에 해당하는 email 받기
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        './secret/client_secret.json',
        scopes = 'openid https://www.googleapis.com/auth/userinfo.email'
        )
    flow.redirect_uri = settings.API_URL + '/signin'
    flow.fetch_token(code=request.GET.get('code'))
    credentials = flow.credentials
    token = credentials.token
    response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?access_token={}'.format(token))
    email = response.json()['email']
    
    #받은 이메일을 저장하기
    try: 
        user = User.objects.create(email=email)
        state_ = request.GET['state']
        state = json.loads(state_)
        name = state['name']
        generation = state['generation']

        user.name = name
        user.generation = generation
        user.save()

        return redirect(settings.FRONT_URL+'?type=signinSuccess')
        
    except:
        return redirect(settings.FRONT_URL+'?type=signinError')

def Logout(request):
    logout(request)
    response = redirect(settings.FRONT_URL)
    response.set_cookie('isLogin', 'false', domain=settings.ENV('DOMAIN'))
    return response

def ProfileColor(request):
    if not request.user:
        return HttpResponse('Unauthorized', status=401)

    request.user.color = request.POST['color']
    request.user.save()
    return HttpResponse('true')

def WordList(request, type, sessionId):
    if not(request.user):
        return HttpResponse('Unauthorized', status=401)

    if type=='mypage':
        wordList = []
        for detgori in request.user.detgori.all():
            wordList.append(detgori.words)
        return HttpResponse(json.dumps({'wordList':wordList}))
    elif type=='session':
        wordList = []
        session = Session.objects.get(pk=sessionId)
        session_detgori = session.detgori.all()
        for detgori in session_detgori:
            wordList.append(detgori.words)
        return HttpResponse(json.dumps({'wordList':wordList})) 

    return HttpResponse('Not Found', status=404)

def my_detgori_infos(userId, currentSeason):
        my_detgori_infos = list()
        currentSessions = currentSeason.session.all()
        currentDetgoris = Detgori.objects.filter(author=userId, parentSession__in=currentSessions)
        my_detgori_infos.append(currentSeason.title)
        for i in range(len(currentDetgoris)):
            my_detgori_infos.append({
                'detgoriId': currentDetgoris[i].id,
                'sessionTitle': currentDetgoris[i].parentSession.title,
                'detgoriTitle': currentDetgoris[i].title,
                'googleId': currentDetgoris[i].googleId,
            })
        return my_detgori_infos

def MypageInfo(request):
    if not(request.user):
        return HttpResponse('Unauthorized', status=401)

    user_seasons = [season for season in request.user.act_seasons.order_by('-id')]
    season_id = None
    try:
        season_id = request.GET['seasonId']
    except:
        pass
    season_detgoris = []
    if len(user_seasons) != 0 and season_id == None:
        season_detgoris = my_detgori_infos(request.user.id,  user_seasons[0])
    elif season_id != None:
        requested_season = Season.objects.get(id=season_id)
        season_detgoris = my_detgori_infos(request.user.id, requested_season)

    seasons = list()
    for season in user_seasons:
        season_info = {
            'id' : season.id,
            'year' : season.year,
            'semester' : season.semester
        }
        seasons.append(season_info)
    response_data = dict()
    response_data['seasonDetgoris'] = season_detgoris
    response_data['seasons'] = seasons
    response_data['name'] = request.user.name
    response_data['color'] = request.user.color
    response_data['generation'] = request.user.generation
    response_data['is_staff'] = request.user.is_staff

    return HttpResponse(json.dumps(response_data), status=200) 

def FrontError(request):
    if not request.user:
        return HttpResponse('Unauthorized', status=401)

    try:
        data = json.loads(request.body.decode('utf-8'))
        error_log = data['errorMessage']['message']
        error_componet = data['from']
        now = datetime.datetime.now()
        fileName = './log/error-front/{}'.format(str(now.year)+'-'+str(now.month))
        is_existed = os.path.exists(fileName)
        with open(fileName, "a" if is_existed else "w") as log:
            log.write(str(now.day)+'일, '+str(now.hour)+'시\n')
            log.write('{} \n'.format(error_componet))
            log.write('{} \n'.format(error_log))
            try: log.write('{}님 이용중 발생 \n'.format(request.user.name))
            except: pass
            log.write('\n==================================================== \n')
            log.close()
    except: pass
    return HttpResponse('FronError logged', status=200)

