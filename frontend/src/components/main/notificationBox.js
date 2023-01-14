import PageWithModal from '../PageWithModal';

export default function NotificationBox({ notifications = [] }) {
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
          <div>{notification_list}</div>
        </div>
      </div>
    );
  } else {
    return '';
  }
}

function Notification({ index, info }) {
  return (
    <PageWithModal
      main={(toggleModal) => (
        <div className="p-1">
          <span className="col-4 text-center p-1 m-1 mx-3">{index}</span>
          <span
            className="p-1 m-1 col-8 text-center link-button"
            onClick={() => toggleModal()}
          >
            {info.title}
          </span>
        </div>
      )}
      modal={(toggleModal) => (
        <div className="m-3 text-start" style={{ width: '100%' }}>
          <h3>
            {info.title}
            <span
              className=" float-end mx-3 cursor2Pointer"
              onClick={() => toggleModal()}
              style={{
                color: 'tomato',
                fontSize: 'x-large',
                fontWeight: 'bold',
              }}
            >
              X
            </span>
          </h3>
          <p>{info.date.slice(0, 10)}</p>
          <p>{info.description}</p>
        </div>
      )}
    />
  );
}
