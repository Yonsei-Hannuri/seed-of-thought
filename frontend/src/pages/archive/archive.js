
import SeasonMenu from '../../components/archive/seasonMenu';
import SeasonDetail from '../../components/archive/seasonDetail';
import BalloonBubbleChart from '../../components/archive/balloon-bubble-chart/balloon-bubble-chart';
import { useArchiveData } from './hook';
import Loading from '../../components/common/loading';

export default function Archive({pageSelect}){
    const {allSeasonData, selection, setSelection, selectionData, wordCount, setLoadWait, loadWait} = useArchiveData();


    return(
            <div className='d-flex flex-row justify-content-evenly h-100' style={{flexWrap:'wrap'}}>
                {   
                    <div  style={{width:'40%', minWidth:'300px', minHeight:'500px', overflow:'scroll'}}> 
                    {
                        loadWait.load ? 
                        ''
                        :
                        selection.state === 0 ?
                        <>
                            <div className='cursor2Pointer' onClick={()=>pageSelect({target:{name:'metaSpace'}})}>X</div>
                            <SeasonMenu 
                                seasons={allSeasonData} 
                                clickhandler={
                                    // loadWait.wait? 
                                    // ()=>{} 
                                    // : 
                                    (arg)=> {setLoadWait({load: true, wait: true}); setSelection({season: arg, state:1});}}
                            />
                        </> :
                        selection.state === 1 |  selection.state === 2 ?
                        <>
                            <div 
                                className='cursor2Pointer' 
                                onClick={
                                    // loadWait.wait? 
                                    // ()=>{} 
                                    // : 
                                    ()=>setSelection({state:0})
                                }
                            >
                                X
                            </div>
                            <SeasonDetail 
                                info={selectionData} 
                                clickhandler={  
                                    // loadWait.wait? 
                                    // ()=>{} 
                                    // : 
                                    (arg) => {setLoadWait({load: true, wait: true}); setSelection({author: arg.author, season:arg.season, state:2});}}
                            />
                        </>
                        :
                        ''
                    }
                    </div>  

                }
                <div  className='m-2' style={{width: '40%', minWidth:'420px', height: '100%', minHeight:'420px'}}>
                    <div className='border border-secondary rounded'>
                        <BalloonBubbleChart 
                            loading={loadWait.load}
                            wordCount={selection.state === 0 ? {...allSeasonData.wordCount} : {...wordCount}}
                        />
                    </div>
                    {
                        loadWait.wait ?
                        <Loading/>:
                        ''
                    }
                </div>
            </div>
    )
}