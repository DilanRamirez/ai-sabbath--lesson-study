import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export interface UserState {
  id: string | null;
  name: string;
  email: string;
  studyGroupId?: string;
  isLoggedIn: boolean;
}

const initialState: UserState = {
  id: null,
  name: "",
  email: "",
  isLoggedIn: false,
};

const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    login(
      state,
      action: PayloadAction<{
        id: string;
        name: string;
        email: string;
        studyGroupId?: string;
      }>
    ) {
      const { id, name, email, studyGroupId } = action.payload;
      state.id = id;
      state.name = name;
      state.email = email;
      state.studyGroupId = studyGroupId;
      state.isLoggedIn = true;
    },
    logout(state) {
      state.id = null;
      state.name = "";
      state.email = "";
      state.studyGroupId = undefined;
      state.isLoggedIn = false;
    },
  },
});

export const { login, logout } = userSlice.actions;
export default userSlice.reducer;
