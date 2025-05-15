import { configureStore } from "@reduxjs/toolkit";
import userReducer from "./slices/user/user-slice";

declare var process: {
  env: {
    NODE_ENV: string;
  };
};
import lessonReducer from "./slices/lesson/lesson-slice";
import themeReducer from "./slices/theme/theme-slice";
import { logger } from "./logger";

const isDev = process.env.NODE_ENV === "development";

export const store = configureStore({
  reducer: {
    user: userReducer,
    lesson: lessonReducer,
    theme: themeReducer,
  },
  middleware: (getDefaultMiddleware) => (isDev ? getDefaultMiddleware().concat(logger) : getDefaultMiddleware()),
});
// Infer typed hooks
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
