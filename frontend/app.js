/* EMOTION VOICE AI — app.js FINAL */

const EC={happy:'#F9D849',sad:'#6C7EE1',angry:'#FF6B6B',anxious:'#F06292',curious:'#A78BFA',fearful:'#90CAF9',disgusted:'#A5D6A7',surprised:'#FFD54F',neutral:'#A594FF',calm:'#4DD9C0',warm:'#F06292',empathetic:'#F06292',reflective:'#6C7EE1',attentive:'#4DD9C0',analytical:'#A594FF',engaged:'#F9D849'};
const EMO_EMOJI={happy:'😊',sad:'😢',angry:'😠',anxious:'😰',curious:'🤔',fearful:'😨',disgusted:'🤢',surprised:'😮',neutral:'😐',calm:'😌',warm:'🤗'};

/* AUTH */
const Auth={
  getUsers(){try{return JSON.parse(localStorage.getItem('eva_users')||'{}')}catch(e){return{}}},
  saveUsers(u){localStorage.setItem('eva_users',JSON.stringify(u))},
  currentEmail(){return localStorage.getItem('eva_current')||null},
  getUser(){const e=this.currentEmail();if(!e)return null;return this.getUsers()[e]||null},
  signup(name,email,pass){
    if(!name||!email||pass.length<6)return{ok:false,msg:'Fill all fields (password min 6 chars).'};
    if(!/\S+@\S+\.\S+/.test(email))return{ok:false,msg:'Enter a valid email address.'};
    const u=this.getUsers();
    if(u[email])return{ok:false,msg:'Email already registered. Sign in instead.'};
    u[email]={name,email,pass:btoa(pass),joined:new Date().toISOString()};
    this.saveUsers(u);localStorage.setItem('eva_current',email);
    return{ok:true,user:u[email]};
  },
  login(email,pass){
    if(!email||!pass)return{ok:false,msg:'Please enter email and password.'};
    const u=this.getUsers();
    if(!u[email])return{ok:false,msg:'No account found. Please sign up first.'};
    if(u[email].pass!==btoa(pass))return{ok:false,msg:'Incorrect password. Please try again.'};
    localStorage.setItem('eva_current',email);return{ok:true,user:u[email]};
  },
  logout(){localStorage.removeItem('eva_current');window.location.href='login.html';},
  require(){
    const e=this.currentEmail();if(!e){window.location.href='login.html';return null;}
    const u=this.getUsers();if(!u[e]){window.location.href='login.html';return null;}
    return u[e];
  },
  getData(email,key){try{return JSON.parse(localStorage.getItem('eva_'+key+'_'+email)||'[]')}catch(e){return[]}},
  setData(email,key,val){localStorage.setItem('eva_'+key+'_'+email,JSON.stringify(val))}
};

/* NAV */
function renderNav(user){
  const el=document.getElementById('nav-user-area');if(!el||!user)return;
  el.innerHTML='<div class="nav-user"><div class="uavatar">'+user.name[0].toUpperCase()+'</div><span>'+user.name.split(' ')[0]+'</span></div><button class="nav-btn" onclick="Auth.logout()">Sign out</button>';
}

/* PARTICLES */
function initParticles(){
  const canvas=document.getElementById('bg-canvas');if(!canvas)return;
  const ctx=canvas.getContext('2d');let W,H,pts=[];
  const C=['rgba(124,110,245,','rgba(240,96,138,','rgba(61,207,186,'];
  function resize(){W=canvas.width=window.innerWidth;H=canvas.height=window.innerHeight;}
  window.addEventListener('resize',resize);resize();
  class P{constructor(){this.x=Math.random()*W;this.y=Math.random()*H;this.vx=(Math.random()-.5)*.3;this.vy=(Math.random()-.5)*.3;this.r=Math.random()*1.5+.5;this.c=C[Math.floor(Math.random()*C.length)];this.a=Math.random()*.4+.1;}update(){this.x+=this.vx;this.y+=this.vy;if(this.x<0||this.x>W)this.vx*=-1;if(this.y<0||this.y>H)this.vy*=-1;}draw(){ctx.beginPath();ctx.arc(this.x,this.y,this.r,0,Math.PI*2);ctx.fillStyle=this.c+this.a+')';ctx.fill();}}
  for(let i=0;i<80;i++)pts.push(new P());
  function lines(){for(let i=0;i<pts.length;i++)for(let j=i+1;j<pts.length;j++){const dx=pts[i].x-pts[j].x,dy=pts[i].y-pts[j].y,d=Math.sqrt(dx*dx+dy*dy);if(d<120){ctx.beginPath();ctx.moveTo(pts[i].x,pts[i].y);ctx.lineTo(pts[j].x,pts[j].y);ctx.strokeStyle='rgba(124,110,245,'+(.06*(1-d/120))+')';ctx.lineWidth=.5;ctx.stroke();}}}
  function loop(){ctx.clearRect(0,0,W,H);pts.forEach(p=>{p.update();p.draw();});lines();requestAnimationFrame(loop);}loop();
}

/* TTS — Browser fallback when Murf not available */
const TTS={
  synth:window.speechSynthesis,voices:[],enabled:false,speaking:false,selectedIdx:0,
  TUNING:{happy:{rate:+.10,pitch:+.15},sad:{rate:-.15,pitch:-.10},angry:{rate:+.15,pitch:+.05},anxious:{rate:-.05,pitch:+.05},curious:{rate:+.05,pitch:+.10},fearful:{rate:-.10,pitch:-.05},surprised:{rate:+.10,pitch:+.20},disgusted:{rate:-.05,pitch:-.10},neutral:{rate:0,pitch:0}},
  loadVoices(){return new Promise(r=>{const l=()=>{const v=this.synth.getVoices();if(v.length){this.voices=v;r(v);}};l();this.synth.onvoiceschanged=l;setTimeout(r,1500);})},
  bestVoice(){const v=this.voices,p=[v=>/en-US/i.test(v.lang)&&/female|woman|zira|samantha|google us/i.test(v.name),v=>/en-GB/i.test(v.lang)&&/female|woman|hazel/i.test(v.name),v=>/en/i.test(v.lang)&&/female|woman/i.test(v.name),v=>/en-US/i.test(v.lang),v=>/en/i.test(v.lang),v=>true];for(const f of p){const x=v.find(f);if(x)return v.indexOf(x);}return 0;},
  populateSelect(id='voice-select'){const s=document.getElementById(id);if(!s)return;s.innerHTML='';this.voices.forEach((v,i)=>{const o=document.createElement('option');o.value=i;o.textContent=v.name+' ('+v.lang+')';s.appendChild(o);});const b=this.bestVoice();this.selectedIdx=b;s.value=b;},
  speak(text,emotion='neutral',onStart,onEnd){
    if(!this.enabled||!text)return;this.synth.cancel();
    const u=new SpeechSynthesisUtterance(text),v=this.voices[this.selectedIdx]||this.voices[0],t=this.TUNING[emotion]||this.TUNING.neutral;
    const br=parseFloat(document.getElementById('rate-slider')?.value||.95),bp=parseFloat(document.getElementById('pitch-slider')?.value||1.05);
    if(v)u.voice=v;u.lang=v?.lang||'en-US';u.rate=Math.max(.5,Math.min(2,br+t.rate));u.pitch=Math.max(.1,Math.min(2,bp+t.pitch));u.volume=1;
    u.onstart=()=>{this.speaking=true;onStart?.();};u.onend=()=>{this.speaking=false;onEnd?.();};u.onerror=()=>{this.speaking=false;onEnd?.();};
    this.synth.speak(u);
  },
  stop(){this.synth.cancel();this.speaking=false;}
};

/* SPEECH RECOGNITION */
const SR={
  recognition:null,active:false,
  init(){const C=window.SpeechRecognition||window.webkitSpeechRecognition;if(!C)return false;this.recognition=new C();this.recognition.continuous=false;this.recognition.interimResults=false;this.recognition.lang='en-US';this.recognition.onresult=e=>{const t=e.results[0][0].transcript;const i=document.getElementById('msg-input');if(i)i.value=t;this.stop();setTimeout(()=>window.sendMsg&&sendMsg(),200);};this.recognition.onerror=()=>this.stop();this.recognition.onend=()=>this.stop();return true;},
  toggle(){if(!this.recognition){alert('Use Chrome or Edge for mic support.');return;}if(this.active)this.stop();else{this.active=true;document.getElementById('mic-btn')?.classList.add('recording');try{this.recognition.start();}catch(e){this.stop();}}},
  stop(){this.active=false;document.getElementById('mic-btn')?.classList.remove('recording');try{this.recognition?.stop();}catch(e){}}
};

/* UTILS */
const fmt=d=>d.toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'});
const today=()=>new Date().toLocaleDateString([],{weekday:'long',month:'long',day:'numeric'});
const waveHTML=n=>{const dl=[0,.1,.2,.15,.25,.05,.3,.18];return Array.from({length:n},(_,i)=>'<span style="animation-delay:'+dl[i%dl.length]+'s"></span>').join('');};

document.addEventListener('DOMContentLoaded',initParticles); 