export interface HomeJourney {
  href:string;
  className:'world-fit'|'world-foundation';
  index:string;
  audience:string;
  name:string;
  emphasis:string;
  themes:string;
  cta:string;
}

export const homeJourneys:HomeJourney[]=[
  {href:'/reveal-fit/',className:'world-fit',index:'01 / FIT',audience:'Voor jezelf & organisaties',name:'Reveal',emphasis:'Fit',themes:'Training · Voeding · Coaching',cta:'Ontdek jouw traject'},
  {href:'/foundation/',className:'world-foundation',index:'02 / FOUNDATION',audience:'Voor talent & kansen',name:'Reveal It',emphasis:'Foundation',themes:'Zelfvertrouwen · Vaardigheden · Perspectief',cta:'Bekijk onze missie'}
];

export const growthSteps=[
  {number:'01',title:'We beginnen bij jou',copy:'Wat wil je veranderen? We kijken naar je doelen, je ritme en wat je nu in de weg zit.'},
  {number:'02',title:'We brengen het in beweging',copy:'Training en begeleiding geven je iets concreets om mee te beginnen.'},
  {number:'03',title:'Je bouwt verder',copy:'Door te oefenen ontwikkel je structuur en vaardigheden die je zelf kunt blijven gebruiken.'}
];
