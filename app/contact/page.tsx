import type {Metadata} from 'next';
import {Breadcrumb,SectionLabel} from '@/components/reveal';
import {ContactForm} from '@/components/contact-form';
export const metadata:Metadata={title:'Kennismaken',description:'Bereid je kennismaking, zakelijke aanvraag of samenwerking met Reveal It voor.'};
export default function Contact(){return <main id="main" className="wrap contact-page"><div><Breadcrumb current="Kennismaken"/><SectionLabel>We beginnen bij jouw vraag</SectionLabel><h1>Wat wil jij<br/><em>in beweging zetten?</em></h1><p className="lead">Of je nu wilt trainen, iets voor je medewerkers zoekt of wilt samenwerken met de Foundation: vertel waar je aan denkt.</p><div className="contact-note"><p className="eyebrow plain">OVER DEZE PREVIEW</p><p>Je kunt hier een bericht voorbereiden en bewaren. Het wordt nog niet naar Reveal It verstuurd. De contactgegevens worden voor de lancering toegevoegd.</p></div></div><ContactForm/></main>}
