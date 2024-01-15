// prints CSV

let res = 'rnk,name,sym,market_cap,circ_supply,url'

for (const tr of Array.from($$('.sc-feda9013-3.ePzlNg.cmc-table tr')).slice(2)) {
    let [_, num, name, sym, a, aa, aaa, mc, aaaa, circ_supply, ...rest] = Array.from(tr.querySelectorAll('td')).map(td => td.textContent)
    const url = tr.querySelector('a').href

    mc = mc.split('$')[2].replaceAll(',', '')
    sym = circ_supply.split(' ')[1]
    circ_supply = circ_supply.split(' ')[0].replaceAll(',','')
    name = name.slice(0, name.length - sym.length)
    
    res += '\n' + [num, name, sym, mc, circ_supply, url].join(',')
    
}
console.log(res)
