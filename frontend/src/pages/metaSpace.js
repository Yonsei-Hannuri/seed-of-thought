function MetaSpace(props) {
  return (
    <div>
        <img
          name='freeNote' onClick={props.pageSelect}
          className="m-3 p-3 cursor2Pointer"
          src="https://image.flaticon.com/icons/png/512/3324/3324709.png"
          width="220"
          height="220"
          alt="Notebook  free icon"
          title="Notebook free icon"
        />
    </div>
  ); 
}

export default MetaSpace;
