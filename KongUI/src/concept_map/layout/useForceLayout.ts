import { useEffect } from 'react';
import {
  forceSimulation,
  forceLink,
  forceManyBody,
  forceX,
  forceY,
  SimulationNodeDatum,
  SimulationLinkDatum,
  forceCollide
} from 'd3-force';
import { useReactFlow, ReactFlowState, useStore, Node } from 'reactflow';

type UseForceLayoutOptions = {
  strength: number;
  distance: number;
};

// add the width and height 
type SimNodeType = SimulationNodeDatum & Node & {
  width: number;
  height: number;
};

const nodesInitializedSelector = (state: ReactFlowState) =>
  Array.from(state.nodeInternals.values())
    .filter((node) => node.hidden === false)
    .every((node) => node.width && node.height && node.position);

function useForceLayout({ strength = -20, distance = 150 }: UseForceLayoutOptions) {
  // const elementCount = useStore(elementCountSelector);
  const nodesInitialized = useStore(nodesInitializedSelector);
  const { setNodes, getNodes, getEdges } = useReactFlow();

  useEffect(() => {
    console.log("im executin");
    const nodes = getNodes();
    const edges = getEdges();

    if (!nodes.length || !nodesInitialized) {
      return;
    }

    const simulationNodes: SimNodeType[] = nodes
      // For Moritz: uncomment to trigger error
      // .filter((node) => node.hidden === false)
      .map((node) => ({
        ...node,
        width: node.width,
        height: node.height,
        // x: node.position.x,
        // y: node.position.y,
    }));


    // idk how this is even working
    const simulationLinks: SimulationLinkDatum<SimNodeType>[] = edges
      .map((edge) => edge)
      .filter((edge) => simulationNodes
        .find((node) => node.id === edge.source && node.id === edge.target)
      )

    console.log("This is links: ", simulationLinks);
    simulationLinks.forEach((link) => {
      console.log("This is link: ", link);  
    });

  const simulation = forceSimulation()
    // controls how quickly animation stops
    .alphaDecay(0.15)
    .nodes(simulationNodes)
    .force('collide', forceCollide().radius(d => ((d as SimNodeType).width + (d as SimNodeType).height) / 2))
    // controls the repulsion between nodes
    .force('charge', forceManyBody().strength(strength/100))
    .force(
      'link',
      forceLink(simulationLinks)
        .id((d: any) => d.id)
        .strength(0.5)
        .distance(distance)
    )
    .force('x', forceX().x(0).strength(0.003))
    .force('y', forceY().y(0).strength(0.003))
    .on('tick', () => {
      setNodes(      
        simulationNodes.map((node) => ({
        ...node,
        id: node.id,
        data: node.data,
        position: { x: node.x, y: node.y },
        className: node.className,
      })))    
    });
    
  //   console.log("Setting simnNodes: ", simulationNodes)
    setNodes(simulationNodes);

    return () => {
      simulation.stop();
    };
  }, [getNodes, getEdges, setNodes, strength, distance, nodesInitialized]);
}

export default useForceLayout;
