const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1720,height:680}});
await p.goto('file://'+process.cwd()+'/html/_sym.html');await p.waitForTimeout(300);await p.screenshot({path:'img/rele_r2n_simbolo.png',omitBackground:true});await b.close()})();
