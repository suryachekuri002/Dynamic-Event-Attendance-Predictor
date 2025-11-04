// Dropdown
        const eventDropdown = document.getElementById('event');
        const typeDropdown = document.getElementById('type');
        const DayDropdown = document.getElementById('day');
        const MonthDropdown=document.getElementById('month')
        const weatherDropdown = document.getElementById('weather')
        const SeasonDropdown = document.getElementById('season')
        const isWeekendInput = document.getElementById('is_weekend')
        const isHolidayInput = document.getElementById('is_holiday')
        const isWeekendText = document.getElementById('isWeekendText');
        const isHolidayText = document.getElementById('isHolidayText');
    
        //adding weather dropdown options dynamically
        const weatheroptions = ['Windy','Sunny','Cloudy','Rainy','Stormy']
        weatheroptions.forEach(opt => {
            const option = document.createElement('option')
            option.value = opt;
            option.textContent = opt;
            weatherDropdown.appendChild(option)
        })

        //adding seasons dropdown options dynamically
        const seasonoptions = ['Rainy','Winter','Autumn','Summer']
        seasonoptions.forEach(opt => {
            const option = document.createElement('option')
            option.value = opt;
            option.textContent = opt;
            SeasonDropdown.appendChild(option)
        })

        // Adding weekend dropdown options dynamically
        const dayoptions = ['Monday', 'Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        dayoptions.forEach(opt => {
            const option = document.createElement('option')
            option.value = opt;
            option.textContent = opt;
            DayDropdown.appendChild(option)
        });


        //Adding month dropdown options dynamically
        const monthoptions=['January','February','March','April','May','June','July','August','September','October','November','December'];
        monthoptions.forEach(month => {
            const option=document.createElement('option')
            option.value = month;
            option.textContent = month;
            MonthDropdown.appendChild(option)
        })

        //  Dynamic event-type
        eventDropdown.addEventListener('change', function () {
            const eventValue = this.value;
            typeDropdown.innerHTML = '<option value="">Select Type</option>';

            let options = [];

            if (eventValue === 'Political') {
                options = [
                    { value: 'Rally', text: 'Rally' },
                    { value: 'Debate', text: 'Debate' }
                ];
            } else if (eventValue === 'Concert') {
                options = [
                    { value: 'Classical', text: 'Classical' },
                    { value: 'Rock', text: 'Rock' }
                ];
            } else if (eventValue === 'Fashion exhibition') {
                options = [
                    { value: 'Men', text: 'Men' },
                    { value: 'Women', text: 'Women' }
                ];
            } else if (eventValue === 'Prerelease') {
                options = [
                    { value: 'Movie', text: 'Movie' },
                    { value: 'Webseries', text: 'Web Series' }
                ];
            } else if (eventValue === 'Sports') {
                options = [
                    { value: 'Cricket', text: 'Cricket' },
                    { value: 'Tennis', text: 'Tennis' },
                    { value: 'Football', text: 'Football' },
                    { value: 'Badminton', text: 'Badminton' },
                    { value: 'Basketball', text: 'Basketball' }
                ];
            } else if (eventValue === 'Traditional events') {
                options = [
                    { value: 'Dussehra', text: 'Dussehra' },
                    { value: 'Vinayaka chavithi', text: 'Vinayaka Chavithi' }
                ];
            }

            // Appending new Type options dynamically
            options.forEach(opt => {
                const option = document.createElement('option');
                option.value = opt.value;
                option.textContent = opt.text;
                typeDropdown.appendChild(option);
            });
        });

        // Function to create Yes/No dropdowns dynamically
        function createYesNoDropdown(selectElement, hiddenInput) {
       // Clear existing options
        selectElement.innerHTML = '';

       // Creating default option
    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = 'Select (Yes or No)';
    selectElement.appendChild(defaultOption);

    // Creating "Yes" option
    const yesOption = document.createElement('option');
    yesOption.value = 'Yes';
    yesOption.textContent = 'Yes';
    selectElement.appendChild(yesOption);

  // Creating "No" option
    const noOption = document.createElement('option');
    noOption.value = 'No';
    noOption.textContent = 'No';
    selectElement.appendChild(noOption);

  // Add event listener to update hidden numeric input
    selectElement.addEventListener('change', function () {
        const selected = this.value.toLowerCase();
        if (selected === 'yes') {
            hiddenInput.value = 1;
        } else if (selected === 'no') {
            hiddenInput.value = 0;
    } else {
        hiddenInput.value = '';
    }
    });
}

// Initialize dropdowns dynamically
createYesNoDropdown(isWeekendText, isWeekendInput);
createYesNoDropdown(isHolidayText, isHolidayInput);

// Auto-updating Weekend and Holiday dropdowns based on selected day
DayDropdown.addEventListener('change', function () {
    const selectedDay = this.value;

    // Auto setting Weekend
    if (selectedDay === 'Saturday' || selectedDay === 'Sunday') {
        isWeekendText.value = 'Yes';
        isWeekendInput.value = 1;
    } else {
        isWeekendText.value = 'No';
        isWeekendInput.value = 0;
    }

    // Auto setting Holiday
    if (selectedDay === 'Sunday') {
        isHolidayText.value = 'Yes';
        isHolidayInput.value = 1;
    } else {
        isHolidayText.value = 'No';
        isHolidayInput.value = 0;
    }
});

// Dynamically show season options based on selected month
MonthDropdown.addEventListener('change', function () {
    const selectedMonth = this.value.toLowerCase();
    let seasonOptions = [];

    // Determine available seasons based on month
    if (['december', 'january', 'february'].includes(selectedMonth)) {
        seasonOptions = ['Winter'];
    } else if (['march', 'april', 'may'].includes(selectedMonth)) {
        seasonOptions = ['Summer'];
    } else if (['june', 'july', 'august','september'].includes(selectedMonth)) {
        seasonOptions = ['Rainy'];
    } else if ([ 'october', 'november'].includes(selectedMonth)) {
        seasonOptions = ['Autumn'];
    }

    // Clear previous season options
    SeasonDropdown.innerHTML = '';

    // Adding a default "Select Season" option
    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = 'Select Season';
    SeasonDropdown.appendChild(defaultOption);

    // Add the determined season options
    seasonOptions.forEach(season => {
        const option = document.createElement('option');
        option.value = season.toLowerCase();
        option.textContent = season;
        SeasonDropdown.appendChild(option);
    });
});





        