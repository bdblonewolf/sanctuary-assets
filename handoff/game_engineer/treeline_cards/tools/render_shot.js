const puppeteer=require('/workspace/m2m_test/node_modules/puppeteer');
(async()=>{
 const b=await puppeteer.launch({executablePath:'/usr/bin/google-chrome',headless:"new",protocolTimeout:600000,args:['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
 const jobs=JSON.parse(process.argv[2]);
 for(const [url,out,w,h] of jobs){
  const pg=await b.newPage(); await pg.setViewport({width:w||1280,height:h||720});
  pg.on('console',m=>console.log('console:',m.text())); pg.on('pageerror',e=>console.log('pageerr',e.message));
  await pg.goto('http://127.0.0.1:8931/r/index.html?'+url+'&w='+(w||1280)+'&h='+(h||720));
  await pg.waitForFunction('window.DONE===1',{timeout:240000});
  const t=await pg.title(); if(t.startsWith('ERR')) console.log(t);
  const el=await pg.$('canvas'); await el.screenshot({path:out}); await pg.close(); console.log('wrote',out);
 }
 await b.close();
})();
