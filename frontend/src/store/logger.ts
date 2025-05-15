/* global console */
export const logger = (storeAPI: any) => (next: any) => (action: any) => {
  console.group(action.type);
  console.info("Dispatching:", action);
  const result = next(action);
  console.log("Next state:", storeAPI.getState());
  console.groupEnd();
  return result;
};
