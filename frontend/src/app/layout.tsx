import "./globals.css";

import type React from "react";
import { Inter } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/theme/theme-provider";
import Header from "@/components/header";
import Footer from "@/components/footer";
import { ReduxProvider } from "@/store/provider";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider attribute="class" defaultTheme="light" enableSystem disableTransitionOnChange>
          <div className="flex min-h-screen flex-col">
            <ReduxProvider>
              <Header />
              <main className="flex-1">{children}</main>
              <Footer />
            </ReduxProvider>
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
