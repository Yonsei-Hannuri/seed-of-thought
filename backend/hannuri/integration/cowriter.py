from hannuri.models import *
import json 

def get_subject(session_id, ):
    session = Session.objects.filter(pk=session_id).first()
    if not session:
        return None
    
    subjectInfo = {
        "subjectTitle": session.title,
        "subjectPurpose": "생각의 공유",
        "subjectContent": json.dumps(
            {
                "attatchments": {
                    "pdf": [
                        "https://files.yonsei-hannuri.org/" + rf.googleId for rf in session.readfile.all()
                    ]
                }
            }
        )
    }
    
    return subjectInfo