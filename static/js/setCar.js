function setCar(start_date, end_date, element) {
    const carID = element.getAttribute('data-car-id');
    const carMake = element.getAttribute('data-car-make');
    const carModel = element.getAttribute('data-car-model');
    const carYear = element.getAttribute('data-car-year');
    const carPrice = element.getAttribute('data-car-price');
    
    const car = {
        id: carID,
        make: carMake,
        model: carModel,
        year: carYear,
        price: carPrice,
        start_date: start_date,
        end_date: end_date
    };

    let selectedCars = JSON.parse(localStorage.getItem("selectedCars")) || [];
    selectedCars.push(car);
    localStorage.setItem("selectedCars", JSON.stringify(selectedCars));
    
    console.log("Car added to localStorage:", car);
}
