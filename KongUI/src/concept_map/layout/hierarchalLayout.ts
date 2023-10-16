import { hierarchy, cluster, HierarchyNode, HierarchyPointNode } from "d3-hierarchy";
import { Node, Edge } from "reactflow";

type D3NodeData<T> = {
    data: Node<T>;
    children?: D3NodeData<T>[];
    x: number;
    y: number;
};

class HierarchalLayout<T = any> {
    nodes: Node[];
    edges: Edge[];
    width: number;
    height: number;

    constructor(nodes: Node[], edges: Edge[]) {
        this.nodes = nodes
        this.edges = edges

        this.width = this.nodes[0]?.width ?? 300
        this.height = this.nodes[0]?.height ?? 300
    }

    // Convert the provided nodes to a d3-friendly format
    toD3Hierarchy(rootId: string): HierarchyNode<D3NodeData<T>> {
        const findChildren = (id: string): D3NodeData<T>[] => {
            return this.nodes
                // d3 expects parentNode property here
                .map(node => (
                    {
                        ...node,
                        parentNode: this.edges.find(edge => edge.target === node.id)?.source ?? undefined 
                    }
                ))
                .filter(node => node.parentNode === id)
                // add attributes expected by d3
                .map(node => (
                    {
                        ...node,
                        data: node.data,
                        children: findChildren(node.id),
                        x: node.position.x,
                        y: node.position.y
                    }
                ));
        };

        const rootNode: D3NodeData<T> = {
            ...this.nodes[0],
            children: findChildren(rootId),
            x: 0,
            y: 0
        };

        return hierarchy(rootNode);
    }

    // Convert the provided d3-friendly nodes back to the react-flow format
    getNodeWithPosition(): Node[] {
        const root = this.toD3Hierarchy(this.nodes[0].id);

        // parameterize this so we can use other layouts
        // height/width manually specified actually looks better
        // const tree = cluster().size([this.width, this.height]);
        console.log(this.width, this.height)

        const tree = cluster().size([1000, 1000]);
        const treeLayout: HierarchyPointNode<unknown> = tree(root as HierarchyNode<unknown>);
        
        // console.log("TREE LAYOUT: ", treeLayout);
        this.getLayoutPositions(treeLayout, this.nodes);
        return this.nodes
    }

    getLayoutPositions(root: HierarchyPointNode<unknown>, nodes: Node[]): void {
        // hack
        let data = root.data as Node;
        
        let node = nodes.filter(node => node.id === data.id)[0];
        node.position = { x: root.x, y: root.y };

        if (root.children) {
            root.children.forEach(child => {
                this.getLayoutPositions(child, nodes);
            });
        }
    }
}

export function getLayoutedElements(nodes: Node[], edges: Edge[]) {
    let augmented_nodes = new HierarchalLayout(nodes, edges).getNodeWithPosition();
    
    return augmented_nodes;
}