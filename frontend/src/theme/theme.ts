import { createTheme } from "@mui/material/styles";

// Light Theme
export const theme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: "#2E5EAA",
      light: "#5D85D6",
      dark: "#1C3D72",
      contrastText: "#FFFFFF",
    },
    secondary: {
      main: "#F4A261",
      light: "#F6B987",
      dark: "#D97C2B",
      contrastText: "#000000",
    },
    background: {
      default: "#FAFAFA",
      paper: "#FFFFFF",
    },
    text: {
      primary: "#212121",
      secondary: "#616161",
    },
    divider: "#E0E0E0",
    success: {
      main: "#388E3C",
    },
    error: {
      main: "#D32F2F",
    },
    info: {
      main: "#1976D2",
    },
  },
  typography: {
    fontFamily: "Inter, Roboto, Arial, sans-serif",
  },
});

// Dark Theme
export const darkTheme = createTheme({
  palette: {
    mode: "dark",
    primary: {
      main: "#90CAF9",
      light: "#E3F2FD",
      dark: "#42A5F5",
      contrastText: "#000000",
    },
    secondary: {
      main: "#F4A261",
      light: "#F6B987",
      dark: "#D97C2B",
      contrastText: "#000000",
    },
    background: {
      default: "#121212",
      paper: "#1E1E1E",
    },
    text: {
      primary: "#FFFFFF",
      secondary: "#B0B0B0",
      disabled: "#757575",
    },
    divider: "#333333",
    success: {
      main: "#66BB6A",
    },
    error: {
      main: "#EF5350",
    },
    info: {
      main: "#29B6F6",
    },
  },
  typography: {
    fontFamily: "Inter, Roboto, Arial, sans-serif",
  },
});
