import EasterEgg from "../components/easterEgg";
function MetaSpace(props) {
  return (
    <div className='d-flex flex-column'>
        <img
          name='freeNote' onClick={props.pageSelect}
          className="m-3 p-3 cursor2Pointer"
          src="img/notebook.png"
          width="220"
          height="220"
          alt="Notebook  free icon"
          title="Notebook free icon"
        />
        <img
          name='archive' onClick={props.pageSelect}
          className="m-3 p-3 cursor2Pointer"
          style={{alignSelf:'center'}}
          src="img/fossil.png"
          width="220"
          height="220"
          alt="arhchive"
          title="arhchive"
        />
        <EasterEgg/>
    </div>
  ); 
}

export default MetaSpace;
