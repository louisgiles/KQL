import type { Metadata } from 'next';
import './globals.css';
export const metadata:Metadata={title:'The Blacklist — Hunting Index',description:'A shared threat hunting workspace for Microsoft Sentinel. Cited intelligence, practical KQL and shared actioned intelligence.',icons:{icon:'/favicon.svg'}};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>;}
