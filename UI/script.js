// Получаем все элементы .Application и их дочерние элементы .AppName и .AppIcon
const applications = document.querySelectorAll('.Application');
const appIcons = document.querySelectorAll('.AppIcon');
const appNames = document.querySelectorAll('.AppName');
const Notify = document.getElementById('InfoBlock');

// Изначально выбранное приложение (начинаем с первого)
let currentAppIndex = 0;

// Создаем аудио элемент для воспроизведения звука
const clickSound = new Audio('media/click.mp3');

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

// Добавляем обработчики событий для клавиш вниз и вверх
document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowRight') {
        moveDown();
    } else if (event.key === 'ArrowLeft') {
        moveUp();
    } else if (event.key === 'Enter') {
        triggerEnterEffect();
    }
});

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
        } else if (currentAppName === 'Screencast') {
            window.location.href = 'Application/Screencast/index.html';
        } else if (currentAppName === 'Settings') {
            window.location.href = 'Application/Settings/index.html';
        }
    }, 100);
}

function RemoteConnected() {
    Notify.classList.add('Notify');
    setTimeout(() => {
        Notify.innerHTML = 'Подключен пульт';
    }, 2000);
    setTimeout(() => {
        Notify.classList.remove('Notify');
        Notify.innerHTML = '';
    }, 2000);
}

// Вызываем функцию, чтобы установить начальное состояние стилей
updateAppStyles();
