import contrast from 'contrast';

export default function AuthorItem({info, selectHandler}){
    const textColor =  contrast(info.color) === 'light' ? 'black' : 'white'; 
    return(
        <div className='m-1 p-1 cursor2Pointer' style={{backgroundColor: info.color, color: textColor, border: '2px solid black', borderRadius: '10px'}} onClick={selectHandler}>
            {info.name}
        </div>
    );
}