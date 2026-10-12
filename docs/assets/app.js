const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('#navigation');
function closeMenu(){nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-label','展开导航');}
toggle.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')!=='true';nav.classList.toggle('open',open);toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'关闭导航':'展开导航');});
nav.addEventListener('click',e=>{if(e.target.closest('a'))closeMenu();});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&toggle.getAttribute('aria-expanded')==='true'){closeMenu();toggle.focus();}});
document.addEventListener('click',e=>{if(!e.target.closest('header'))closeMenu();});
// Integration hook only: no cookies, identifiers, storage, or external transmission.
document.addEventListener('click',event=>{
 const link=event.target.closest('a[data-conversion]');
 if(!link)return;
 document.dispatchEvent(new CustomEvent('ai-plus:conversion',{detail:{action:link.dataset.conversion,page:location.pathname}}));
});
