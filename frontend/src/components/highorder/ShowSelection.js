import { useState, useRef } from 'react';
import getGlobalRect from '../../modules/getGlobalRect';

const ShowSelection = ({ title, panel, options }) => {
  const [selected, setSelected] = useState(null);
  const [panelHeight, setPanelHeight] = useState(null);
  const div = useRef();
  const onSelect = (selection) => {
    const rect = getGlobalRect(div.current);
    if (selected) {
      setPanelHeight(rect.height);
    }
    window.scrollTo(0, rect.top);
    setTimeout(() => {
      setSelected(selection);
    }, 500);
  };
  return (
    <div className="row">
      <span className="fw-bolder fs-4 py-1"> {title}</span>
      <div ref={div} style={{ minHeight: `${panelHeight}px` || 'auto' }}>
        {selected && panel(selected)}
      </div>
      <div>
        <ul className="d-flex p-0 clear-fix overflow-auto justify-content-start flex-wrap">
          {options(onSelect)}
        </ul>
      </div>
    </div>
  );
};

export default ShowSelection;
