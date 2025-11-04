// Dropdown elements
const eventDropdown = document.getElementById('event');
const typeDropdown = document.getElementById('type');
const DayDropdown = document.getElementById('day');
const MonthDropdown = document.getElementById('month');
const weatherDropdown = document.getElementById('weather');
const SeasonDropdown = document.getElementById('season');
const isWeekendInput = document.getElementById('is_weekend');
const isHolidayInput = document.getElementById('is_holiday');
const isWeekendText = document.getElementById('isWeekendText');
const isHolidayText = document.getElementById('isHolidayText');

// Helper function to populate dropdowns
function populateDropdown(select, options, defaultValue) {
    select.innerHTML = '';
    options.forEach(opt => {
        const option = document.createElement('option');
        option.value = opt;
        option.textContent = opt;
        if (opt === defaultValue) option.selected = true;
        select.appendChild(option);
    });
}

// Weather dropdown (default: Sunny)
populateDropdown(weatherDropdown, ['Windy', 'Sunny', 'Cloudy', 'Rainy', 'Stormy'], 'Sunny');

// Season dropdown (default: Summer)
populateDropdown(SeasonDropdown, ['Rainy', 'Winter', 'Autumn', 'Summer'], 'Summer');

//  Day dropdown (default: Monday)
populateDropdown(DayDropdown, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 'Monday');

//  Month dropdown (default: January)
populateDropdown(MonthDropdown, ['January','February','March','April','May','June','July','August','September','October','November','December'], 'January');

//  Event dropdown (default: Concert)
populateDropdown(eventDropdown, ['Political', 'Concert', 'Fashion exhibition', 'Prerelease', 'Sports', 'Traditional events'], 'Concert');

//  Type dropdown — depends on event
function updateTypeOptions(eventValue) {
    typeDropdown.innerHTML = '';
    let options = [];

    if (eventValue === 'Political') options = ['Rally', 'Debate'];
    else if (eventValue === 'Concert') options = ['Classical', 'Rock'];
    else if (eventValue === 'Fashion exhibition') options = ['Men', 'Women'];
    else if (eventValue === 'Prerelease') options = ['Movie', 'Webseries'];
    else if (eventValue === 'Sports') options = ['Cricket', 'Tennis', 'Football', 'Badminton', 'Basketball'];
    else if (eventValue === 'Traditional events') options = ['Dussehra', 'Vinayaka chavithi'];

    // Default type based on event
    const defaultType = options.length ? options[0] : '';
    options.forEach(opt => {
        const option = document.createElement('option');
        option.value = opt;
        option.textContent = opt;
        if (opt === defaultType) option.selected = true;
        typeDropdown.appendChild(option);
    });
}

// Initialize default event type
updateTypeOptions('Concert');

// Change event updates type options
eventDropdown.addEventListener('change', function () {
    updateTypeOptions(this.value);
});

// Yes/No dropdowns (default: No)
function createYesNoDropdown(selectElement, hiddenInput, defaultValue = 'No') {
    selectElement.innerHTML = '';
    ['Yes', 'No'].forEach(val => {
        const option = document.createElement('option');
        option.value = val;
        option.textContent = val;
        if (val === defaultValue) option.selected = true;
        selectElement.appendChild(option);
    });
    hiddenInput.value = defaultValue === 'Yes' ? 1 : 0;

    selectElement.addEventListener('change', function () {
        hiddenInput.value = this.value === 'Yes' ? 1 : 0;
    });
}

createYesNoDropdown(isWeekendText, isWeekendInput, 'No');
createYesNoDropdown(isHolidayText, isHolidayInput, 'No');

// Auto update weekend/holiday when changing day
DayDropdown.addEventListener('change', function () {
    const selectedDay = this.value;

    if (selectedDay === 'Saturday' || selectedDay === 'Sunday') {
        isWeekendText.value = 'Yes';
        isWeekendInput.value = 1;
    } else {
        isWeekendText.value = 'No';
        isWeekendInput.value = 0;
    }

    if (selectedDay === 'Sunday') {
        isHolidayText.value = 'Yes';
        isHolidayInput.value = 1;
    } else {
        isHolidayText.value = 'No';
        isHolidayInput.value = 0;
    }
});

// Update season when month changes
MonthDropdown.addEventListener('change', function () {
    const selectedMonth = this.value.toLowerCase();
    let seasonOptions = [];

    if (['december', 'january', 'february'].includes(selectedMonth)) seasonOptions = ['Winter'];
    else if (['march', 'april', 'may'].includes(selectedMonth)) seasonOptions = ['Summer'];
    else if (['june', 'july', 'august', 'september'].includes(selectedMonth)) seasonOptions = ['Rainy'];
    else if (['october', 'november'].includes(selectedMonth)) seasonOptions = ['Autumn'];

    populateDropdown(SeasonDropdown, seasonOptions, seasonOptions[0]);
});
