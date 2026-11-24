const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+process.cwd()+'/mini.html');await p.waitForTimeout(500);await p.screenshot({path:'../miniatura_h01v5.png'});await b.close()})();
