__상황__  

1. 클라이언트에서 특정 pdf를 react-pdf 라이브러리가 load하지 못하는 현상이 벌어졌다.

> __web console__  
Warning: Indexing all PDF objects


2. 파일을 다운 받아 확인을 해보니 학회원이 pdf파일이 아닌 hwp파일을 올렸다.

__해결__
1. 학회원에게 알려 삭제 후 pdf파일 재업로드를 요청했다.

2. 파일의 확장자를 확인하여 pdf파일이 아닌 경우 error response를 보내도록 했다.




