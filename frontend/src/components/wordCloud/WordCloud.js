import ReactWordcloud from 'react-wordcloud';
import wordCloudDataMaker from './lib/wordCloudDataMaker';

const WordCloud = ({ wordList }) => {
  return (
    <div className="row m-0">
      <div className="text-center" id="wc_box">
        <ReactWordcloud
          words={wordCloudDataMaker(wordList)}
          options={{ fontSizes: [8, 60] }}
        />
      </div>
    </div>
  );
};

export default WordCloud;
