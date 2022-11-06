import dataListEcchi from './dataComicEcchi.json' assert {type: 'json'};
console.log(dataListEcchi.ecchi[0].name)

// var list = document.getElementById('box').innerHTML
dataListEcchi.ecchi.forEach(item => {
    if (item.id < 50) {
        document.getElementById('box').innerHTML += `<div class="item">
            <div class="item-image">
                <img src="${item.srcImg}" alt="" class="item-img">
            </div>
            <div class="item-content">
                <h3 class="item-title">${item.name}</h3>
                <p class="item-text">Chap ${item.chap}</p>
            </div>
        </div>`;
    }
});