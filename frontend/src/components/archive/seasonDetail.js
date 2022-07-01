import AuthorItem from "./authorItem";

export default function SeasonDetail(props){
    const authors = props.info.author.map((author, idx) =>
        <AuthorItem 
            key={idx} 
            info={author} 
            selectHandler={()=>props.clickhandler({author: author.id, season: props.info.id})} 
        /> 
    )
    const sessions = props.info.session.map(
        (session) => {
            return (
                <a 
                    key={session.id} 
                    target='blank' 
                    href={`/session/?sessionID=${session.id}`}>
                        <li className="list-group-item list-group-item-action list-group-item-primary">
                            {session.week}주차: {session.title}
                        </li>
                </a>
                )
        }
    );

    return(
        <div>
            <div>
                <h2 style={{textAlign: 'center'}}>{props.info.title}</h2>
                <p style={{textAlign: 'center'}}>{props.info.year}년도 {props.info.semester}학기</p>
                <div style={{display:'flex', flexDirection:'row', justifyContent:'space-around'}}>
                    <div>{props.info.sessioner} 학술부장</div>
                    <div>{props.info.leader} 회장</div>
                    <div>{props.info.socializer} 기획부장</div>
                </div>
            </div>
            <div className='d-flex flex-row'>
                {authors}
            </div>
            <>
                {sessions}
            </>
        </div>
    );
}