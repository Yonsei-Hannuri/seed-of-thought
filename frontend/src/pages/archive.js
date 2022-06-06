import axios from 'axios';
import address from '../config/address.json';
import { useEffect, useState } from 'react';

const SLIDE = 0;
const SEASONPAGE = 1;

export default function Archive(){
    const [seasons, setSeasons] = useState([]);
    const [selected, setSelected] = useState(SLIDE);

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
    
    return(
        <div>
            {seasons.length === 0 ? '' : seasons[0].year}
        </div>
    )
}