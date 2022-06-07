import axios from 'axios';
import address from '../config/address.json';
import SeasonSlideUI from '../components/archive/seasonSlideUI';
import SeasonPage from '../components/archive/seasonPage';
import XButton from '../components/common/XButton';
import { useEffect, useState } from 'react';

const SLIDEPAGE = -1;

export default function Archive(){
    const [seasons, setSeasons] = useState([]);
    const [selectSeason, setSelectSeason] = useState(SLIDEPAGE);
    const [seasonInfo, setSeasonInfo] = useState({});

    useEffect(() => {
        (async function(){
            const res = await axios({
                            method: 'GET',
                            url: address.back + 'season/',
                            withCredentials: true,
                        });
            const data = res.data;
            setSeasons(data);
        })();
    }, []);


    useEffect(() => {
        if (selectSeason !== SLIDEPAGE){
            (async function(){
                const res = await axios({
                                method: 'GET',
                                url: address.back + 'season/' + selectSeason + '/',
                                withCredentials: true,
                            });
                const data = res.data;
                setSeasonInfo(data);
            }())
        }
    }, [selectSeason]);

    if (selectSeason === SLIDEPAGE){
        return(
            <>
                <SeasonSlideUI 
                    seasons={seasons} 
                    clickhandler={(arg)=> setSelectSeason(arg)}
                />
            </>
        )
    } else {
        return (
            <>
                <XButton clickhandler={setSelectSeason} args={[-1]}/>
                <SeasonPage info={seasonInfo}/>
            </>
        )
    }
}