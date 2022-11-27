/**
 * @param {{[string] : number}} wordCounts
 * @returns {{ text: string, value: number}[]}
 */
const generateWordCloudData = (wordCounts, threshold) => {
  let wordList = [];
  for (let key in wordCounts) {
    if (wordCounts[key] < threshold) {
      continue;
    }
    wordList.push({ text: key, value: wordCounts[key] });
  }
  return wordList;
};

export default generateWordCloudData;
