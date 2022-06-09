import axios from 'axios';
import address from '../../config/address.json';
import SeasonMenu from '../../components/archive/seasonMenu';
import SeasonPage from './seasonPage';
import XButton from '../../components/common/XButton';
import { useEffect, useState } from 'react';

const SLIDEPAGE = -1;
const SEASONLOADED = -2;

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
        if (selectSeason !== SLIDEPAGE && selectSeason !== SEASONLOADED){
            (async function(){
                const res = await axios({
                                method: 'GET',
                                url: address.back + 'season/' + selectSeason + '/',
                                withCredentials: true,
                            });
                const data = res.data;
                setSeasonInfo(data);
                setSelectSeason(SEASONLOADED);
            }())
        }
    }, [selectSeason]);

    if (selectSeason !== SEASONLOADED){
        return(
            <>
                <SeasonMenu 
                    seasons={seasons} 
                    clickhandler={(arg)=> setSelectSeason(arg)}
                />
            </>
        )
    } else {
        return (
            <>
                <XButton clickhandler={()=>setSelectSeason(-1)}/>
                <SeasonPage info={seasonInfo}/>
            </>
        )
    }
}