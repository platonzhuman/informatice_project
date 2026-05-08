let products = [], cart = [];

// download tovar
async function load() {
    const res = await fetch('/products');
    products = await res.json();
    document.getElementById('goods').innerHTML = `<ul>${products.map(p => `
        <li>${p.name} — ${p.price}₽ 
            <button onclick="add(${p.id})">+</button>
            <small>(ост. ${p.stock})</small>
        </li>`).join('')}</ul>`;
}

// download in korz
window.add = (id) => {
    const p = products.find(x => x.id === id);
    const item = cart.find(x => x.id === id);
    
    if (item) {
        if (item.qty < p.stock) item.qty++;
        else return alert('Больше нет на складе');
    } else {
        cart.push({...p, qty: 1});
    }
    render();
};

// vuvod rkrox
function render() {
    const cartDiv = document.getElementById('cart');
    if (!cart.length) {
        cartDiv.innerHTML = '<i>Пусто</i>';
        document.getElementById('total').innerText = '0';
        return;
    }

    let html = '<table><tr><th>Товар</th><th>Кол-во</th><th>Сумма</th><th></th></tr>';
    let total = 0;

    cart.forEach((item, i) => {
        const sum = item.price * item.qty;
        total += sum;
        html += `<table>
            <td>${item.name}</td>
            <td><input type="number" value="${item.qty}" onchange="change(${i}, this.value)"></td>
            <td>${sum}</td>
            <td><button onclick="remove(${i})">×</button></td>
        </tr>`;
    });
    
    cartDiv.innerHTML = html + '</table>';
    document.getElementById('total').innerText = total;
}

window.change = (i, v) => {
    const val = parseInt(v);
    if (val <= cart[i].stock && val > 0) cart[i].qty = val;
    else alert('Недопустимое количество');
    render();
};

window.remove = (i) => { cart.splice(i, 1); render(); };

// button bye
document.getElementById('buy').onclick = async () => {
    if (!cart.length) return;
    const body = {
        cashier_id: document.getElementById('cashier').value,
        items: cart.map(i => ({id_product: i.id, quantity: i.qty}))
    };

    const res = await fetch('/sale', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(body)
    });
    const data = await res.json();

    const msg = document.getElementById('msg');
    if (res.ok) {
        msg.innerHTML = `<b style="color:green">Успех! Чек №${data.check_id}</b>`;
        cart = [];
        render();
        load();
    } else {
        msg.innerHTML = `<b style="color:red">Ошибка: ${data.error}</b>`;
    }
};

// button otchet
document.getElementById('reportBtn').onclick = async () => {
    const d = document.getElementById('date').value;
    if (!d) return;
    const res = await fetch(`/report?date=${d}`);
    const data = await res.json();
    
    let txt = `Выручка: ${data.revenue} ₽\n\nПродано:\n`;
    data.items.forEach(i => txt += `• ${i.name}: ${i.qty} шт.\n`);
    document.getElementById('reportResult').innerText = txt;
};

load();