/* Keep real controls together. CSS text columns can fragment or hide buttons. */
export function pageItems(container){
 const items=[];
 function add(node){
  if(node.nodeType!==1){if(node.textContent.trim())items.push(node);return;}
  if(node.matches('summary'))return;
  if(node.matches('.options')){
   for(const child of [...node.children]){const wrap=document.createElement('div');wrap.className='options focus-option-item';wrap.append(child);items.push(wrap);}return;
  }
  if(node.matches('details,.explain,.exercise-hint,.exercise-source')){for(const child of [...node.childNodes])add(child);return;}
  items.push(node);
 }
 for(const node of [...container.childNodes])add(node);
 return items;
}
export function paginateContent(container,items,height){
 const limit=Math.max(80,height),pages=[];
 container.replaceChildren();container.style.height='';container.style.columnWidth='';container.style.columnGap='';container.style.columnFill='';
 function create(){const page=document.createElement('div');page.className='focus-content-page';container.append(page);pages.push(page);return page;}
 let page=create();
 for(const item of items){
  page.append(item);
  if(page.children.length>1&&page.scrollHeight>limit+1){item.remove();page=create();page.append(item);}
 }
 for(const p of pages){p.style.maxHeight=limit+'px';p.hidden=true;}
 return {count:pages.length,show(index){const at=Math.max(0,Math.min(pages.length-1,index));pages.forEach((p,i)=>{p.hidden=i!==at;});return at;},containing(node){return pages.findIndex(p=>p.contains(node));},pages};
}
