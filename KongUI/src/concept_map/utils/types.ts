import { Dispatch, SetStateAction, createElement } from 'react';

export type UseStateDispatch<S> = Dispatch<SetStateAction<S>>;

export const addPropsToRFNode = (WrappedComponent, additionalProps = {}) => {
  return (props) => {
      return createElement(WrappedComponent, {
          ...props,
          ...additionalProps,
      });
  };
};