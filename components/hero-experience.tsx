'use client';

import {useEffect, useRef, type PointerEvent} from 'react';
import {Arrow, LinkButton} from '@/components/reveal';

export function HeroExperience(){
  const sectionRef=useRef<HTMLElement>(null);
  const desktopRef=useRef<HTMLVideoElement>(null);
  const mobileRef=useRef<HTMLVideoElement>(null);
  const pointer=useRef({x:0,y:0});

  useEffect(()=>{
    const section=sectionRef.current;
    if(!section) return;
    const desktopVideo=desktopRef.current;
    const mobileVideo=mobileRef.current;
    const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
    const mobile=window.matchMedia('(max-width: 640px)');
    let frame=0;
    let visible=false;
    const current={x:0,y:0,progress:0};

    const activeVideo=()=>mobile.matches?mobileVideo:desktopVideo;
    const ensureSource=(video:HTMLVideoElement|null)=>{
      if(!video||video.dataset.ready) return;
      video.src=video.dataset.src||'';
      video.preload='metadata';
      video.dataset.ready='true';
      video.load();
    };
    const setPlayback=(play:boolean)=>{
      const video=activeVideo();
      [desktopVideo,mobileVideo].forEach(item=>{if(item&&item!==video)item.pause();});
      if(!video||reduced.matches) return;
      if(play){ensureSource(video);void video.play().catch(()=>{});}
      else video.pause();
    };
    const render=()=>{
      const rect=section.getBoundingClientRect();
      const travel=Math.max(rect.height-window.innerHeight,1);
      const progress=Math.max(0,Math.min(1,-rect.top/travel));
      current.x+=(pointer.current.x-current.x)*.065;
      current.y+=(pointer.current.y-current.y)*.065;
      current.progress=progress;
      const p=current.progress;
      const x=current.x;
      const y=current.y;
      section.style.cssText=[
        `--film-scale:${(.965+p*.045).toFixed(4)}`,
        `--film-rx:${(-y).toFixed(2)}deg`,`--film-ry:${(x*1.5).toFixed(2)}deg`,
        `--video-scale:${(1.02+p*.035).toFixed(4)}`,
        `--video-x:${(-x*12).toFixed(2)}px`,`--video-y:${(-y*9).toFixed(2)}px`,
        `--kicker-opacity:${Math.max(0,1-p*2.2).toFixed(3)}`,`--kicker-y:${(-p*30).toFixed(2)}px`,
        `--title-opacity:${Math.max(0,1-p*1.8).toFixed(3)}`,
        `--title-x:${(-x*7).toFixed(2)}px`,`--title-y:${(-p*85-y*4).toFixed(2)}px`,`--title-y-mobile:${(-p*55).toFixed(2)}px`,`--title-scale:${(1-p*.06).toFixed(4)}`,
        `--lead-opacity:${Math.max(0,1-p*2.35).toFixed(3)}`,`--lead-y:${(-p*50).toFixed(2)}px`,`--lead-y-mobile:${(-p*35).toFixed(2)}px`,
        `--shift-opacity:${Math.max(0,Math.min(1,(p-.46)*3.8)).toFixed(3)}`,`--shift-y:${((1-p)*70).toFixed(2)}px`
      ].join(';');
      if(visible) frame=requestAnimationFrame(render);
    };
    const handleViewportChange=()=>setPlayback(visible);
    const observer=new IntersectionObserver(([entry])=>{
      visible=entry.isIntersecting;
      setPlayback(visible);
      if(visible&&!frame) frame=requestAnimationFrame(render);
      if(!visible&&frame){cancelAnimationFrame(frame);frame=0;}
    },{threshold:.02});
    observer.observe(section);
    mobile.addEventListener('change',handleViewportChange);
    return()=>{observer.disconnect();mobile.removeEventListener('change',handleViewportChange);cancelAnimationFrame(frame);desktopVideo?.pause();mobileVideo?.pause();};
  },[]);

  function move(event:PointerEvent<HTMLElement>){
    if(event.pointerType==='touch') return;
    const rect=event.currentTarget.getBoundingClientRect();
    pointer.current.x=((event.clientX-rect.left)/rect.width-.5)*2;
    pointer.current.y=((event.clientY-rect.top)/rect.height-.5)*2;
  }

  return <section ref={sectionRef} className="cinematic-hero" onPointerMove={move} onPointerLeave={()=>{pointer.current={x:0,y:0};}} aria-labelledby="home-title">
    <div className="hero-sticky">
      <div className="hero-film" aria-hidden="true">
        <video ref={desktopRef} className="film-desktop" poster="/media/hero-poster-desktop.webp" muted playsInline loop preload="none" data-src="/media/hero-cinematic-desktop.mp4"/>
        <video ref={mobileRef} className="film-mobile" poster="/media/hero-poster-mobile.webp" muted playsInline loop preload="none" data-src="/media/hero-cinematic-mobile.mp4"/>
        <div className="film-wash"/><div className="film-grain"/><div className="film-frame"/>
      </div>
      <div className="hero-content wrap">
        <p className="hero-kicker"><span/>Jouw groei begint hier</p>
        <h1 id="home-title"><span>Discipline</span><span>builds</span><em>destiny.</em></h1>
        <div className="hero-lead"><p>Sterker in je lijf. Steviger in het leven.<br/>Training, voeding en coaching voor jouw ontwikkeling.</p><div className="actions"><LinkButton href="/reveal-fit">Ontdek Reveal Fit</LinkButton><a className="hero-foundation-link" href="/foundation">Onze Foundation <Arrow/></a></div></div>
        <p className="hero-shift" aria-hidden="true"><span>kracht in jezelf</span><em>ruimte voor een ander</em></p>
      </div>
    </div>
  </section>;
}
