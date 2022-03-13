import chartDataMaker from "./charDateMaker";
import chartOption from "./chartOption";
import { Bar } from 'react-chartjs-2';
function WordChart(props){
    const chartData = chartDataMaker(props.data);
    const options = chartOption;
    return (
      <div className="mt-3 py-3" id="statics">
        <span className="fw-bolder fs-4 m-0">통계</span>
        <div className="maxWidth m-auto">
          <Bar data={chartData} options={options} />
        </div>
      </div>
    );
}

export default WordChart;
