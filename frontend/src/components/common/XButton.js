export default function XButton(props){
    return(
        <div onClick={()=>props.clickhandler(...props.args)}>
            X
        </div>
    )
}