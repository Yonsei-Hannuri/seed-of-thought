import Slide from './seasonSlide';

export default function SeasonSlides(props){
    const slides = props.seasons.map(season => {
        <Slide info={season}/>
    });

    return (
        <div style={{display: 'flex'}}>
            {slides}
        </div>
    )
}