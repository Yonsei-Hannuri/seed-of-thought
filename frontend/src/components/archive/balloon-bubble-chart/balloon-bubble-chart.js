import * as d3 from "d3";
import ballonDataMaker from "./balloon-data-process";
import { useRef } from "react";

export default function BalloonBubbleChart({wordCount, loading}){ 
  const div = useRef();
  const width = div.current?.offsetWidth;
  const height = div.current?.offsetHeight;
  if (loading === false){
    const priorNodes = {};
    d3.select('svg').selectAll('circle').nodes().forEach((elem) => {
      const priorNode = elem.__data__;
      priorNodes[priorNode.word] = priorNode;
    });
    const newNodes = ballonDataMaker(wordCount, priorNodes, width, height);
    d3.select("svg"); 
    const timeT = Date.now();
    let idx = 0;
    const simulation = d3.forceSimulation()
        .force('charge', d3.forceManyBody().strength(11))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .on('tick', ()=>{
          tick(idx);
          idx++;
        })
    simulation.nodes(Object.values(newNodes)).restart();
  
    function tick(idx) {
        d3.select('svg')
          .selectAll('circle')
          .data(Object.values(newNodes))
          .join('circle')
            .attr('r', (d)=>{
                const delta = d.radius - d.priorR;
                let r = delta === 0 ? d.radius : d.priorR + delta / 3000 * (Date.now() - timeT); 

                if ((delta > 0 && r > d.radius) || (delta < 0 && r < d.radius)){
                  r = d.radius;
                  d.priorR = d.radius;
                }

                d.collisionR = r;
                
                return r;
            })
            .attr('cx', function(d) {
              return d.x;
            })
            .attr('fill', (d)=>{
              return d.color;
            })
            .attr('stroke', 'black')
            .attr('cy', function(d) {
              return d.y;
            })
    
          d3.select('svg')
            .selectAll('text')
            .data(Object.values(newNodes))
            .join('text')
              .attr('x', (d) => d.x )
              .attr('y', (d) => d.y )
              .attr("text-anchor", "middle")
              .attr("dominant-baseline", "central") 
              .text((d) => {
                return d.word
              })
              .style('font-size', (d)=> `${d.collisionR / 2}px`)
              .style("fill", (d)=>d.textColor)
          
          if (idx % 8 === 0) return;
          simulation.nodes(Object.values(newNodes))
            .force('collision', d3.forceCollide().radius((d) => d.collisionR-0.05))
      }
  }   
    return(
      <div ref={div} style={{ minHeight:'400px'}}>
        <svg width={width} height={height}>
        </svg>
      </div>
    );
}