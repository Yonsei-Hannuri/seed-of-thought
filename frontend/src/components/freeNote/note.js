export default function Note({info, writing, page, position, onClick, onUpload}) {
      if (info === false) {
        if (writing) {
          return (
            <div
              style={{ backgroundColor: '#f5f5f5' }}
              className="w-100 h-100 rounded-3 "
            >
              <form className="w-100 h-100" onSubmit={(e)=>onUpload(e)}>
                <textarea
                  style={{ backgroundColor: '#f5f5f5' }}
                  className="w-100 h-75 rounded-3 form-control"
                  name="text"
                  required
                ></textarea>
                <input type="hidden" name="page" value={page}></input>
                <input
                  type="hidden"
                  name="position"
                  value={position}
                ></input>
                <button className="btn btn-light float-end m-2">끄적이기</button>
              </form>
            </div>
          );
        } else {
          return (
            <div
              className="w-100 h-100 rounded-3 cursor2Pointer"
              style={{ backgroundColor: '#f5f5f5' }}
              onClick={() => onClick(position)}
            ></div>
          );
        }
      } else {
        let randomNumber = 0;
        let source = info.text.slice(0, 10);
        let words = source.split('');
        for (let i = 0; i < words.length; i++) {
          randomNumber += words[i].charCodeAt(0);
        }
        randomNumber += info.id;
        const fontSelected = 'font-'+(randomNumber % 5 + 1)
        return (
          <div
            className={
              'textDiv w-100 h-100 p-3 rounded-3 ' + fontSelected
            }
            style={{ backgroundColor: '#f5f5f5' }}
          >
            {info.text}
          </div>
        );
      }
  }
  