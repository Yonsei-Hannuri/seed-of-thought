import XButton from "../common/XButton"

export default function SessionModal({info, xhandler}){
    console.log(info);
    return(
        <div style={{display:'flex', justifyContent:'center'}}>
            <div style={{position: 'fixed', border: '2px solid black', width: '40%', height: '80%', backgroundColor: 'white', opacity: '0.8'}}>
                <XButton clickhandler={xhandler}/>
                <h2>{info.title}</h2>
            </div>
        </div>
    )
}