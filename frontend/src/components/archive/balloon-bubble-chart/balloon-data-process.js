import contrast from 'contrast';

export default function ballonDataMaker(wordCount={}, nodes={}, width=400, height=400){
    const newNodes = {};
    const countTotal = Object.values(wordCount).reduce((pre, cur) => pre + cur, 0);
    const circleSizeCoeff = 1500;
    Object.keys(nodes).forEach((key)=> {
        newNodes[key] = {...nodes[key], radius: 0}; 
    });
    Object.entries(wordCount).forEach(([key, count])=>{
        if(nodes[key]) { 
            newNodes[key].radius = (count / countTotal) * circleSizeCoeff
        } else {
            const color = colorSelctor(Math.random());
            const textColor = contrast(color) === 'light' ? 'black': 'white';

            newNodes[key] = { 
                priorR: 5, 
                x: width/2 + ((Math.random()-0.5) * circleSizeCoeff/3*2), 
                y: height/2 + ((Math.random()-0.5) * circleSizeCoeff/3*2), 
                radius: (count / countTotal) * circleSizeCoeff, 
                color: color, 
                textColor: textColor,
                collisionR: 5,
                word: key
            };
        }
    });

    return newNodes;
};


const colorSelctor = (number) => {
    const num = number * 100;
    let color;
    if (num < 20) color = '#3d5a80';
    else if (num < 40) color = '#98c1d9';
    else if (num < 60) color = '#e0fbfc';
    else if (num < 80) color = '#ee6c4d';
    else  color = '#293241';

    return color;
}

