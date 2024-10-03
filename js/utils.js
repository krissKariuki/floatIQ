'use strict'

const $=document.querySelector.bind(document)
const $$=document.querySelectorAll.bind(document)

const RAW=(...params)=>render_active_window(...params)
const MOE=(...params)=>modify_elements_styles(...params)
const HAE=(...params)=>highlight_active_element(...params)


function create_element(parent,elem,id,Class,txt = '')
{
    const el=document.createElement(elem)
    $(parent).append(el)
    el.setAttribute('id',id)
    el.setAttribute('class',Class)
    el.innerHTML=txt
}

function render_active_window(active,class_name,display='block')
{
    [...$$(class_name)].forEach(elem=>
    {
        if(elem.getAttribute('class')==$(active).getAttribute('class'))elem.style.display=display
        else elem.style.display='none'
    })
}
function toggle_self(class_name,class_list)
{
    [...$$(class_name)].forEach(element=>{element.addEventListener('click',()=>
    {
        if(element.classList.contains(class_list))element.classList.remove(class_list)

        else element.classList.add(class_list)
    })
    })
}

function toggle_other(element,target,class_list)
{
    $(element).addEventListener('click',()=>
    {
        if($(target).classList.contains(class_list))$(target).classList.remove(class_list)

        else $(target).classList.add(class_list)
    })
}
function modify_other_elements(element,target_class,class_list)
{
    $(element).addEventListener('click',()=>
    {
        [...$$(target_class)].forEach(element=>
        {
            if(element.classList.contains(class_list))element.classList.remove(class_list)
        else element.classList.add(class_list)
        })
    })
}

function highlight_active_element(class_name,style)
{
    [...$$(class_name)].forEach(elem=>
    {
        elem.addEventListener('click',activate)
    })
    
    function activate(e)
    {
        const target=e.target.getAttribute('class');
        
        [...$$(class_name)].forEach(elem=>
        {
            if(elem.getAttribute('class')==target)elem.classList.add(style)
            else elem.classList.remove(style)
        })
    }
}

function random_number (min=10,max=100)
{
    return Math.round((Math.random()*max)+min).toFixed(2)
}

function random_color(color='rgb',alpha='')
{
    const r=Math.round(Math.random()*255)
    const g=Math.round(Math.random()*255)
    const b=Math.round(Math.random()*255)
    
    const a=typeof(alpha)!='number'?((Math.random()+0.1).toFixed(2)):alpha
    
    const color_object=
    {
        'r':()=>`rgba(${r},0,0,${a})`,
        'g':()=>`rgba(0,${g},0,${a})`,
        'b':()=>`rgba(0,0,${b},${a})`,
        'w':()=>`rgba(255,255,255,${a})`,
        'b':()=>`rgba(0,0,0,${a})`,
        'rg':()=>`rgba(${r},${g},0,${a})`,
        'rb':()=>`rgba(${r},0,${b},${a})`,
        'gb':()=>`rgba(0,${g},${b},${a})`,
        'rgb':()=>`rgba(${r},${g},${b},${a})`
    }
    
    
    if(color in color_object)return color_object[color]()
    
    else throw Error('invalid color format in random_color()')
}

function swap_currency(currency_rate=1)
{
    
    function currency_rates(cnc='$',qty=1,rate=currency_rate)
    {
        const convert=cnc=='$'?{currency:'kes',amount:(rate*qty).toFixed(2)}:{currency:'$',amount:(qty/rate).toFixed(2)}
        
        return convert
    }
    [...$$('.currency-rate')].forEach(element=>
    {
        const currency_element=element.querySelector('.currency')
        const balance_element=element.querySelector('.balance')
        const curr=currency_element.innerText
        const baln=parseFloat(balance_element.innerText.replace(/,/g,''))
        const conversion=currency_rates(curr,baln)
        
        
        currency_element.innerText=conversion.currency
        balance_element.innerText=parseFloat(conversion.amount).toLocaleString('en-us')
        
    })
}

async function update_currency(time=1000,url='https://v6.exchangerate-api.com/v6/f987115a5202b2a548b68e6e/latest/USD')
{
    const controller=new AbortController()
    const timeout=setTimeout(()=>controller.abort(),time)
    const response=await fetch(url,{signal:controller.signal})
    
    clearTimeout(timeout)
    
    const usd_kes=await response.json()
    return usd_kes.conversion_rates.KES
}