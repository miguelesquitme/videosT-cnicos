const {chromium}=require('playwright');const fs=require('fs');
// node batch.js jobs.json  -> jobs: [{f, out, views:[{yaw,pitch,...}], cfg:{}}]
(async()=>{const J=JSON.parse(fs.readFileSync(process.argv[2]));
const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
for(const j of J){for(let i=0;i<j.views.length;i++){const out=`${j.out}_${i}.png`; if(fs.existsSync(out)&&!j.force) continue;
 const p=await b.newPage({viewport:{width:700,height:700}});p.on('pageerror',e=>console.log('ERR',j.out,e.message));
 const cfg=Object.assign({f:j.f,w:700,h:700,exp:1.0},j.cfg||{},j.views[i]);
 try{await p.goto('http://127.0.0.1:8770/hq.html#'+encodeURIComponent(JSON.stringify(cfg)));
 await p.waitForFunction('window.done===true',{timeout:120000});await p.screenshot({path:out});}catch(e){console.log('FAIL',out,e.message)}
 await p.close();}console.log('ok',j.out);}
await b.close();})();
