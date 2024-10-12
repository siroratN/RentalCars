function setPrice(STRIPE_PUBLIC_KEY, csrf_token) {
    const stripe = Stripe(STRIPE_PUBLIC_KEY)
    const selectedCars = JSON.parse(localStorage.getItem('selectedCars')) || []
    const price = selectedCars.reduce((total, car) => {
        const startDate = new Date(car.start_date)
        const endDate = new Date(car.end_date)
        const days = Math.ceil((endDate - startDate) / (1000 * 3600 * 24))
        return total + (car.price * days)
    }, 0)
    const carIds = selectedCars.map((car) => car.id)
    const startDates = selectedCars.map((car) => car.start_date)
    const endDates = selectedCars.map((car) => car.end_date)
    
    fetch('/create-checkout-session/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify({ car_id: carIds, price: price, start_date: startDates, end_date: endDates })
    })
    .then(function (response) {
        return response.json()
    })
    .then(function (session) {
        localStorage.clear()
        return stripe.redirectToCheckout({ sessionId: session.id })
    })
}