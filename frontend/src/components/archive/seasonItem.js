const style = {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    backgroundColor: 'orange',
    width: '30%',
    height: '10rem',
    textAlign: 'center',
    clipPath: 'circle(35%)',
}

export default function SeasonItm(props){
    return(
        <div style={style} onClick={()=>props.clickhandler(props.info.id)}>
            <div>
                {props.info.year}-{props.info.semester}:
            </div>
            <div style={{padding: '0 30% 0 30%'}}>
                {props.info.title}
            </div>
        </div>
    )
}