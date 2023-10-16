import { Backend, getBackend} from "../common/Backend"
import { createContext } from 'use-context-selector';
import React, { memo } from "react";
import { useMemoObject } from "../hooks/useMemo";

import { Node } from "reactflow";
import { RFNodeData } from "../common/common-types";
import { AxiosResponse } from "axios";

// WHy do we have this separately from backend file again???
interface BackendContext {
	backend: Backend
}

interface BackendProviderProps {
	url: string
}

export const BackendContext = createContext<Readonly<BackendContext>>(
	{} as BackendContext
);

export const BackendProvider = memo(({url, children}: React.PropsWithChildren<BackendProviderProps>) => {
	const backend = getBackend(url);

	const value = useMemoObject<BackendContext>({
		backend
	});

	return <BackendContext.Provider value={value}>{children}</BackendContext.Provider>
})