import { useEffect, useState } from "react";
import SessionItem from "../../components/archive/sessionItem";
import axios from "axios";
import address from '../../config/address.json';
import SessionModal from "../../components/archive/sessionModal";

const NOSELECT = -1

export default function SeasonPage(props){
    const [selectSession, setSelectSession] = useState(NOSELECT);
    const [sessionInfo, setSessionInfo] = useState({});

    const sessions = props.info.session.map((session, idx) =>
        <SessionItem 
            key={idx} 
            info={session} 
            selectHandler={()=>setSelectSession(session.id)} 
        /> 
    )

    useEffect(()=>{
        (async function(){
            const res = await axios({
                method: 'GET',
                url: address.back + 'session/' + selectSession + '/',
                withCredentials: true,
            });
            const data = res.data;
            setSessionInfo(data);
        }())
    },[selectSession])

    return(
        <div>
            <div>
                {selectSession !== NOSELECT ? 
                    <SessionModal info={sessionInfo} xhandler={()=>setSelectSession(NOSELECT)}/> :''}
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