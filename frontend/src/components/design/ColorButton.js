export default function ColorButton({ color, text, onClick, clicked }) {
  return (
    <div>
      <button
        style={{
          border: `2px solid ${color}`,
          boxShadow: `0px 0px 3px ${color}`,
          color: `${clicked ? 'Gainsboro' : 'black'}`,
        }}
        className="btn m-1 btn-light"
        onClick={onClick}
      >
        {text}
      </button>
    </div>
  );
}
