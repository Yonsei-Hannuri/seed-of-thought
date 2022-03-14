import { Component } from "react"

class EasterEgg extends Component {
    static defaultProps = {
        says: [
            [
                '안녕하세요~!', 
                '좋은 하루 보내고 있나요?', 
                '앞으로 메타동방에 여러 기능이 추가될 예정이에요.',
                '우선적으로 생각하고 있는 거는',
                '포토북이랑 아카이빙 페이지입니다.',
                '얼른 개발 하려고는 하는데',
                '언제가 될지는 모르겠네요 ㅋㅠ',
                '그럼 저는 이만 갈게요~',
            ],
            [
                '열심히 코딩 중...',
            ],
            [
                '홈페이지 건의사항 있으면 말해주세요~',
                '그런 당신은 미래의 앱 디자이너!',
                'jnh03336@gmail.com',
                '커몬커몬',
            ],
            [
                '사랑한다 말하고~',
                '날 받아줄 때에~',
                '더 이상 나는 바랄게 없다고~',
                '자신있게 말해노코~',
                '자라나는 욕심에~',
                '무안해지지만~',
                '또 하루 종일 그대의 생각에~',
                '난 맘 졸여요~🎵',
                '(음치임)',
            ],
            [
                '나는 지금 미쳐가고 있다.',
                '이 헤드폰에 내 모든 몸과',
                '영혼을 맡겼다',
                '...',
                '음악만이 나라에서 허락하는',
                '유일한 마약이니까',
                '이게 바로 지금의 나다',
                '🎧'
            ]
        ],
    };

    state = {
        say: '',
        num: 0,
        clickLimit: 0,
        clickTimes: 0,
    }

    componentDidMount(){
        const num = Math.floor(Math.random()*this.props.says.length)
        this.setState({
            num: num,
            say: this.props.says[num],
            clickLimit: this.props.says[num].length,
        });
    }


    addClick = () =>{
        this.setState({clickTimes: this.state.clickTimes+1});
    }

    render(){
        if (!this.state.clickTimes){
            return(
                <div onClick={this.addClick} style={{display:'flex'}}>
                    <span style={{marginLeft:'auto'}}>🧑🏻‍💻</span> 
                </div>
            );
        }
        else if(this.state.clickTimes > this.state.clickLimit){
            return('');
        }
        return(   
            <div>
                <div style={{display:'flex'}}>
                    <div style={{marginLeft:'auto'}}>
                        {this.state.say[this.state.clickTimes-1]} 
                    </div>
                    <span  onClick={this.addClick} style={{marginLeft: 'auto'}}>🧑🏻‍💻</span> 
                </div>
            </div>
        );
    }
}

export default EasterEgg;
