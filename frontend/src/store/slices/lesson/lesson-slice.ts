import { Lesson, LessonMetadata } from "@/types/types";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface LessonState {
  currentLesson: Lesson | null;
  metadata: LessonMetadata[]; // List of all lessons available
  selectedDayIndex: number | null; // Tracks current study day
  loading: boolean;
  error?: string;
}

const initialState: LessonState = {
  currentLesson: null,
  metadata: [],
  selectedDayIndex: null,
  loading: false,
};

const lessonSlice = createSlice({
  name: "lesson",
  initialState,
  reducers: {
    setLesson(state, action: PayloadAction<Lesson>) {
      state.currentLesson = action.payload;
    },
    setMetadata(state, action: PayloadAction<LessonMetadata[]>) {
      state.metadata = action.payload;
    },
    setSelectedDay(state, action: PayloadAction<number>) {
      state.selectedDayIndex = action.payload;
    },
    setLessonLoading(state, action: PayloadAction<boolean>) {
      state.loading = action.payload;
    },
    setLessonError(state, action: PayloadAction<string | undefined>) {
      state.error = action.payload;
    },
  },
});

export const {
  setLesson,
  setMetadata,
  setSelectedDay,
  setLessonLoading,
  setLessonError,
} = lessonSlice.actions;

export default lessonSlice.reducer;
