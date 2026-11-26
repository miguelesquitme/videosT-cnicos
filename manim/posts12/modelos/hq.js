const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const L=JSON.parse(fs.readFileSync(process.argv[2]));const out={};for(const [n,cfg] of Object.entries(L)){const p=await b.newPage({viewport:{width:cfg.w||1400,height:cfg.h||1400}});
p.on('pageerror',e=>console.log(n,e.message));await p.goto('http://127.0.0.1:8799/hq.html#'+encodeURIComponent(JSON.stringify(cfg)));
try{await p.waitForFunction('window.done===true',{timeout:180000});}catch(e){console.log(n,'timeout',await p.title())}
out[n]=await p.evaluate('window.pts');await p.screenshot({path:`hq_${n}.png`,omitBackground:true});await p.close();}
fs.writeFileSync('hq_pts.json',JSON.stringify(out,null,1));await b.close();})();
