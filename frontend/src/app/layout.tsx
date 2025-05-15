import "./globals.css";
import { ReactNode } from "react";
import { ReduxProvider } from "@/store/provider";
import Header from "@/components/header";
import Footer from "@/components/footer";
import { ThemeProvider } from "@/theme/theme-provider";

export const metadata = {
  title: "Sabbath School App",
  description: "Interactive daily Bible study experience",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <ThemeProvider
          attribute="class"
          defaultTheme="light"
          enableSystem
          disableTransitionOnChange
        >
          <div className="flex min-h-screen flex-col">
            <Header />
            <ReduxProvider>{children}</ReduxProvider>
            <Footer />
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
