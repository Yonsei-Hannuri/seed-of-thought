import { useEffect, useState } from 'react';
import ReactWordcloud from 'react-wordcloud';
import errorReport from '../modules/errorReport';
import wordCloudDataMaker from '../components/wordCloud/lib/wordCloudDataMaker';

const WordCloud = ({ src }) => {
  const [wordCloudWords, setWordCloudWords] = useState([]);
  const [error, setError] = useState(false);

  useEffect(() => {
    if (src === undefined) return;
    fetch(src, {
      credentials: 'include',
    })
      .then((res) => res.json())
      .then((data) => {
        // let width = document.getElementById('wc_box').offsetWidth;
        // let height = document.getElementById('wc_box').offsetHeight;
        setWordCloudWords(wordCloudDataMaker(data.wordList));
      })
      .catch((e) => {
        setError(true);
        errorReport(e, 'wordcloud_mypage_handleClickCloud');
      });
  }, [src]);

  if (error) {
    return <div> Error! </div>;
  }
  return (
    <div className="row m-0">
      <div className="text-center" id="wc_box">
        <ReactWordcloud
          words={wordCloudWords}
          options={{ fontSizes: [8, 60] }}
        />
      </div>
    </div>
  );
};

export default WordCloud;
