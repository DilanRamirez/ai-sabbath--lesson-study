// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const logger = (storeAPI: any) => (next: any) => (action: any) => {
  console.group(action.type);
  console.info("Dispatching:", action);
  const result = next(action);
  console.log("Next state:", storeAPI.getState());
  console.groupEnd();
  return result;
};
