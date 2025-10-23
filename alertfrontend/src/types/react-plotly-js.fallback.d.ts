/*
  Fallback typings for react-plotly.js
  -------------------------------------------------
  @types/react-plotly.js is installed, so this file is kept disabled
  (suffix .fallback.d.ts) to avoid conflicts with the official types.

  If you work in an environment without the @types package, rename this file to:
    src/types/react-plotly-js.d.ts
  to activate the fallback.
*/

declare module 'react-plotly.js' {
  import * as React from 'react';
  const Plot: React.ComponentType<any>;
  export default Plot;
}

