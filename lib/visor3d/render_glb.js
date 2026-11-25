const {chromium}=require('playwright');(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const L=JSON.parse(process.argv[2]);for(const [n,qs] of L){const p=await b.newPage({viewport:{width:700,height:700}});
p.on('pageerror',e=>console.log(n,e.message));await p.goto(`http://127.0.0.1:8799/g.html?${qs}`);
try{await p.waitForFunction('window.done===true',{timeout:90000});}catch(e){console.log(n,'timeout',await p.title())}
await p.screenshot({path:`g_${n}.png`,omitBackground:true});await p.close();}await b.close();})();
