function addToCart(id, name, price) {
    event.preventDefault();

    fetch('/api/add-to-cart', {
        method: 'POST',
        body: JSON.stringify(
            {
                id: id,
                name: name,
                price: price
            }
        ),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function (response) {
        console.info(response)
        return response.json()
    }).then(function (data) {
        console.info(data)
        let cartCounter = document.getElementById('cartCounter')

        cartCounter.innerText = data.total_quantity
    }).catch(function (error) {
        console.error(error);
    })
}
