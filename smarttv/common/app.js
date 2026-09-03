(() => {
  const state={query:'música',items:[],history:JSON.parse(localStorage.getItem('miyt_history')||'[]'),apiBase:null};
  const $=id=>document.getElementById(id);
  const grid=$('grid'),empty=$('empty'),sectionTitle=$('sectionTitle'),providerLabel=$('providerLabel');
  const searchOverlay=$('searchOverlay'),searchInput=$('searchInput'),playerOverlay=$('playerOverlay');
  const video=$('videoPlayer'),frame=$('youtubeFrame');
  const FALLBACKS=['https://yewtu.be','https://inv.nadeko.net','https://invidious.nerdvpn.de'];

  function focusables(scope=document){return [...scope.querySelectorAll('.focusable:not([disabled])')].filter(el=>el.offsetParent!==null)}
  function focusFirst(scope=document){const a=focusables(scope);if(a.length)setTimeout(()=>a[0].focus(),40)}
  function closestInDirection(current,key){
    const all=focusables();if(!current||!all.includes(current))return all[0];
    const c=current.getBoundingClientRect(),cx=c.left+c.width/2,cy=c.top+c.height/2;let best=null,bscore=1e9;
    for(const el of all){if(el===current)continue;const r=el.getBoundingClientRect(),x=r.left+r.width/2,y=r.top+r.height/2,dx=x-cx,dy=y-cy;
      const ok=key==='ArrowLeft'?dx<-5:key==='ArrowRight'?dx>5:key==='ArrowUp'?dy<-5:dy>5;if(!ok)continue;
      const primary=(key==='ArrowLeft'||key==='ArrowRight')?Math.abs(dx):Math.abs(dy);const cross=(key==='ArrowLeft'||key==='ArrowRight')?Math.abs(dy):Math.abs(dx);const score=primary+cross*2.2;
      if(score<bscore){bscore=score;best=el;}}
    return best||current;
  }
  document.addEventListener('keydown',e=>{
    const code=e.keyCode||e.which,key=e.key;
    if([37,38,39,40].includes(code)||['ArrowLeft','ArrowUp','ArrowRight','ArrowDown'].includes(key)){
      e.preventDefault();const map={37:'ArrowLeft',38:'ArrowUp',39:'ArrowRight',40:'ArrowDown'};const next=closestInDirection(document.activeElement,map[code]||key);if(next)next.focus();return;
    }
    if(code===13||key==='Enter'){const el=document.activeElement;if(el&&el.click){e.preventDefault();el.click();}return;}
    if(code===10009||code===461||key==='Escape'){
      if(!playerOverlay.classList.contains('hidden')){closePlayer();e.preventDefault();return;}
      if(!searchOverlay.classList.contains('hidden')){closeSearch();e.preventDefault();return;}
      if(confirm('¿Salir de Mi YouTube TV?'))window.MIYT_PLATFORM.exit();
    }
  });

  async function chooseApi(){
    const candidates=[];
    try{const r=await fetch('https://api.invidious.io/instances.json',{cache:'no-store'});const data=await r.json();data.forEach(([host,meta])=>{if(meta&&meta.api&&meta.cors&&meta.type==='https')candidates.push('https://'+host);});}catch(e){}
    candidates.push(...FALLBACKS);
    for(const base of [...new Set(candidates)]){
      try{const r=await fetch(base+'/api/v1/search?q=mi%20youtube&type=video&page=1&sort_by=relevance');if(r.ok){state.apiBase=base;providerLabel.textContent='Proveedor remoto activo';return base;}}catch(e){}
    }
    throw new Error('No remote provider');
  }

  async function search(q){
    state.query=q;sectionTitle.textContent='Resultados: '+q;grid.innerHTML='';empty.classList.add('hidden');$('networkStatus').textContent='Conectando…';
    try{
      if(!state.apiBase)await chooseApi();
      const url=state.apiBase+'/api/v1/search?q='+encodeURIComponent(q)+'&type=video&page=1&sort_by=relevance';
      const r=await fetch(url);if(!r.ok)throw new Error('search '+r.status);const items=await r.json();
      state.items=(Array.isArray(items)?items:[]).filter(x=>x.type==='video'||x.videoId).slice(0,24);render();$('networkStatus').textContent='Internet ✓';$('networkStatus').style.color='#8f8';
    }catch(e){state.apiBase=null;empty.classList.remove('hidden');$('networkStatus').textContent='Sin conexión';$('networkStatus').style.color='#f88';}
  }
  function thumb(item){return item.videoThumbnails?.find(x=>x.quality==='medium')?.url||item.videoThumbnails?.[0]?.url||('https://i.ytimg.com/vi/'+item.videoId+'/hqdefault.jpg')}
  function duration(sec){sec=Number(sec||0);const m=Math.floor(sec/60),s=sec%60;return m+':'+String(s).padStart(2,'0')}
  function escapeHtml(s){return String(s||'').replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]||c))}
  function render(){
    grid.innerHTML='';state.items.forEach((item,i)=>{const b=document.createElement('button');b.className='card focusable';b.dataset.index=i;b.innerHTML=`<img class="thumb" src="${thumb(item)}" alt=""><span class="duration">${duration(item.lengthSeconds)}</span><div class="card-title">${escapeHtml(item.title||'Video')}</div><div class="card-meta">${escapeHtml(item.author||'Canal')} · ${item.viewCountText||''}</div>`;b.onclick=()=>play(item);grid.appendChild(b);});focusFirst(grid);
  }
  async function play(item){
    playerOverlay.classList.remove('hidden');$('playerTitle').textContent=item.title||'Video';$('playerChannel').textContent=item.author||'';frame.classList.add('hidden');video.classList.remove('hidden');
    state.history=[{videoId:item.videoId,title:item.title,author:item.author,thumb:thumb(item),ts:Date.now()},...state.history.filter(x=>x.videoId!==item.videoId)].slice(0,50);localStorage.setItem('miyt_history',JSON.stringify(state.history));
    try{if(!state.apiBase)await chooseApi();const r=await fetch(state.apiBase+'/api/v1/videos/'+encodeURIComponent(item.videoId));const info=await r.json();const formats=(info.formatStreams||[]).filter(f=>f.url);const pick=formats.find(f=>/720p|480p/.test(f.qualityLabel||f.quality))||formats[0];if(!pick)throw new Error('no stream');video.src=pick.url;video.onerror=()=>fallbackFrame(item.videoId);await video.play().catch(()=>fallbackFrame(item.videoId));}catch(e){fallbackFrame(item.videoId)}
    setTimeout(()=>$('closePlayer').focus(),100);
  }
  function fallbackFrame(id){try{video.pause()}catch(e){}video.removeAttribute('src');video.load();video.classList.add('hidden');frame.classList.remove('hidden');frame.src='https://www.youtube-nocookie.com/embed/'+encodeURIComponent(id)+'?autoplay=1&rel=0';}
  function closePlayer(){try{video.pause()}catch(e){}video.removeAttribute('src');video.load();frame.src='about:blank';playerOverlay.classList.add('hidden');focusFirst(grid)}
  function openSearch(){searchOverlay.classList.remove('hidden');searchInput.value=state.query;setTimeout(()=>searchInput.focus(),60)}
  function closeSearch(){searchOverlay.classList.add('hidden');$('searchBox').focus()}
  function showHistory(){sectionTitle.textContent='Historial';state.items=state.history.map(x=>({videoId:x.videoId,title:x.title,author:x.author,videoThumbnails:[{url:x.thumb}],lengthSeconds:0,viewCountText:''}));render()}
  $('searchBox').onclick=openSearch;$('doSearch').onclick=()=>{const q=searchInput.value.trim();if(q){closeSearch();search(q)}};$('cancelSearch').onclick=closeSearch;$('closePlayer').onclick=closePlayer;
  document.querySelectorAll('.chip').forEach(ch=>ch.onclick=()=>{document.querySelectorAll('.chip').forEach(x=>x.classList.remove('selected'));ch.classList.add('selected');search(ch.dataset.query)});
  document.querySelectorAll('.navitem').forEach(n=>n.onclick=()=>{const a=n.dataset.action;if(a==='home')search('música');else if(a==='search')openSearch();else if(a==='history')showHistory();else if(a==='settings')alert('Mi YouTube TV 1.0.0\nLG webOS + Samsung Tizen\nContenido remoto por Internet.');});
  window.addEventListener('online',()=>{$('networkStatus').textContent='Internet ✓'});window.addEventListener('offline',()=>{$('networkStatus').textContent='Sin conexión'});
  search('música');
})();
