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

// 微信咨询：就地弹出二维码，不跳转到外部页面。
// 标记 data-wechat 的链接仍指向真实地址，脚本不可用时可正常点击。
(function () {
  const dialog = document.getElementById('wx-dialog');
  if (!dialog) return;
  const context = dialog.querySelector('#wx-context');
  const panel = dialog.querySelector('.wx-panel');
  let lastFocus = null;

  function open(trigger) {
    lastFocus = trigger;
    const label = trigger && trigger.getAttribute('data-context');
    if (context) {
      context.hidden = !label;
      context.textContent = label ? '咨询套餐：' + label : '';
    }
    dialog.hidden = false;
    document.body.classList.add('wx-open');
    const close = dialog.querySelector('[data-wx-close]');
    if (close) close.focus();
  }

  function close() {
    dialog.hidden = true;
    document.body.classList.remove('wx-open');
    if (lastFocus && typeof lastFocus.focus === 'function') lastFocus.focus();
    lastFocus = null;
  }

  document.addEventListener('click', function (event) {
    const trigger = event.target.closest && event.target.closest('a[data-wechat]');
    if (trigger) {
      // 让用户仍能用中键/Cmd 点击在新标签打开原链接。
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.button !== 0) return;
      event.preventDefault();
      open(trigger);
      if (typeof gtag === 'function') {
        gtag('event', 'wechat_qr_open', {
          page_name: document.body.getAttribute('data-page') || '',
          cta_position: trigger.getAttribute('data-position') || '',
          product: trigger.getAttribute('data-context') || ''
        });
      }
      return;
    }
    if (dialog.hidden) return;
    if (event.target.closest('[data-wx-close]') || !event.target.closest('.wx-panel')) close();
  });

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && !dialog.hidden) close();
  });

  // 焦点保持在弹窗内
  if (panel) {
    dialog.addEventListener('keydown', function (event) {
      if (event.key !== 'Tab') return;
      const items = dialog.querySelectorAll('button, a[href], img[tabindex]');
      if (!items.length) return;
      const first = items[0];
      const last = items[items.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    });
  }
})();
