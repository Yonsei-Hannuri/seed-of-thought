import SessionItem from "./sessionItem";

export default function SeasonPage(props){
    const sessions = props.info.session.map((session, idx) =>
        <SessionItem key={idx} info={session}/> 
    )
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
                <div>
                    {sessions}
                </div>
            </div>
        </div>
    );
}