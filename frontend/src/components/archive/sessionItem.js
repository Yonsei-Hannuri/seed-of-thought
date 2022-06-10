export default function SessionItem({info, selectHandler}){
    return(
        <div style={{display:'flex', backgroundColor:'powderblue', width:'33%', padding:'2%', flexDirection:'column', justifyContent:'center', border: '2px solid black', borderRadius: '10px'}} onClick={selectHandler}>
            <h5>{info.week} 주차</h5>
            <h4>{info.title}</h4>
        </div>
    );
}