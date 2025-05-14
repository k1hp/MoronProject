// Функция авто пролистывания контента по id
function scrollToSection(sectionId) {
  const element = document.getElementById(sectionId);
  if (element) {
    element.scrollIntoView({ behavior: "smooth" });
  }
}
// по пикселям
function scrollByPixels(pixels) {
  window.scrollBy({
    top: pixels,
    left: 0,
    behavior: "smooth",
  });
}

// Массив с данными процессоров я хз как это будет работать на практике, но в моей голове все идеально
const processors = [
  {
    name: "Процессор AMD A6-7480 OEM",
    socket: "FM2+",
    cores: 2,
    frequency: "3.5 ГГц",
    cache: "1 МБ",
    graphics: "AMD Radeon R5",

    price: "4 290 ₽",
  },
  {
    name: "Процессор AMD Athlon X4 950 OEM",
    socket: "AM4",
    cores: 4,
    frequency: "3.5 ГГц",
    cache: "2 МБ",
    tdp: "65 Вт",

    price: "5 490 ₽",
  },
  {
    name: "Процессор AMD A6-9500E OEM",
    socket: "AM4",
    cores: 2,
    frequency: "3 ГГц",
    cache: "1 МБ",

    price: "3 990 ₽",
  },
];

// Функция для создания карточек процессоров, убейте меня
function createProcessorCards() {
  const container = document.getElementById("processors-container");

  processors.forEach((processor) => {
    const card = document.createElement("div");
    card.className = "col";

    card.innerHTML = `
            <div class="card product-card shadow-sm h-100">
                <div class="card-body">
                    <h5 class="card-title">${processor.name}</h5>
                    <ul class="specs-list mb-3">
                        <li><strong>Сокет:</strong> ${processor.socket}</li>
                        <li><strong>Количество ядер:</strong> ${
                          processor.cores
                        }</li>
                        <li><strong>Базовая частота:</strong> ${
                          processor.frequency
                        }</li>
                        <li><strong>Кэш L2:</strong> ${processor.cache}</li>
                        ${
                          processor.graphics
                            ? `<li><strong>Графика:</strong> ${processor.graphics}</li>`
                            : ""
                        }
                        ${
                          processor.tdp
                            ? `<li><strong>Тепловыделение:</strong> ${processor.tdp}</li>`
                            : ""
                        }
                    </ul>
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <button class="btn btn-sm btn-outline-primary">Добавать</button>
                        <div>

                        <h5 class="mb-0 text-primary">${processor.price}</h5>
                    </div>
                </div>
            </div>
        `;

    container.appendChild(card);
  });
}
// Создаем карточки процессоров при загрузке страницы
document.addEventListener("DOMContentLoaded", createProcessorCards);

// Массив с данными материнских плат
const motherboards = [
    {

        name: "Материнская плата ASUS PRIME A320M-K",
        socket: "AM4",
        formFactor: "Micro ATX",
        ramSlots: 2,
        maxRam: "32 ГБ",
        price: "4 990 ₽"
    },
    {
        name: "Материнская плата MSI B450M PRO-VDH MAX",
        socket: "AM4",
        formFactor: "Micro ATX",
        ramSlots: 4,
        maxRam: "64 ГБ",
        price: "5 490 ₽"
    },
    {
        name: "Материнская плата Gigabyte B450 AORUS M",
        socket: "AM4",
        formFactor: "Micro ATX",
        ramSlots: 4,
        maxRam: "64 ГБ",
        price: "5 990 ₽"
    }
];

// Функция для создания карточек материнских плат
function createMotherboardCards() {
    const container = document.getElementById('motherboards-container');

    motherboards.forEach(motherboard => {
        const card = document.createElement('div');
        card.className = 'col';

        card.innerHTML = `
            <div class="card product-card shadow-sm h-100">
                <div class="card-body">
                    <h5 class="card-title">${motherboard.name}</h5>
                    <ul class="specs-list mb-3">
                        <li><strong>Сокет:</strong> ${motherboard.socket}</li>
                        <li><strong>Форм-фактор:</strong> ${motherboard.formFactor}</li>
                        <li><strong>Количество слотов для ОЗУ:</strong> ${motherboard.ramSlots}</li>
                        <li><strong>Максимальный объём ОЗУ:</strong> ${motherboard.maxRam}</li>
                    </ul>
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <button class="btn btn-sm btn-outline-primary">Добавить</button>
                        <div>
                            <h5 class="mb-0 text-primary">${motherboard.price}</h5>
                        </div>
                    </div>
                </div>
            </div>
        `;

        container.appendChild(card);
    });
}

// Создаем карточки материнских плат при загрузке страницы
document.addEventListener("DOMContentLoaded", createMotherboardCards);


/*document.addEventListener("DOMContentLoaded", () => {
    createProcessorCards(); //  Создание карточек процессоров
    createMotherboardCards(); // Создаем карточки материнских плат
    createGraphicsCardCards(); // Создание видеокарт
}); */

// Массив с данными видеокарт
const graphicsCards = [
    {
        name: "Видеокарта NVIDIA GeForce GTX 1650",
        memory: "4 ГБ GDDR5",
        coreClock: "1485 МГц",
        memoryClock: "8000 МГц",
        tdp: "75 Вт",
        price: "14 990 ₽"
    },
    {
        name: "Видеокарта AMD Radeon RX 5500 XT",
        memory: "8 ГБ GDDR6",
        coreClock: "1607 МГц",
        memoryClock: "14000 МГц",
        tdp: "130 Вт",
        price: "19 990 ₽"
    },
    {
        name: "Видеокарта NVIDIA GeForce RTX 3080",
        memory: "12 ГБ GDDR6",
        coreClock: "1320 МГц",
        memoryClock: "15000 МГц",
        tdp: "170 Вт",
        price: "34 990 ₽"
    }
];

// Функция для создания карточек видеокарт
function createGraphicsCardCards() {
    const container = document.getElementById('graphics-cards-container');

    graphicsCards.forEach(graphicsCard => {
        const card = document.createElement('div');
        card.className = 'col';

        card.innerHTML = `
            <div class="card product-card shadow-sm h-100">
                <div class="card-body">
                    <h5 class="card-title">${graphicsCard.name}</h5>
                    <ul class="specs-list mb-3">
                        <li><strong>Память:</strong> ${graphicsCard.memory}</li>
                        <li><strong>Частота ядра:</strong> ${graphicsCard.coreClock}</li>
                        <li><strong>Частота памяти:</strong> ${graphicsCard.memoryClock}</li>
                        <li><strong>Тепловыделение:</strong> ${graphicsCard.tdp}</li>
                    </ul>
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <button class="btn btn-sm btn-outline-primary">Добавить</button>
                        <div>
                            <h5 class="mb-0 text-primary">${graphicsCard.price}</h5>
                        </div>
                    </div>
                </div>
            </div>
        `;

        container.appendChild(card);
    });
}

document.addEventListener("DOMContentLoaded", createGraphicsCardCards);

document.addEventListener("DOMContentLoaded", () => {
    const links = document.querySelectorAll("nav ul li a");

    links.forEach(link => {
        link.addEventListener("click", () => {
            links.forEach(l => l.classList.remove("active"));
            link.classList.add("active");
        });
    });
});


    function copyToClipboard(id) {
        const element = document.getElementById(id);
        const range = document.createRange();
        range.selectNode(element);
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(range);
        try {
            document.execCommand('copy');
            alert('Данные успешно скопированы!');
        } catch(err) {
            alert('Ошибка копирования.');
        }
        window.getSelection().removeAllRanges();
    }
