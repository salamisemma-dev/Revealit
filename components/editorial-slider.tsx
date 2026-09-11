'use client';

import {useId, useRef, useState, type KeyboardEvent, type PointerEvent} from 'react';
import type {EditorialSlide} from '@/data/editorial-slides';

export function EditorialSlider({slides,label}:{slides:EditorialSlide[];label:string}){
  const [active,setActive]=useState(0);
  const startX=useRef<number|null>(null);
  const titleId=useId();
  const show=(index:number)=>setActive((index+slides.length)%slides.length);
  const onKeyDown=(event:KeyboardEvent<HTMLElement>)=>{
    if(event.key==='ArrowLeft'){event.preventDefault();show(active-1);}
    if(event.key==='ArrowRight'){event.preventDefault();show(active+1);}
  };
  const pointerDown=(event:PointerEvent<HTMLElement>)=>{startX.current=event.clientX;};
  const pointerUp=(event:PointerEvent<HTMLElement>)=>{
    if(startX.current===null) return;
    const distance=event.clientX-startX.current;
    if(Math.abs(distance)>45) show(active+(distance<0?1:-1));
    startX.current=null;
  };

  return <section className="editorial-slider" aria-roledescription="carousel" aria-label={label} aria-labelledby={titleId} tabIndex={0} onKeyDown={onKeyDown} onPointerDown={pointerDown} onPointerUp={pointerUp}>
    <h2 id={titleId} className="sr-only">{label}</h2>
    <div className="editorial-slides" aria-live="polite">{slides.map((slide,index)=><article className={`editorial-slide ${slide.image?'has-image':''} tone-${slide.tone??'image'} ${index===active?'is-active':''}`} aria-hidden={index!==active} key={slide.eyebrow}>{slide.image?<img src={slide.image} alt={slide.alt??''} width="1536" height="1024" loading={index===0?'eager':'lazy'}/>:null}<div className="slide-shade"/><div className="slide-copy"><p>{slide.eyebrow}</p><h3>{slide.title}<br/><em>{slide.emphasis}</em></h3><span>{slide.body}</span></div></article>)}</div>
    <div className="slider-controls"><div className="slider-buttons"><button type="button" onClick={()=>show(active-1)} aria-label="Vorige dia">←</button><button type="button" onClick={()=>show(active+1)} aria-label="Volgende dia">→</button></div></div>
  </section>;
}
