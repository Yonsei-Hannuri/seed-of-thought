import { useState } from 'react';

export default function NameCard({ info, clickhandler }) {
  const [clicked, setClicked] = useState(false);
  return (
    <div>
      <button
        style={{
          border: `2px solid ${info.authorColor}`,
          boxShadow: `0px 0px 3px ${info.authorColor}`,
          color: `${clicked ? 'Gainsboro' : 'black'}`,
        }}
        className="btn m-1 btn-light"
        value={info.googleId}
        onClick={() => {
          clickhandler(info.googleId, info.id);
          setClicked(true);
        }}
      >
        {info.authorName}
      </button>
    </div>
  );
}
