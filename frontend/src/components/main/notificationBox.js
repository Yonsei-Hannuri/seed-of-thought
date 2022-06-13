import { useState } from "react";

export default function NotificationBox({notifications=[]}) {
  const notification_list = notifications.map((info, idx) => (
    <Notification index={idx + 1} info={info} key={info.id} />
  ));
  if (notification_list.length !== 0) {
    return (
      <div className="my-5">
        <div className="row p-4 align-items-center rounded-3 border shadow-lg">
          <div className="text-start">
            <h4>공지사항</h4>
          </div>
          <table className="table">
            <tbody>{notification_list}</tbody>
          </table>
        </div>
      </div>
    );
  } else {
    return '';
  }
}

function Notification({index, info}){
  const [clicked, setClicked] = useState(false);
    if (clicked === true) {
      return (
        <tr>
          <th className="col-3 text-center">{index}</th>
          <td>
            <h3>
              {info.title}
              <button
                className="float-end link-button"
                onClick={()=>setClicked(!clicked)}
              >
                X
              </button>
            </h3>
            <p>{info.date.slice(0, 10)}</p>
            <p>{info.description}</p>
          </td>
        </tr>
      );
    }
    return (
      <tr>
        <th className="col-3 text-center">{index}</th>
        <td>
          <div
            className="col-9 text-start link-button"
            onClick={()=>setClicked(!clicked)}
          >
            {info.title}
          </div>
        </td>
      </tr>
    );
}
