export default function DetgoriItem({info}){
    return(
        <a href={`https://drive.google.com/file/d/${info.googleId}/view`}>
            <h5>
                {info.authorName} : &nbsp;
                {info.title}
            </h5>
        </a>
    )
}