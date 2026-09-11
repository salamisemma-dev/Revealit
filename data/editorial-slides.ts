export interface EditorialSlide {
  eyebrow:string;
  title:string;
  emphasis:string;
  body:string;
  image?:string;
  alt?:string;
  tone?:'cream'|'sand'|'dark';
}

export const fitSlides:EditorialSlide[]=[
  {eyebrow:'01 / Begin bij jezelf',title:'Kracht krijgt',emphasis:'richting.',body:'Training die aansluit op jouw niveau, doelen en ritme.',image:'/images/hero.webp',alt:'Een sporter kijkt uit over een rustige natuurlijke omgeving.'},
  {eyebrow:'02 / Bouw een ritme',title:'Kleine keuzes.',emphasis:'Blijvend effect.',body:'Structuur maakt vooruitgang herkenbaar en helpt je om door te gaan.',tone:'sand'},
  {eyebrow:'03 / Neem het mee',title:'Sterker in',emphasis:'je dagelijks leven.',body:'Beweging, voeding en coaching vormen samen één praktische basis.',tone:'dark'}
];

export const foundationSlides:EditorialSlide[]=[
  {eyebrow:'01 / Gezien worden',title:'Talent verdient',emphasis:'ruimte.',body:'Een veilige omgeving om te ontdekken, te oefenen en vertrouwen op te bouwen.',image:'/images/community.webp',alt:'Een coach spreekt buiten met een groep jongvolwassenen.'},
  {eyebrow:'02 / Vertrouwen door doen',title:'Ontdekken.',emphasis:'Oefenen. Groeien.',body:'Praktische ervaringen helpen vaardigheden zichtbaar en bruikbaar te maken.',tone:'cream'},
  {eyebrow:'03 / Samen verder',title:'Kansen ontstaan',emphasis:'niet alleen.',body:'We verbinden mensen, kennis en mogelijkheden rond persoonlijke ontwikkeling.',tone:'dark'}
];
