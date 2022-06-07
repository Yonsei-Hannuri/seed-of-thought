import SeasonSlide from './seasonSlide';

export default function SeasonSlideUI(props){
    const slides = props.seasons.map((season, idx) => 
        <div onClick={()=>props.clickhandler(season.id)}>
            <SeasonSlide info={season} key={idx}/>
        </div>
    );

    return (
        <div style={{display: 'flex', justifyContent: 'space-around'}}>
            {slides}
        </div>
    )
}