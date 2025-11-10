(function(){
    function debounce(fn, delay){ let t=null; return function(){ clearTimeout(t); t=setTimeout(()=>fn.apply(this, arguments), delay); }; }
    function by(id){ return document.getElementById(id); }

    function transformExpr(s){
        if (s==null) return '';
        s = String(s).trim().replace(/\^/g,'**');
        s = s.replace(/\bsen\b/gi,'sin').replace(/\bln\b/gi,'log');
        s = s.replace(/(?<=[0-9)])\s*(?=[A-Za-z(])/g,'*');
        return s;
    }
    function parseNumberString(s){ s=String(s||'').trim(); if(s==="") return NaN; if(/^[+-]?\d+\s*\/\s*[+-]?\d+$/.test(s)){const p=s.split('/');return Number(p[0])/Number(p[1]);}const v=Number(s); return isNaN(v)?NaN:v; }


    async function savePreviewPNG(plotDiv){
        try{
            const dataUrl = await Plotly.toImage(plotDiv, {format:'png', width:1000, height:420, preserveAspectRatio:true});
            const base64 = dataUrl.split(',')[1];
            const hidden = by('preview_image'); if(hidden) hidden.value = base64;
        }catch(e){
            console.warn('No se pudo extraer PNG de Plotly:', e);
        }
    }

    // compute xs/ys given expr and optional interval; if interval missing, auto-sample around 0
    function sampleFunction(expr, a, b, N=800){
        const mathAvailable = (typeof math !== 'undefined');
        let compiled=null;
        if(mathAvailable){ try{ compiled = math.compile(expr); }catch(e){ compiled = null; } }
        // if a/b not finite, choose default span [-5,5] and try to locate sign changes adaptively
        if(!isFinite(a) || !isFinite(b) || a===b){ a=-5; b=5; }
        const xs = new Array(N); const ys=new Array(N);
        for(let i=0;i<N;i++){ const x = a + (b-a)*i/(N-1); xs[i]=x; try{ ys[i] = compiled ? compiled.evaluate({x:x}) : evalExprFallback(expr,x); }catch(e){ ys[i]=NaN; } }
        // detect sign change intervals; return xs, ys and any crossing x approx
        let crossing = null; for(let i=0;i<N-1;i++){ const y1=ys[i], y2=ys[i+1]; if(isFinite(y1) && isFinite(y2) && y1*y2<=0){ crossing = xs[i] + (xs[i+1]-xs[i])*(Math.abs(y1)/(Math.abs(y1)+Math.abs(y2)||1)); break; } }
        return {xs, ys, crossing};
    }
    function evalExprFallback(expr,x){ // last resort unsafe fallback using Function but only for numbers; try to limit exposure
        try{ const fun = new Function('x','with(Math){ return '+expr+' }'); return fun(x); }catch(e){ return NaN; }
    }

    async function serverPreviewRequest(){
        const form = new FormData(); form.append('funcion', by('funcion').value||''); form.append('limite_inferior', by('limite_inferior').value||''); form.append('limite_superior', by('limite_superior').value||'');
        try{ const r = await fetch('/biseccion/preview',{method:'POST', body: form}); if(!r.ok){ const d = await r.json(); console.warn('server preview error',d); return null; } const d=await r.json(); return d.plot_data; }catch(e){ console.warn('server preview fetch failed',e); return null; }
    }

    async function makePreview(){
        const func = by('funcion'); if(!func) return;
        const expr = transformExpr(func.value||''); if(!expr || expr.trim()==='') return hidePreview();
        // parse interval if provided; if not provided, will auto-sample
        const aRaw = by('limite_inferior') ? by('limite_inferior').value : '';
        const bRaw = by('limite_superior') ? by('limite_superior').value : '';
        let a = parseNumberString(aRaw); let b = parseNumberString(bRaw);
        // if libs available, draw interactive Plotly; otherwise use server fallback and fill hidden input
        if(typeof Plotly !== 'undefined' && typeof math !== 'undefined'){
            // if interval not provided or invalid, pick a default span but try to zoom around crossing
            let res = sampleFunction(expr, a, b, 1200);
            // if a/b were invalid, but we found a crossing, re-sample centered around crossing for better view
            if((!isFinite(a) || !isFinite(b) || a===b) && res.crossing!=null){ const c=res.crossing; a=c-2; b=c+2; res = sampleFunction(expr,a,b,1200); }
            const trace = { x: res.xs, y: res.ys, mode:'lines', line:{color:'#1f77b4', width:2} };
            const zeroLine = { x:[res.xs[0], res.xs[res.xs.length-1]], y:[0,0], mode:'lines', line:{color:'#aaa', dash:'dash'}, hoverinfo:'none' };
            const shapes = [];
            if(res.crossing!=null){ shapes.push({type:'line', x0:res.crossing, x1:res.crossing, y0:Math.min(...res.ys.filter(v=>isFinite(v))), y1:Math.max(...res.ys.filter(v=>isFinite(v))), line:{color:'#ff7f0e', dash:'dot'}}); }
            const layout = { title:{text:'Vista previa de f(x)'}, plot_bgcolor:'rgba(0,0,0,0)', paper_bgcolor:'rgba(0,0,0,0)', xaxis:{title:'x'}, yaxis:{title:'f(x)'}, shapes:shapes };
            const plotDiv = by('biseccion_preview_plot'); plotDiv.innerHTML=''; plotDiv.classList.remove('hidden');
            await Plotly.react(plotDiv,[trace,zeroLine],layout,{responsive:true});
            // save PNG into hidden input
            try{ const dataUrl = await Plotly.toImage(plotDiv,{format:'png', width:1000, height:420}); const b64 = dataUrl.split(',')[1]; by('preview_image').value = b64; }catch(e){ console.warn('no png from plotly',e); }
            return;
        }
        // fallback: ask server to prepare PNG (and it will detect crossing when interval absent)
        const b64 = await serverPreviewRequest(); if(b64){ by('preview_image').value = b64; const plotDiv=by('biseccion_preview_plot'); plotDiv.innerHTML=''; const img=new Image(); img.src='data:image/png;base64,'+b64; img.style.width='100%'; img.style.height='100%'; img.style.objectFit='contain'; plotDiv.appendChild(img); plotDiv.classList.remove('hidden'); }
    }

    function hidePreview(){ const d=by('biseccion_preview_plot'); if(d){ d.classList.add('hidden'); d.innerHTML=''; } }

    document.addEventListener('DOMContentLoaded', function(){
        const btn = by('btn_preview'); if(btn) btn.classList.add('styled-preview');
        const deb = debounce(makePreview,200);
        const f = by('funcion'); if(f){ f.addEventListener('keydown', function(e){ if(e.key==='Enter'){ e.preventDefault(); makePreview(); } }); f.addEventListener('blur', ()=>{ makePreview(); }); f.addEventListener('paste', ()=> setTimeout(makePreview,120)); }
        const a = by('limite_inferior'); const b = by('limite_superior'); if(a) a.addEventListener('change', deb); if(b) b.addEventListener('change', deb);
        if(btn) btn.addEventListener('click', makePreview);

        // intercept form submit to ensure preview_image is present
        const form = document.querySelector('form.formulario_biseccion');
        if(form){
            form.addEventListener('submit', async function(e){
                // if preview_image already present, allow submit
                const hid = by('preview_image');
                if(hid && hid.value){ return; }
                // otherwise, prevent submission, generate preview synchronously (await), then submit
                e.preventDefault();
                await makePreview();
                // small delay to ensure hidden field set
                setTimeout(()=>{ form.submit(); }, 80);
            });
        }
    });
})();
