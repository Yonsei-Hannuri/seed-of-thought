import Folder from "./folder";

export default function FolderUI({seasonSessionInfos}) {
    const Folders = seasonSessionInfos.map((sessionInfo, idx) => (
        <Folder sessionInfo={sessionInfo} idx={idx} key={idx}/>
    ))
    return(
        <div className="folderUI">
            {Folders}
        </div>
    )
}

