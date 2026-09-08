/* 独立美术样片。所有纸材与地图来自同一幅 ImageGen 母画。 */
const REGIONS = {
  north: {id:"01",name:"北美禁区带",headline:["洗衣店里","出现了一片海"],short:"洗衣店里出现了一片海",deck:["断电两小时后，潮线仍在三扇滚筒窗之间保持水平。","店外道路干燥，最近海岸线在一千公里外。"],risk:"红线升温",available:true,total:4,photo:"assets/north.png",alt:"北美来稿：三台洗衣机的窗内出现同一条海平面",tasks:[{name:"洗衣机海潮现场复核",meta:"线索 · 常驻 · 耗时 2 天"},{name:"干涸道路水样追踪",meta:"深链 · 限时 · 耗时 3 天"}]},
  east: {id:"02",name:"东亚神秘地带",headline:["天文台在凌晨","向北移动"],short:"天文台在凌晨向北移动",deck:["凌晨三点，整座天文台向北平移了五十米。","值班员坚持所有仪器仍在原位。"],risk:"地区锁定",available:false,total:2,photo:"assets/east.png",alt:"东亚来稿：月前的天文台建筑",tasks:[{name:"核对天文台基座位移",meta:"已知情报 · 尚未解锁"},{name:"追查北向磁针记录",meta:"解锁条件 · 线索不足"}]},
  pacific: {id:"03",name:"南太平洋失航区域",headline:["深海电波正在","重复呼号"],short:"深海电波正在重复呼号",deck:["失联渔船的最后讯号来自海面千米以下。","海面浮标却记录到同一组短波。"],risk:"地区锁定",available:false,total:2,photo:"assets/pacific.png",alt:"太平洋来稿：碟面盛着海水的巨大天线",tasks:[{name:"复听失联渔船呼号",meta:"已知情报 · 尚未解锁"},{name:"比对深海浮标记录",meta:"解锁条件 · 深链不足"}]}
};
const $ = id => document.getElementById(id);
const state={selected:"north",expanded:false,entered:false};
let transitionTimer;

function fitStage(){
  const scale=Math.min(innerWidth/1672,innerHeight/941);
  $("stage").style.transform=`translate(${(innerWidth-1672*scale)/2}px,${(innerHeight-941*scale)/2}px) scale(${scale})`;
}

// 将完整 1104×704 原图投影到同一张照片纸面的四角。不裁切或制作状态缩略图。
// 这些角来自本轮母画的实际边缘，而非旧 UI 的框体尺寸。
function projectPhoto(){
  const p=[[73,275],[607,255],[626,588],[83,609]];
  const [p0,p1,p2,p3]=p;
  const dx1=p1[0]-p2[0],dx2=p3[0]-p2[0],dx3=p0[0]-p1[0]+p2[0]-p3[0];
  const dy1=p1[1]-p2[1],dy2=p3[1]-p2[1],dy3=p0[1]-p1[1]+p2[1]-p3[1];
  const den=dx1*dy2-dx2*dy1;
  const g=(dx3*dy2-dx2*dy3)/den,h=(dx1*dy3-dx3*dy1)/den;
  const a=p1[0]-p0[0]+g*p1[0],b=p3[0]-p0[0]+h*p3[0];
  const d=p1[1]-p0[1]+g*p1[1],e=p3[1]-p0[1]+h*p3[1];
  $("story-photo").style.transform=`matrix3d(${a/1104},${d/1104},0,${g/1104},${b/704},${e/704},0,${h/704},0,0,1,0,${p0[0]},${p0[1]},0,1)`;
}

function render(animate=false){
  const r=REGIONS[state.selected];
  $("story").dataset.region=state.selected;
  $("story").classList.toggle("expanded",state.expanded);
  $("story").classList.toggle("entered",state.entered);
  $("story-kicker").textContent=`PHOTO DESK / 当前来稿 ${r.id}`;
  $("region-name").textContent=r.name;
  $("headline").replaceChildren();
  const lines=state.entered?["地区任务台","样片入口"]:state.expanded?[r.short]:r.headline;
  lines.forEach((line,i)=>{if(i)$("headline").append(document.createElement("br"));$("headline").append(document.createTextNode(line));});
  $("risk").textContent=r.risk;
  $("risk").hidden=state.entered;
  $("deck").textContent=r.deck.join("\n");
  $("deck").hidden=state.expanded||state.entered;
  $("task-list").hidden=!state.expanded||state.entered;
  $("entry-copy").hidden=!state.entered;
  $("task-list").replaceChildren(...r.tasks.map(task=>{
    const li=document.createElement("li");
    const n=document.createElement("span");n.className="task-name";n.textContent=task.name;
    const m=document.createElement("span");m.className="task-meta";m.textContent=task.meta;
    li.append(n,m);return li;
  }));
  $("disclosure").hidden=state.entered;
  $("disclosure").setAttribute("aria-expanded",String(state.expanded));
  $("disclosure-title").textContent=`任务情报 · ${r.total}`;
  $("disclosure-hint").textContent=state.expanded?`已显示 2 / 共 ${r.total} 项 −`:"查看已知任务 ＋";
  $("enter").disabled=!r.available;
  $("enter").textContent=state.entered?"返回选题桌 ↶":r.available?"进入地区 →":"尚未解锁";
  $("access-note").textContent=state.entered?"正式游戏未连接":r.available?"可进入调查":"来稿可查阅 · 暂不可进入";
  $("map-caption").textContent=`${r.id} / ${r.name}的来稿正在左侧工作夹中展开`;
  for(const el of document.querySelectorAll("button[data-region]")){
    const selected=el.dataset.region===state.selected;
    el.setAttribute("aria-pressed",String(selected));
    const sub=el.querySelector(".place-sub");
    if(sub)sub.textContent=selected?"当前来稿":REGIONS[el.dataset.region].available?"可进入调查":"锁定 · 可预览";
  }
  if(!$("story-photo").src.endsWith(r.photo))$("story-photo").src=r.photo;
  $("story-photo").alt=r.alt;
  $("announcer").textContent=`${r.name}。${r.short}。${r.available?"可进入调查":"地区锁定，可查看线报"}。${state.expanded?"已展开任务情报":""}`;
  if(animate){
    clearTimeout(transitionTimer);
    $("story-photo").classList.remove("is-changing");
    for(const p of document.querySelectorAll(".map-place"))p.classList.remove("picked");
    void $("story-photo").offsetWidth;
    $("story-photo").classList.add("is-changing");
    document.querySelector(`.map-place[data-region="${state.selected}"]`).classList.add("picked");
    transitionTimer=setTimeout(()=>$("story-photo").classList.remove("is-changing"),500);
  }
}

function selectRegion(key){
  if(!REGIONS[key])return;
  state.selected=key;state.entered=false;render(true);
}
function toggleTasks(){if(state.entered)return;state.expanded=!state.expanded;render();}
document.querySelectorAll("button[data-region]").forEach(el=>el.addEventListener("click",()=>selectRegion(el.dataset.region)));
$("disclosure").addEventListener("click",toggleTasks);
$("enter").addEventListener("click",()=>{if(!REGIONS[state.selected].available)return;state.entered=!state.entered;state.expanded=false;render();});
addEventListener("keydown",e=>{
  if(e.ctrlKey||e.altKey||e.metaKey)return;
  if(["1","2","3"].includes(e.key)){selectRegion(["north","east","pacific"][Number(e.key)-1]);e.preventDefault();}
  if(e.key.toLowerCase()==="e"){toggleTasks();e.preventDefault();}
  if(e.key==="Escape"){state.entered=false;state.expanded=false;render();}
});
addEventListener("resize",fitStage);
for(const r of Object.values(REGIONS)){const image=new Image();image.src=r.photo;}
projectPhoto();fitStage();render();
window.nightdesk={state,regions:REGIONS,selectRegion,toggleTasks,render,photoCorners:[[73,275],[607,255],[626,588],[83,609]]};
