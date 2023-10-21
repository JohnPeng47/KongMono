import cytoscape from 'cytoscape';
import fcose from 'cytoscape-fcose';
import { 
    useReactFlow, 
    ReactFlowState, 
    useStore, 
    Node,
		Edge
} from 'reactflow';
import { RFNodeData } from '../common/common-types';
import { NodeType } from '../common/common-types';

type CytoNode = {
	data: {
		id: string,
		rfNode: Node<RFNodeData>
	}
}

type CytoEdge = {
	data: {
		id: string,
		source: string,
		target: string,
		rfEdge: Edge
	}
}

function getCytoScapeLayout(nodes: Node[], edges: Edge[]): Node[] {
	cytoscape.use(fcose); // register extension
	const cytoNodes: CytoNode[] = nodes.map((node, index) => (
		{
			data: {
				id: node.id,
				identifier: node.id,
				rfNode: {
					...node
				}
			}
		}
	))
	
	const cytoEdges: CytoEdge[] = edges.map((edge, index) => (
		{
			data: {
				id: edge.id,
				target: edge.target,
				source: edge.source,
				identifier: edge.id,
				rfEdge: {
					...edge
				}
			}
		}
	))

	const elements = {
		nodes: cytoNodes,
		edges: cytoEdges
	}

	const cy = cytoscape({
			container: null,
			elements,
			headless: true,
			styleEnabled: false,
			animate: null,
	});

	cy.layout({
			name: 'fcose',
			animate: null, // Whether to animate the layout
			nodeRepulsion: 500000000000000000000, // Node repulsion strength
			idealEdgeLength: 70, // Ideal edge length
			edgeElasticity: 0.45, // Edge elasticity
			nestingFactor: 0.1, // Nesting factor for compound nodes
			gravity: 1.00, // Gravity strength
			numIter: 2500, // Number of iterations
			initialStep: 0.35, // Initial step size
			minDistLimit: 5, // Minimum distance between nodes
			nodeSeparation: 12, // Minimum distance between nodes
			tile: true, // Whether to tile disconnected components
	}).run();

	const repoNodes = cy.nodes().map((node) => (
		// do something with bounding box
		{
			...node.data().rfNode,
			// type: NodeType.AttachedNode,
			// hidden: false,
			position: node.position(),
			positionAbsolute: node.position()
		}
	));

  return repoNodes;
}

export default getCytoScapeLayout;