import { Node } from "reactflow"

export function getNodeElement(node: Node): HTMLElement {
	return document.querySelector(`[data-id="${node.id}"]`)
}

export const updateNode = (nodes: Node[], updateNodes: Node[]) => {
	return (nodes: Node[]) => {
		return nodes.map((nds) => {
			return updateNodes.find((node) => node.id === nds.id) ?? nds
		})
	}
}

export function generateUUID(): string {
	return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
			const r = (Math.random() * 16) | 0;
			const v = c === 'x' ? r : (r & 0x3) | 0x8;
			return v.toString(16);
	});
}

export const noop = () => {};
