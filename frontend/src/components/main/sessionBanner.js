export default function SessionBanner({recentSession={}}) {
    if (recentSession.week){
        return (
        <div>
            <div className="px-4 py-5 my-5 text-center">
            <h3 className="display-5 fw-normal">
                {recentSession.week} 주차
            </h3>
            <h1 className="display-5 fw-bold">
                {recentSession.title}
            </h1>
            <div className="col-lg-6 mx-auto">
                <div className="d-grid gap-2 d-sm-flex justify-content-sm-center">
                <a href={'/session/?sessionID=' + recentSession.id}>
                    <button
                    type="button"
                    className="btn btn-light border btn-lg px-4 gap-3"
                    >
                    세션 입장하기
                    </button>
                </a>
                </div>
            </div>
            </div>
        </div>
        );
    } else {
        return '';
    }
}
