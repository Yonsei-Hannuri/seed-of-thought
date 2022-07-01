import SeasonItem from './seasonItem';

export default function SeasonMenu(props){
    const seasons = props.seasons?.map((season, idx) => 
        <SeasonItem info={season} key={idx} clickhandler={props.clickhandler}/>
    );

    return (
        <div style={{display: 'flex', flexDirection:'column', flexWrap:'flex-wrap'}}>
            {seasons}
        </div>
    )
}