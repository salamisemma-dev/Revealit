export function prepareMessage(input) {
  if (!input || typeof input !== 'object') throw new Error('Een naam en vraag zijn nodig.');
  const {name, message, topic = 'Persoonlijke begeleiding', email = ''} = input;
  if (typeof name !== 'string' || !name.trim() || name.length > 100) throw new Error('Vul een naam van maximaal 100 tekens in.');
  if (typeof message !== 'string' || message.trim().length < 10 || message.length > 2500) throw new Error('Schrijf een vraag van 10 tot 2500 tekens.');
  if (typeof topic !== 'string' || !topic.trim() || topic.length > 100) throw new Error('Kies een geldig onderwerp.');
  if (typeof email !== 'string' || email.length > 150 || (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))) throw new Error('Vul een geldig e-mailadres in of laat dit veld leeg.');
  return `Aan: Reveal It (ontvanger nog toe te voegen)\nOnderwerp: ${topic.trim()}\nVan: ${name.trim()}${email?'\nE-mail: '+email:''}\n\n${message.trim()}\n\nDit is een conceptbericht. Het is niet verstuurd.`;
}
