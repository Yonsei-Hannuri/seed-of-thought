import axios from 'axios';
import address from '../../config/address.json';
import { useEffect, useState } from 'react';


export const useArchiveData = () => {

    const [selection, setSelection] = useState({season: 0, author: 0,  state: 0});
    const [allSeasonData, setAllSeasonData] = useState({wordCount:{}, initalized: false});
    const [selectionData, setSelectionData] = useState([]);
    const [wordCount, setWordCount] = useState({});
    const [loadWait, setLoadWait] = useState({load: true, wait: true});

    const waitTolerance = 10000; 
    useEffect(() => {
        if (selection.state === 0 && allSeasonData.initalized === false){
            (async function(){
                const [resSeason, resWords] = await Promise.all([
                        axios({
                                method: 'GET',
                                url: address.back + 'season/',
                                withCredentials: true,
                                params: {
                                    condition: 'no_current',
                                }
                            }), 
                        axios({
                                method: 'GET',
                                url: address.back + 'archive/',
                                params: {
                                    target: 'hannuri',
                                }
                        })
                        ]);
                const allSeasonData = resSeason.data;
                allSeasonData.wordCount = resWords.data;
                setAllSeasonData(allSeasonData);
                setLoadWait({load: false, wait: true});
                setTimeout(()=>setLoadWait({load: false, wait: false}), waitTolerance);
            })();
        } else if (selection.state === 1) {
            (async function(){
                const [resSeason, resWords, resActiveUser] = await Promise.all([
                        axios({
                                method: 'GET',
                                url: address.back + 'season/' + selection.season + '/',
                                withCredentials: true,
                            }),
                        axios({
                                method: 'GET',
                                url: address.back + 'archive/',
                                params: {
                                    target: 'season',
                                    id: selection.season,
                                }
                        }),
                        axios({
                                method: 'GET',
                                url: address.back + 'user/',
                                withCredentials: true,
                                params: {
                                    seasonActiveUser: selection.season
                                }
                        })
                    ]);
                const SeasonData = resSeason.data;
                const wordsData = resWords.data;
                SeasonData['author'] = resActiveUser.data;
                setSelectionData(SeasonData);
                setWordCount( wordsData );
                setLoadWait({load: false, wait: true});
                setTimeout(()=>setLoadWait({load: false, wait: false}), waitTolerance);
            }())
        } else if (selection.state === 2) {
            (async function(){
                const resWords = 
                    await axios({
                        method: 'GET',
                        url: address.back + 'archive/',
                        params: {
                            target: 'author',
                            id: selection.author,
                            id2: selection.season,
                        }
                    })
                const wordData = resWords.data;
                setWordCount(wordData);
                setLoadWait({load: false, wait: true});
                setTimeout(()=>setLoadWait({load: false, wait: false}), waitTolerance);
            }())
        }
    }, [selection]);


    return {
        allSeasonData,
        selection,
        setSelection,
        wordCount,
        selectionData,
        loadWait,
        setLoadWait
    };
}