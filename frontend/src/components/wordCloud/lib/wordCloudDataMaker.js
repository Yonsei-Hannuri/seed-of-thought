import sumCounts from '../../../modules/sumCounts';
import generateWordCloudData from './generateWordCloudData';

const wordCloudThreshold = 3;
/**
 *
 * @param { string[] } counts 각 요소 string은 {'a': 3, 'b': 4} 와 같은 형태
 * @returns {{ text: string, value: number}[]} sumedCounts 각 count가 모두 합쳐진 결과물
 */
const wordCloudDataMaker = (counts) => {
  const wordCounts = sumCounts(counts);
  const wordCloudData = generateWordCloudData(wordCounts, wordCloudThreshold);
  return wordCloudData;
};

export default wordCloudDataMaker;
