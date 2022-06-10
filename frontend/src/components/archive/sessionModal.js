import XButton from "../common/XButton"
import DetgoriItem from "./detgoriItem";

export default function SessionModal({info, xhandler}){
    const detgoris = info.detgori?.map((detgori)=><DetgoriItem key={detgori.id} info={detgori}/>)
    return(
        <div style={{display:'flex', justifyContent:'center'}}>
            <div style={{position: 'fixed', border: '2px solid black', width: '70%', minHeight: '20rem', backgroundColor: 'white', opacity: '0.9', padding: '3%'}}>
                <div style={{display:'flex', justifyContent: 'flex-end'}}>
                    <XButton clickhandler={xhandler}/>
                </div>
                <h2>{info.title}</h2>
                <h5>{info.week} 주차</h5>
                <div>
                    {detgoris}
                </div>
            </div>
        </div>
    )
}