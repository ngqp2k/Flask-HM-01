function addToCart(id, name, price) {
    event.preventDefault();

    fetch('/api/add-to-cart', {
        method: 'POST',
        body: JSON.stringify(
            {
                id: id,
                name: name,
                price: price,
                num_of_nights: document.getElementById('numOfNights').value
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

function deleteCart(roomID) {
    if (confirm("Bạn chắc chắn xóa sản phẩm khỏi giỏ?") === true) {
        fetch(`/api/cart/${roomID}`, {
            method: "delete"
        }).then(res => res.json()).then(data => {
            let d = document.getElementsByClassName("cart-counter");
            for (let e of d)
                e.innerText = data.total_quantity;

            let d2 = document.getElementsByClassName("cart-amount");
            for (let e of d2)
                e.innerText = data.total_amount.toLocaleString("en");

            let e = document.getElementById(`room${roomID}`);
            e.style.display = "none";
        });
    }
}

function pay() {
    if (confirm("Bạn chắc chắn thanh toán?") === true) {
        fetch("/api/pay", {
            method: 'post'
        }).then(res => res.json()).then(data => {
            if (data.status === 200)
                location.reload();
            else
                alert("Something wrong!");
        })
    }
}