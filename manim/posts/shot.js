const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
const n=parseInt(process.argv[2]);for(let i=1;i<=n;i++){const k=String(i).padStart(2,'0');await p.goto('file://'+process.cwd()+'/html/post_'+k+'.html');
await p.waitForTimeout(250);await p.screenshot({path:'png/post_'+k+'.png'});}await b.close()})();