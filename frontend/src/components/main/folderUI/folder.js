export default function Folder({idx, sessionInfo}) {
    const clickFolderTagText = (e) => {
        const topAdjustCoeff = idx;
        const folder = e.target.parentElement.parentElement;
        if (Number(folder.style.top.slice(0,2)) > 50) {
            folder.style.top = Number(folder.style.top.slice(0,2))-45+'%';
        } else{
            folder.style.top = (82 - topAdjustCoeff * 3) + '%';
        }
    }

    const leftAdjustCoeff = idx % 4;
    const topAdjustCoeff = idx;
    const folderStyle={
        width:  98 - 3*idx +'%',
        top: (82 - topAdjustCoeff * 3) + '%',
        zIndex: 10 - idx,
        left: Math.random()*6 + '%'
    }
    const folderTagStyle = {
        backgroundColor: '#cadcf8',
        left: leftAdjustCoeff * 25 + '%',

    }
    const folderBodyStyle = {
        backgroundColor: '#cadcf8',
    }
    return(
        <div className="folder" style={folderStyle}>
            <div className="folderTag" style={folderTagStyle}>
                <div className="folderTagText" onClick={clickFolderTagText}>
                    {sessionInfo.week + ' 주차'}
                </div>
            </div>
            <div className="folderBody" style={folderBodyStyle}>
                <div className="folderBodyText">
                    <a className="folderUI_link" href={'session/?sessionID='+sessionInfo.id}>
                        {sessionInfo.title}
                    </a>
                </div>
            </div>
        </div>
    )
}
