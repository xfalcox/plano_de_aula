import { spawn } from 'node:child_process';
import { readdir, readFile, writeFile, mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const profile=await mkdtemp(path.join(tmpdir(),'plano_verificacao_'));
const browser=spawn('chromium',['--headless','--no-sandbox','--disable-gpu','--disable-dev-shm-usage','--remote-debugging-port=9337','--remote-allow-origins=*',`--user-data-dir=${profile}`,'about:blank'],{stdio:'ignore'});
const results=[];
let ws;
try {
  let targets;
  for(let attempt=0;attempt<100;attempt++){
    try{targets=await (await fetch('http://127.0.0.1:9337/json')).json();break;}catch{await new Promise(r=>setTimeout(r,100));}
  }
  if(!targets)throw new Error('Chromium não iniciou');
  ws=new WebSocket(targets.find(t=>t.type==='page').webSocketDebuggerUrl);
  await new Promise((resolve,reject)=>{ws.addEventListener('open',resolve,{once:true});ws.addEventListener('error',reject,{once:true});});
  let seq=0;const pending=new Map();const errors=[];
  ws.addEventListener('message',event=>{const msg=JSON.parse(event.data);if(msg.id){const item=pending.get(msg.id);pending.delete(msg.id);if(msg.error)item.reject(new Error(JSON.stringify(msg.error)));else item.resolve(msg.result);}else if(msg.method==='Runtime.exceptionThrown'){errors.push(msg.params.exceptionDetails.text+': '+(msg.params.exceptionDetails.exception?.description||''));}});
  function cdp(method,params={}){return new Promise((resolve,reject)=>{const id=++seq;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}));});}
  async function evaluate(expression){const result=await cdp('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(result.exceptionDetails)throw new Error(JSON.stringify(result.exceptionDetails));return result.result.value;}
  async function open(file){const url=pathToFileURL(file).href;await cdp('Page.navigate',{url});for(let i=0;i<100;i++){if(await evaluate(`document.readyState==='complete'&&location.href===${JSON.stringify(url)}`))break;await new Promise(r=>setTimeout(r,50));}await evaluate('document.fonts.ready.then(()=>true)');}
  function assert(ok,label){results.push({label,ok:!!ok});if(!ok)throw new Error(label);}
  await cdp('Page.enable');await cdp('Runtime.enable');
  await cdp('Emulation.setDeviceMetricsOverride',{width:1280,height:1100,deviceScaleFactor:1,mobile:false});
  await cdp('Emulation.setEmulatedMedia',{media:'print'});
  const names=await readdir(path.join(root,'materiais/editaveis'));
  for(const name of names.filter(n=>n.endsWith('.html'))){
    await open(path.join(root,'materiais/editaveis',name));
    const metrics=await evaluate(`Array.from(document.querySelectorAll('.page')).map((page,i)=>{
      const r=page.getBoundingClientRect(),foot=page.querySelector('.footer').getBoundingClientRect();
      const walker=document.createTreeWalker(page,NodeFilter.SHOW_TEXT);let n;const bad=[];
      while(n=walker.nextNode()){if(!n.textContent.trim()||n.parentElement.closest('.footer'))continue;const range=document.createRange();range.selectNodeContents(n);for(const b of range.getClientRects()){if(b.bottom>foot.top-2||b.right>r.right+1||b.left<r.left-1)bad.push({text:n.textContent.slice(0,75),bottom:b.bottom-r.top,footer:foot.top-r.top,right:b.right-r.right});}}
      for(const el of page.querySelectorAll('.box, pre, table, .cards, .stage, .ticket, .flow, .layer, .answer')){const b=el.getBoundingClientRect();if(b.bottom>foot.top-2||b.right>r.right+1||b.left<r.left-1)bad.push({element:el.className||el.tagName,bottom:b.bottom-r.top,footer:foot.top-r.top});}
      return {page:i+1,bad};
    })`);
    const bad=metrics.filter(p=>p.bad.length);
    assert(bad.length===0,`${name}: sem texto cortado ou sobreposição ao rodapé ${JSON.stringify(bad)}`);
  }
  await cdp('Emulation.setEmulatedMedia',{media:'screen'});
  await cdp('Network.enable');
  await cdp('Network.emulateNetworkConditions',{offline:true,latency:0,downloadThroughput:0,uploadThroughput:0});
  await open(path.join(root,'materiais/demos/html.html'));
  assert(await evaluate(`document.querySelector('#link').getAttribute('href')==='#agenda'`),'HTML: destino inicial');
  await evaluate(`document.querySelector('#destino').value='local';document.querySelector('#destino').dispatchEvent(new Event('change'));document.querySelector('#link').click();`);
  await new Promise(r=>setTimeout(r,100));
  const htmlState=await evaluate(`({hash:location.hash,label:document.querySelector('#link').textContent,href:document.querySelector('#link').getAttribute('href')})`);
  assert(htmlState.hash==='#local'&&htmlState.label==='Ver local','HTML: troca de destino e navegação offline '+JSON.stringify(htmlState));
  await open(path.join(root,'materiais/demos/css.html'));
  await evaluate(`document.querySelector('#padding').value='32';document.querySelector('#padding').dispatchEvent(new Event('input'));document.querySelector('#margin').value='24';document.querySelector('#margin').dispatchEvent(new Event('input'));`);
  assert(await evaluate(`getComputedStyle(document.querySelector('#convite')).paddingTop==='32px'&&getComputedStyle(document.querySelector('#convite')).marginTop==='24px'`),'CSS: controles alteram as regiões corretas');
  await evaluate(`document.querySelector('#estilo').click()`);
  assert(await evaluate(`getComputedStyle(document.querySelector('#convite')).borderTopWidth==='0px'`),'CSS: alternância de estilo');
  await open(path.join(root,'materiais/demos/javascript.html'));
  assert(await evaluate(`!document.querySelector('#participar').disabled&&document.querySelector('#status').textContent.includes('ainda não')`),'JS: estado inicial');
  await evaluate(`document.querySelector('#participar').focus()`);
  await cdp('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',windowsVirtualKeyCode:13,text:'\r',unmodifiedText:'\r'});
  await cdp('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});
  const keyState=await evaluate(`({disabled:document.querySelector('#participar').disabled,button:document.querySelector('#participar').textContent,message:document.querySelector('#status').textContent,active:document.activeElement.id})`);
  assert(keyState.disabled&&keyState.button==='Confirmado'&&keyState.message==='Presença confirmada!','JS: confirmação por teclado e bloqueio de repetição '+JSON.stringify({keyState,errors}));
  await evaluate(`document.querySelector('#reiniciar').click()`);
  assert(await evaluate(`!document.querySelector('#participar').disabled&&document.querySelector('#status').textContent.includes('ainda não')`),'JS: reinício');
  await evaluate(`document.querySelector('#participar').click()`);
  assert(await evaluate(`document.querySelector('#participar').disabled&&document.querySelector('#trilha').textContent.includes('click recebido')`),'JS: confirmação por clique');
  await open(path.join(root,'materiais/demos/exemplo_html_completo.html'));
  assert(await evaluate(`document.querySelector('main h1').textContent==='Festa de formatura'&&document.querySelector('a').getAttribute('href')==='#agenda'&&!!document.querySelector('#agenda')`),'Exemplo HTML completo: estrutura e destino');
  await open(path.join(root,'materiais/demos/exemplo_css_completo.html'));
  assert(await evaluate(`Array.from(document.querySelectorAll('.convite')).length===2&&Array.from(document.querySelectorAll('.convite')).every(el=>getComputedStyle(el).paddingTop==='16px'&&getComputedStyle(el).marginTop==='12px')`),'Exemplo CSS completo: mesma regra em dois elementos');
  await open(path.join(root,'materiais/demos/exemplo_javascript_completo.html'));
  await evaluate(`document.querySelector('#participar').click()`);
  assert(await evaluate(`document.querySelector('#participar').disabled&&document.querySelector('#status').textContent==='Presença confirmada!'`),'Exemplo JS completo: confirmação local');
  assert(errors.length===0,'Demos sem exceções de JavaScript: '+errors.join('; '));
  // Check all local links from index, including generated PDF destinations.
  const start=await readFile(path.join(root,'materiais/INICIO.html'),'utf8');
  for(const match of start.matchAll(/href="([^"]+)"/g)){
    if(!match[1].startsWith('http'))await readFile(path.join(root,'materiais',match[1]));
  }
  assert(true,'Índice: todos os destinos locais existem');
  await writeFile(path.join(root,'materiais/verificacao.json'),JSON.stringify({checkedAt:new Date().toISOString(),results},null,2));
  console.log(`${results.length} verificações passaram: layout, links e interações offline.`);
} finally {
  ws?.close();browser.kill('SIGTERM');
  await new Promise(r=>setTimeout(r,300));
  await rm(profile,{recursive:true,force:true});
}
