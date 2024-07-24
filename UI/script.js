// Получаем все элементы .Application и их дочерние элементы .AppName и .AppIcon
const applications = document.querySelectorAll('.Application');
const appIcons = document.querySelectorAll('.AppIcon');
const appNames = document.querySelectorAll('.AppName');
const Notify = document.getElementById('InfoBlock');
const timeElement = document.getElementById('Time');
const saverElement = document.getElementById('Saver');

// Изначально выбранное приложение (начинаем с первого)
let currentAppIndex = 0;

// Создаем аудио элемент для воспроизведения звука
const clickSound = new Audio('media/click.mp3');

// Таймер для отслеживания активности
let inactivityTimer = null;

// Функция для обновления стилей при выборе/снятии выбора приложения
function updateAppStyles() {
    // Сначала снимаем выбор со всех приложений
    appNames.forEach((appName, index) => {
        appName.style.color = 'transparent';
        appIcons[index].style.transform = 'scale(1.0)';
    });

    // Затем выделяем выбранное приложение
    appNames[currentAppIndex].style.color = '#eee';
    appIcons[currentAppIndex].style.transform = 'scale(1.2)'; // Увеличение размера выбранного AppIcon

    // Воспроизводим звуковой эффект
    clickSound.currentTime = 0; // Сбрасываем текущее время воспроизведения, чтобы можно было воспроизводить многократно
    clickSound.play();
}

// Обработчик события для клавиши вниз
function moveDown() {
    if (currentAppIndex < applications.length - 1) {
        currentAppIndex++;
    } else {
        currentAppIndex = 0;
    }
    updateAppStyles();
}

// Обработчик события для клавиши вверх
function moveUp() {
    if (currentAppIndex > 0) {
        currentAppIndex--;
    } else {
        currentAppIndex = applications.length - 1;
    }
    updateAppStyles();
}

// Функция для обработки эффекта при нажатии Enter
function triggerEnterEffect() {
    const currentIcon = appIcons[currentAppIndex];
    const currentAppName = appNames[currentAppIndex].innerText;

    currentIcon.style.transform = 'scale(1.0)';
    clickSound.currentTime = 0; // Сбрасываем текущее время воспроизведения, чтобы можно было воспроизводить многократно
    clickSound.play();
    setTimeout(() => {
        currentIcon.style.transform = 'scale(1.2)';
        // Проверка имени приложения и переход на соответствующий сайт
        if (currentAppName === 'YouTube') {
            window.location.href = 'https://www.youtube.com/tv';
        } else if (currentAppName === 'Dev Test') {
            window.location.href = './Application/Application/Loader/index.html';
        }
    }, 100);
}

// Обработчик события нажатия клавиш
document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowRight') {
        moveDown();
    } else if (event.key === 'ArrowLeft') {
        moveUp();
    } else if (event.key === 'Enter') {
        triggerEnterEffect();
    }

    // Сбрасываем таймер при нажатии клавиши
    resetInactivityTimer();
});

// Функция для изменения цветов при бездействии
function setInactiveStyles() {
    timeElement.style.color = '#fff';
    saverElement.style.backgroundColor = '#000';
}

// Функция для изменения цветов при активности
function setActiveStyles() {
    timeElement.style.color = 'transparent';
    saverElement.style.backgroundColor = 'transparent';
}

// Функция для сброса таймера бездействия
function resetInactivityTimer() {
    clearTimeout(inactivityTimer);
    setActiveStyles();
    inactivityTimer = setTimeout(setInactiveStyles, 10000); // 10 секунд
}

// Функция для отображения уведомления о подключении пульта
function RemoteConnected() {
    Notify.classList.add('Notify');
    setTimeout(() => {
        Notify.classList.remove('Notify');
    }, 5000);
}

// Функция для обновления времени
function updateTime() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    timeElement.innerHTML = `${hours}:${minutes}`;
}

// Запускаем обновление времени каждую секунду
setInterval(updateTime, 1000);

// Вызываем функцию один раз, чтобы установить начальное время
updateTime();

// Вызываем функцию, чтобы установить начальное состояние стилей
updateAppStyles();
resetInactivityTimer(); // Устанавливаем начальный таймер
