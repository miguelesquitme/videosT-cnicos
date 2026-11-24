const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
for(const k of process.argv.slice(2)){await p.goto('file://'+process.cwd()+'/'+k+'.html');await p.waitForTimeout(400);await p.screenshot({path:'../miniatura_'+k+'_pro.png'});}
await b.close()})();