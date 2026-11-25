const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
for(const k of process.argv.slice(2)){await p.goto('file://'+process.cwd()+'/html/'+k+'.html');await p.waitForTimeout(400);await p.screenshot({path:'png/'+k+'.png'});}
await b.close()})();