const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const out={};
for(const v of ['iso','izq','frente']){const p=await b.newPage({viewport:{width:1400,height:1400}});
p.on('console',m=>console.log(v,m.text()));p.on('pageerror',e=>console.log(v,'ERR',e.message));
await p.goto(`http://127.0.0.1:8765/modelo.html?v=${v}`);await p.waitForFunction('window.done===true',{timeout:60000});
out[v]=await p.evaluate('window.pts');await p.screenshot({path:`r3d_${v}.png`,omitBackground:true});await p.close();}
fs.writeFileSync('pts.json',JSON.stringify(out,null,1));await b.close();})();
