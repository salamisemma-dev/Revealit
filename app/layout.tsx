import type {Metadata} from 'next';
import './globals.css';
import {Header,Footer} from '@/components/reveal';
const siteUrl='https://salamisemma-dev.github.io/Revealit/';
export const metadata:Metadata={title:{default:'Reveal It | Discipline builds destiny',template:'%s | Reveal It'},description:'Reveal It verbindt training, coaching en persoonlijke ontwikkeling. Ontdek Reveal Fit en Reveal It Foundation.',metadataBase:new URL(siteUrl),icons:{icon:'/favicon.svg',shortcut:'/favicon.svg'}};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="nl"><head><script type="application/ld+json" dangerouslySetInnerHTML={{__html:JSON.stringify({'@context':'https://schema.org','@type':'WebSite',name:'Reveal It',url:siteUrl,description:'Training, coaching en persoonlijke ontwikkeling via Reveal Fit en Reveal It Foundation.',inLanguage:'nl'})}}/></head><body><a className="skip-link" href="#main">Ga naar inhoud</a><Header/>{children}<Footer/></body></html>}
