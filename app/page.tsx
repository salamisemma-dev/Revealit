import { Arrow, LinkButton, SectionLabel } from '@/components/reveal';
import {HeroExperience} from '@/components/hero-experience';
import {growthSteps,homeJourneys} from '@/data/home';
export default function Home() {
return <main id="main">
<HeroExperience/>
<section id="over" className="manifesto wrap section-space"><SectionLabel>De mens als geheel</SectionLabel><div className="manifesto-title"><h2>Eén mens.<br/><em>Meerdere lagen.</em></h2><span aria-hidden="true">01</span></div><div className="manifesto-copy"><p>Een sterker lichaam kan het begin zijn van meer zelfvertrouwen. Een vaste routine kan je dag richting geven.</p><p>Reveal It verbindt beweging, coaching en persoonlijke ontwikkeling. Niet als snelle oplossing, maar als basis waarop je zelf verder kunt bouwen.</p></div></section>
<section className="worlds section-space"><div className="wrap worlds-heading"><SectionLabel>Twee richtingen. Eén basis.</SectionLabel><h2>Kies waar jouw<br/><em>beweging begint.</em></h2></div><div className="world-grid">{homeJourneys.map(journey=><a className={`world ${journey.className}`} href={journey.href} key={journey.href}><div className="world-shade"/><div className="world-index">{journey.index}</div><div className="world-copy"><p>{journey.audience}</p><h3>{journey.name} <em>{journey.emphasis}</em></h3><span>{journey.themes}</span><b>{journey.cta} <Arrow/></b></div></a>)}</div></section>
<section className="approach wrap section-space"><div><SectionLabel>Zo kijken wij naar groei</SectionLabel><h2>Kleine stappen.<br/><em>Een eigen richting.</em></h2></div><div className="steps">{growthSteps.map(step=><article key={step.number}><span>{step.number}</span><div><h3>{step.title}</h3><p>{step.copy}</p></div></article>)}</div></section>
<section className="closing"><div className="wrap"><SectionLabel>De eerste stap is van jou</SectionLabel><h2>Geef je groei<br/><em>een richting.</em></h2><LinkButton href="/contact/" light>Bereid je kennismaking voor</LinkButton></div></section>
</main>}
