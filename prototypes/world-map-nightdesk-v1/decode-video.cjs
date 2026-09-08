/* 用浏览器解码真实录屏；仅转换格式，不重新演出或绘制 UI。 */
const {chromium}=require('C:/Users/gzfangyue/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('node:fs');const path=require('node:path');
(async()=>{
  const root=path.join(__dirname,'evidence','v2','decoded-frames');fs.mkdirSync(root,{recursive:true});
  const browser=await chromium.launch({headless:true,executablePath:'C:/Users/gzfangyue/AppData/Local/ms-playwright/chromium_headless_shell-1223/chrome-headless-shell-win64/chrome-headless-shell.exe'});
  const page=await browser.newPage();
  await page.goto('http://127.0.0.1:8786',{waitUntil:'networkidle'});
  const duration=await page.evaluate(async()=>{
    const video=document.createElement('video');video.src='evidence/v2/05-interaction-demo.webm';video.muted=true;video.preload='auto';
    const canvas=document.createElement('canvas');canvas.width=960;canvas.height=540;
    document.body.replaceChildren(video,canvas);window.recordedVideo=video;window.recordedCanvas=canvas;
    await new Promise((resolve,reject)=>{video.onloadeddata=resolve;video.onerror=reject;});return video.duration;
  });
  let count=0;
  for(let time=1;time<duration-.1;time+=.125){
    const data=await page.evaluate(async t=>{
      const v=window.recordedVideo,c=window.recordedCanvas;
      await new Promise(resolve=>{v.onseeked=resolve;v.currentTime=t;});
      c.getContext('2d').drawImage(v,0,0,960,540);return c.toDataURL('image/png').split(',')[1];
    },time);
    fs.writeFileSync(path.join(root,String(count++).padStart(4,'0')+'.png'),Buffer.from(data,'base64'));
  }
  await browser.close();process.stdout.write(JSON.stringify({duration,frames:count,directory:root}));
})().catch(e=>{process.stderr.write(String(e.stack));process.exit(1)});
