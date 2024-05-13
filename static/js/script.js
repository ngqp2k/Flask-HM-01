function addToCart() {
    event.preventDefault();

    fetch('/api/add-to-cart', {
        method: 'POST',
        body: JSON.stringify(
            {
                id: 1,
                name: "Item 1",
                price: 10.00
            }
        ),
        headers: {
            'Content-Type': 'application/json'
        }
    })
}

function test() {
    event.preventDefault();

    alert('Test');

    fetch('/api/test', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
}