import EasterEgg from "../components/easterEgg";
function MetaSpace(props) {
  return (
    <div>
        <img
          name='freeNote' onClick={props.pageSelect}
          className="m-3 p-3 cursor2Pointer"
          src="notebook.png"
          width="220"
          height="220"
          alt="Notebook  free icon"
          title="Notebook free icon"
        />
        <EasterEgg/>
    </div>
  ); 
}

export default MetaSpace;
