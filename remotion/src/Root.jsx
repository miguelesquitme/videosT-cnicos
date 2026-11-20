import React from 'react';
import {Composition} from 'remotion';
import {R3} from './R3';
import {R4} from './R4';
import p3 from '../props_r3.json';
import p4 from '../props_r4.json';
import {R5} from './R5';
import p5 from '../props_r5.json';
const meta = ({props}) => ({durationInFrames: Math.ceil(props.total * 30)});
const C = (id, comp, p) => <Composition id={id} component={comp} durationInFrames={Math.ceil(p.total * 30)} fps={30} width={1080} height={1920} defaultProps={p} calculateMetadata={meta} />;
export const Root = () => <>
  {C('R3', R3, p3)}
  {C('R4', R4, p4)}
  {C('R5', R5, p5)}
</>;
