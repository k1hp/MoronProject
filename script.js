// Функция авто пролистывания контента по id
function scrollToSection(sectionId) {
  const element = document.getElementById(sectionId);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' });
  }
}
// по пикселям
function scrollByPixels(pixels) {
    window.scrollBy({
      top: pixels,
      left: 0,
      behavior: 'smooth'
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
        
        price: "4 290 ₽"
    },
    {
        name: "Процессор AMD Athlon X4 950 OEM",
        socket: "AM4",
        cores: 4,
        frequency: "3.5 ГГц",
        cache: "2 МБ",
        tdp: "65 Вт",
        
        price: "5 490 ₽"
    },
    {
        name: "Процессор AMD A6-9500E OEM",
        socket: "AM4",
        cores: 2,
        frequency: "3 ГГц",
        cache: "1 МБ",
        
        price: "3 990 ₽"
    }
];

// Функция для создания карточек, Я ХОТЕЛ УМЕРЕТЬ когда делал это
function createProcessorCards() {
    const container = document.getElementById('processors-container');
    
    processors.forEach(processor => {
        const card = document.createElement('div');
        card.className = 'col';
        
        card.innerHTML = `
            <div class="card product-card shadow-sm h-100">
                <div class="card-body">
                    <h5 class="card-title">${processor.name}</h5>
                    <ul class="specs-list mb-3">
                        <li><strong>Сокет:</strong> ${processor.socket}</li>
                        <li><strong>Количество ядер:</strong> ${processor.cores}</li>
                        <li><strong>Базовая частота:</strong> ${processor.frequency}</li>
                        <li><strong>Кэш L2:</strong> ${processor.cache}</li>
                        ${processor.graphics ? `<li><strong>Графика:</strong> ${processor.graphics}</li>` : ''}
                        ${processor.tdp ? `<li><strong>Тепловыделение:</strong> ${processor.tdp}</li>` : ''}
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

// Создаем карточки при загрузке страницы
document.addEventListener('DOMContentLoaded', createProcessorCards);