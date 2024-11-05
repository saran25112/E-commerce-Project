$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 2,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 4,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 6,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2] 
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText=data.quantity 
            document.getElementById("amount").innerText=data.amount 
            document.getElementById("totalamount").innerText=data.totalamount
            location.reload();
        }
    })
})

$('.minus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2] 
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText=data.quantity 
            document.getElementById("amount").innerText=data.amount 
            document.getElementById("totalamount").innerText=data.totalamount
            location.reload();
        }
    })
})


$('.remove-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id:id
        },
        success:function(data){
            document.getElementById("amount").innerText=data.amount 
            document.getElementById("totalamount").innerText=data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
            location.reload(); 
        }
    })
})


$('.plus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/pluswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            //alert(data.message)
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})


$('.minus-wishlist').click(function() {
    var id = $(this).attr("pid").toString();
    var wishlistItem = $(this).closest('.wishlist-item'); // Adjust selector based on your wishlist item structure
    
    $.ajax({
        type: "GET",
        url: "/minuswishlist",
        data: {
            prod_id: id
        },
        success:function(data){
            //alert(data.message)
            location.reload(); 
        }
    });
});


function updateCategoryTitle(newTitle) {
    // Update the title on the page
    document.getElementById("categoryTitle").textContent = newTitle;
    
    // Store the selected title in session storage
    sessionStorage.setItem('selectedCategoryTitle', newTitle);
}

// Load the saved title from session storage on page load
document.addEventListener("DOMContentLoaded", function() {
    const savedTitle = sessionStorage.getItem('selectedCategoryTitle');
    if (savedTitle) {
        document.getElementById("categoryTitle").textContent = savedTitle;
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    const cartSlidePanel = document.getElementById('cartSlidePanel');
    const closePanelBtn = document.getElementById('closePanelBtn');
    const cartItemsList = document.getElementById('cart-items');
    const amountSpan = document.getElementById('amount');
    const totalAmountSpan = document.getElementById('totalamount');

    // Open slide panel and update cart when an "Add to Cart" button is clicked
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            cartSlidePanel.classList.add('active'); // Show panel
            const productId = this.getAttribute('data-product-id');

            fetch(`/add-to-cart/?prod_id=${productId}`, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.innerHTML = 'Added &nbsp;&nbsp;&nbsp;<i class="fa-solid fa-check"></i>';
                    this.classList.add('added-to-cart5');
                    updateCart(data.cart_items, data.amount, data.totalamount);
                } else {
                    alert("Error adding product to cart.");
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });

    // Close the slide panel
    closePanelBtn.addEventListener('click', function () {
        cartSlidePanel.classList.remove('active');
        location.reload(); 
    });

    // Update cart quantity or remove item
    cartItemsList.addEventListener('click', function (e) {
        const actionElement = e.target.closest('.plus-cart, .minus-cart, .remove-cart');
        if (!actionElement) return;

        const action = actionElement.classList.contains('plus-cart') ? 'increase' :
                    actionElement.classList.contains('minus-cart') ? 'decrease' : null;
        const productId = actionElement.getAttribute('pid');

        if (!productId) {
            console.error('Error: Product ID is missing');
            return;
        }

        let url = '';
        if (action) {
            // For quantity increase or decrease
            url = `/update-cart/?prod_id=${productId}&action=${action}`;
        } else {
            // For item removal
            url = `/remove-from-cart/?prod_id=${productId}`;
        }

        fetch(url, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateCart(data.cart_items, data.amount, data.totalamount);
            } else {
                alert(data.error || "Error updating cart.");
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });


    // Update cart content dynamically
    function updateCart(items, amount, totalamount) {
        cartItemsList.innerHTML = '';

        items.forEach(item => {
            const listItem = document.createElement('li');
            listItem.classList.add('list-group-item');

            listItem.innerHTML = `
                <div class="row">
                    <div class="col-sm-3 text-center align-self-center">
                        <img src="${item.product_image}" alt="${item.product_name}" class="img-fluid img-thumbnail shadow-sm" height="150" width="150">
                    </div>
                    <div class="col-sm-9">
                        <h5>${item.product_name}</h5>
                        <div class="my-3">
                            <label for="quantity">Quantity:</label>
                            <a class="minus-cart btn" pid="${item.product_id}">
                                <i class="fa fa-minus-square fa-lg"></i>
                            </a>
                            <span>${item.quantity}</span>
                            <a class="plus-cart btn" pid="${item.product_id}">
                                <i class="fas fa-plus-square fa-lg"></i>
                            </a>
                        </div>
                        <div class="d-flex justify-content-between">
                            <a href="#" class="remove-cart btn btn-sm btn-secondary" pid="${item.product_id}">
                                Remove item
                            </a>
                            <p class="mb-0"><strong>Rs. ${item.total_price}</strong></p>
                        </div>
                    </div>
                </div>
                <hr class="text-muted">
            `;

            cartItemsList.appendChild(listItem);
        });

        amountSpan.textContent = `Rs. ${amount}`;
        totalAmountSpan.textContent = `Rs. ${totalamount}`;
    }
});

