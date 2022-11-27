import sumCounts from '../../../modules/sumCounts';

/**
 *
 * @param { string[] } data 각 요소 string은 {'a': 3, 'b': 4} 와 같은 형태
 * @returns
 */
function chartDataMaker(data) {
  const words = sumCounts(data);
  // make a rank
  let wordArray = [];
  for (let key in words) {
    let count = words[key];
    wordArray.push([key, count]);
  }
  wordArray.sort(function (a, b) {
    return -(a[1] - b[1]);
  });

  // chart config
  let chartData = {
    labels: wordArray.slice(0, 5).map((item) => item[0]), //많이 언급된 단어 라벨
    datasets: [
      {
        label: '', //이건 왜 있는 걸까?
        data: wordArray.slice(0, 5).map((item) => item[1]), //언급 횟수
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(255, 206, 86, 0.2)',
          'rgba(75, 192, 192, 0.2)',
          'rgba(153, 102, 255, 0.2)',
          'rgba(255, 159, 64, 0.2)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  return chartData;
}

export default chartDataMaker;
