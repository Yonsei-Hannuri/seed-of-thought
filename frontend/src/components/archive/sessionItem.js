export default function SessionItem({info, selectHandler}){
    return(
        <div onClick={selectHandler}>
            {info.title}
        </div>
    );
}