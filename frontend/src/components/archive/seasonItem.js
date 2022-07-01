const style = {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    backgroundColor: '#BCD2E8',
    border: "2px solid #73A5C6",
    textAlign: 'center',
    width: '40%',
}

export default function SeasonItem({info, clickhandler}){
    return(

        <div className='cursor2Pointer w-100 rounded border border-dark p-2 mb-2 border-opacity-75' style={style} onClick={()=>clickhandler(info.id)}>
            <div>
                {info.year}-{info.semester}:
            </div>
            <div>
                {info.title}
            </div>
        </div>
    )
}