import React from "react";
import * as d3 from "d3";

const xScale = d3.scaleLinear().domain([-250, 250]).range([0, 500]);
const yScale = d3.scaleLinear().domain([0, 300]).range([320, 0]);

const PAINT_W = 80;
const FT_LINE_Y = 150;
const FT_R = 60;
const THREE_R = 238;
const THREE_X = 220;
const THREE_Y = Math.sqrt(THREE_R ** 2 - THREE_X ** 2); // ~90.77

// SVG arc radii account for the different x vs y pixel density
const svgRx = (r) => xScale(r) - xScale(0);
const svgRy = (r) => yScale(0) - yScale(r);

export default function CourtDiagram({ plays }) {
  return (
    <svg
      viewBox="0 0 500 320"
      style={{ width: "100%", display: "block", background: "#c8a96e" }}
    >
      {/* Court boundary */}
      <rect
        x={xScale(-250)}
        y={yScale(300)}
        width={xScale(250) - xScale(-250)}
        height={yScale(0) - yScale(300)}
        fill="none"
        stroke="white"
        strokeWidth={2}
      />

      {/* Paint */}
      <rect
        x={xScale(-PAINT_W)}
        y={yScale(FT_LINE_Y)}
        width={xScale(PAINT_W) - xScale(-PAINT_W)}
        height={yScale(0) - yScale(FT_LINE_Y)}
        fill="none"
        stroke="white"
        strokeWidth={2}
      />

      {/* Free throw circle — upper half only */}
      <path
        d={`M ${xScale(-FT_R)} ${yScale(FT_LINE_Y)} A ${svgRx(FT_R)} ${svgRy(FT_R)} 0 0 1 ${xScale(FT_R)} ${yScale(FT_LINE_Y)}`}
        fill="none"
        stroke="white"
        strokeWidth={2}
      />

      {/* Basket */}
      <circle
        cx={xScale(0)}
        cy={yScale(0)}
        r={8}
        fill="none"
        stroke="white"
        strokeWidth={2}
      />

      {/* 3-point line — arc centered on basket, not baseline */}
      <path
        d={`
          M ${xScale(-THREE_X)} ${yScale(0)}
          L ${xScale(-THREE_X)} ${yScale(THREE_Y)}
          A ${svgRx(THREE_R)} ${svgRy(THREE_R)} 0 0 1 ${xScale(THREE_X)} ${yScale(THREE_Y)}
          L ${xScale(THREE_X)} ${yScale(0)}
        `}
        fill="none"
        stroke="white"
        strokeWidth={2}
      />

      {plays.map((play, i) => (
        <circle
          key={i}
          cx={xScale(play.x_legacy)}
          cy={yScale(play.y_legacy)}
          r={6}
          fill={
            play.action_type?.toLowerCase().includes("made") ? "green" : "red"
          }
          opacity={0.7}
        />
      ))}
    </svg>
  );
}
