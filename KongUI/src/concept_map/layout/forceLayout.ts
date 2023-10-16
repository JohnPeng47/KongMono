// import { Node, Edge } from "reactflow";
// import { collide, simulation } from "./physics";
// import { forceLink } from "d3-force";

// type ForceNode = Node & { 
//     fx?: number | unknown ; 
//     fy?: number | unknown ; 
// };

// export function forceLayout(nodes: ForceNode[], edges: Edge[], initialised: boolean) {
//   let layoutNodes = nodes.map((node) => ({
//     ...node,
//     x: node.position.x,
//     y: node.position.y
//   }));
//   let running = false;

//   // If React Flow hasn't initialised our nodes with a width and height yet, or
//   // if there are no  nodes in the flow, then we can't run the simulation!
//   if (!initialised ||nodes.length === 0) return [false, {}];

//   // @ts-ignore
//   simulation.nodes(layoutNodes).force(
//     "link",
//     forceLink(edges)
//       .id((d) => d.id)
//       .strength(0.05)
//       .distance(100)
//   );

//   // The tick function is called every animation frame while the simulation is
//   // running and progresses the simulation one step forward each time.
//   const tick = () => {
//     nodes.forEach((node, i) => {
//       const dragging = Boolean(
//         document.querySelector(`[data-id="${node.id}"].dragging`)
//       );

//       // Setting the fx/fy properties of a node tells the simulation to "fix"
//       // the node at that position and ignore any forces that would normally
//       // cause it to move.
//       nodes[i].fx = dragging ? node.position.x : null;
//       nodes[i].fy = dragging ? node.position.y : null;
//     });

//     simulation.tick();
//     nodes.forEach((node) => (
//         { 
//             ...node, 
//             position: {
//                  x: node.x, 
//                  y: node.y 
//             } 
//         }
//     ))

//     window.requestAnimationFrame(() => {
//       // Give React and React Flow a chance to update and render the new node
//       // positions before we fit the viewport to the new layout.
//       fitView();

//       // If the simulation hasn't be stopped, schedule another tick.
//       if (running) tick();
//     });
//   };

//   const toggle = () => {
//     running = !running;
//     running && window.requestAnimationFrame(tick);
//   };

//   const isRunning = () => running;

//   return [true, { toggle, isRunning }];
// }

export {}