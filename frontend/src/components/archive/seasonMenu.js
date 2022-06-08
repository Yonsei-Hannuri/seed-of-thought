import SeasonItem from './seasonItem';

export default function SeasonMenu(props){
    const slides = props.seasons.map((season, idx) => 
        <SeasonItem info={season} key={idx} clickhandler={props.clickhandler}/>
    );

    return (
        <div style={{display: 'flex', justifyContent: 'space-around'}}>
            {slides}
        </div>
    )
}