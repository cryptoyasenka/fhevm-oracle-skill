import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AsyncRevealVault — fhevm-oracle demo",
  description:
    "Encrypted, time-locked reveal on Zama FHEVM Sepolia. Built on the fhevm-oracle skill.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
