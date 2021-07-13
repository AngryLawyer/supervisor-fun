import React from 'react';

interface Props {
  width: number;
  height: number;
  className?: string;
  waterLevel: number;
}

const WATER_Y_OFFSET = 30;
const WATER_MAX_HEIGHT = 86;

//https://www.flaticon.com/authors/good-ware
export default ({ width, height, className, waterLevel }: Props) => {
  const waterHeight = WATER_MAX_HEIGHT * waterLevel;
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width={width} height={height} viewBox="0 0 128 128" className={className}>
      <rect width="72" height={waterHeight} fill="blue" x="28" y={WATER_Y_OFFSET + (WATER_MAX_HEIGHT - (waterHeight))}></rect>
      <g>
        <path d="M94.808,96.47a1.751,1.751,0,0,0,1.75-1.75v-7a1.75,1.75,0,0,0-3.5,0v7A1.75,1.75,0,0,0,94.808,96.47Z"/>
        <path d="M121.5,113.75h-2.69V76a16.759,16.759,0,0,0-16.25-16.725V31.942h1.248a1.75,1.75,0,0,0,1.75-1.75v-6a1.751,1.751,0,0,0-1.75-1.75h-1.416A13.642,13.642,0,0,0,88.81,10.75H68.75V6.5A1.75,1.75,0,0,0,67,4.75H61A1.75,1.75,0,0,0,59.25,6.5v4.25H39.19A13.642,13.642,0,0,0,25.608,22.442H24.192a1.751,1.751,0,0,0-1.75,1.75v6a1.75,1.75,0,0,0,1.75,1.75H25.44V59.275A16.759,16.759,0,0,0,9.19,76v37.75H6.5a1.75,1.75,0,0,0-1.75,1.75v6a1.75,1.75,0,0,0,1.75,1.75h115a1.75,1.75,0,0,0,1.75-1.75v-6A1.75,1.75,0,0,0,121.5,113.75ZM115.31,76v37.75h-2.5V76a10.755,10.755,0,0,0-10.25-10.725v-2.5A13.256,13.256,0,0,1,115.31,76Zm-12.75,37.75V68.775A7.254,7.254,0,0,1,109.31,76v37.75Zm-3.5,0H73.75V31.942H99.06ZM27.215,28.442l-.025,0-.024,0H25.942v-2.5h76.116v2.5h-1.224l-.024,0-.025,0ZM70.25,60.378v5.979H57.75V60.378Zm-12.5-3.5V50.9h12.5v5.979Zm12.5,12.979v5.978H57.75V69.857Zm0,9.478v5.979H57.75V79.335Zm0,9.479v5.979H57.75V88.814Zm0-41.415H57.75V41.421h12.5ZM57.75,98.293h12.5v5.978H57.75Zm12.5-66.351v5.979H57.75V31.942Zm-12.5,75.829h12.5v5.979H57.75Zm5-99.521h2.5v2.5h-2.5Zm-23.56,6H88.81a10.167,10.167,0,0,1,10.033,8.192H29.157A10.167,10.167,0,0,1,39.19,14.25ZM54.25,31.942V113.75H28.94V31.942ZM18.69,113.75V76a7.254,7.254,0,0,1,6.75-7.225V113.75ZM12.69,76A13.256,13.256,0,0,1,25.44,62.775v2.5A10.755,10.755,0,0,0,15.19,76v37.75h-2.5Zm107.06,43.75H8.25v-2.5h111.5Z"/>
      </g>
    </svg>
  );
}
